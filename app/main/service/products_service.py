import copy, requests, os, jwt, re

from flask_restx import abort

from app.main import db
from app.main.model.product import Product
from app.main.model.product_image import ProductImage
from app.main.model.category import Category
from app.main.service.auth_service import get_user_by_id
from app.main.service.cart_service import delete_cart_by_product
from app.main.utils.image_helper import (
    generate_filename, 
    b64str_to_byte, 
    allowed_mimetype
)
from app.main.utils.celery_tasks import upload_to_gcs, remove_from_gcs

########### GET PRODUCT LIST ###########
def get_product_list(data, headers):
    current_user = _get_user_identity(headers)
    if current_user and current_user.type.value == "seller":
        products_list = db.session.execute(db.select(Product)).scalars().all()
        response_body = {"data": products_list, "total_rows": len(products_list)}
    else:
        response_body = _product_list(data)

    return response_body

def _product_list(data):
    # order / sort by price
    sort_price = None
    if 'sort_by' in data:
        if data['sort_by'] == "Price a_z":
            sort_price = db.asc(Product.price)
        elif data['sort_by'] == "Price z_a":
            sort_price = db.desc(Product.price)

    filters = tuple()
    # only available product and category
    filters += (db.and_(Product.deleted=="0", Category.deleted=="0"), )
    # filter by category
    if 'category' in data:
        category = data['category'].split(',')
        filters += (Product.category_id.in_(category), )
    # filter by price (lower, higher)
    if 'harga' in data: # key: price
        start, end = data['harga'].split(',')
        filters += (Product.price.between(start, end), )
    # filter by conditon new/used
    if 'kondisi' in data: # key: condition
        condition = data['kondisi'].split(',')
        filters += (Product.condition.in_(condition), )
    # filter by similar names
    if 'product_name' in data:
        filters += (Product.name.like('%'+str(data['product_name'])+'%'), )
    # query; get product list
    try:
        result = db.paginate(
            db.select(Product)
                .join(Category)
                .filter(*filters)
                .order_by(sort_price),
            page=int(data['page']),
            per_page=int(data['page_size'])
        )
        response_body = {"data": result.items, "total_rows": result.total}
        if not result.items:
            response_body.update({'success': False, 'message': 'No items available'})
            return response_body, 404
    except ValueError as e:
        abort(400, 'Page and page size must be numeric')
    except db.exc.DataError as e:
        abort(500, "Something went wrong", error=str(e.orig))
    
    return response_body


########### GET PRODUCT DETAIL ###########
def get_product_detail(product_id):
    try:
        result = db.session.execute(
            db.select(Product)
            .filter_by(id=product_id)
            .options(db.joinedload(Product.category))
        ).scalar()
    except db.exc.DataError as e:
        abort(500, "Something went wrong", error=str(e.orig))
    if not result:
        abort(404, c_not_found='Item not available')
    return result

########### Admin Page ###########
########### Save new product ###########
def save_new_product(data):
    result_data = _validation(data)
    try:
        ### store new product ###
        new_product = Product(**result_data)
        db.session.add(new_product)
        db.session.flush()
        ### upload image ###
        if 'images' in data:
            images_name = _upload_images(data)
            ### store filename to db ###
            images_obj = list()
            for name in images_name:
                images_obj.append(
                    ProductImage(
                        product_id = new_product.id,
                        image = name
                    )
                )
            db.session.add_all(images_obj)

        db.session.flush()
    except:
        db.session.rollback()
        abort(500, "Product could not be added")
    
    db.session.commit()
    return {"message": "Product added"}, 201

def save_product_changes(data):
    result_data = _validation(data)
    
    try:
        db.session.execute(
            db.update(Product)
            .where(Product.id == data['product_id'])
            .values(**result_data)
        )
        if 'images' in data:
            keep_images = [e.split('/')[-1] for e in data['images'] if 'data' not in e]
            new_images = [e for e in data['images'] if 'data' in e]

            deleted_rows = db.session.execute(
                db.delete(ProductImage)
                .where(ProductImage.product_id == data['product_id'])
                .filter(ProductImage.image.not_in(keep_images))
                .returning(ProductImage.image)
            ).fetchall()

            if deleted_rows:
                images_to_delete = [e[0] for e in deleted_rows]
                _remove_images(images_to_delete)
            
            if new_images:
                data['images'] = new_images
                if keep_images:
                    data.update({
                        "last_image": keep_images[-1]
                    })
                images_name = _upload_images(data)
                images_obj = list()
                for name in images_name:
                    images_obj.append(
                        ProductImage(
                            product_id = data['product_id'],
                            image = name
                        )
                    )
                db.session.add_all(images_obj)
    
        db.session.flush()
    except:
        db.session.rollback()
        abort(500, "Product could not be updated")
    
    db.session.commit()

    return {"message": "Product updated"}, 200

########### REMOVE PRODUCT ###########
def mark_as_deleted(product_id):
    try:
        product = db.session.execute(
            db.select(Product)
            .filter_by(id=product_id)
            .options(db.noload(Product.images))
        ).scalar_one()
        product.deleted = "1"
        db.session.commit()
    except db.exc.DataError:
        db.session.rollback()
        abort(404, "Item not available")
    
    delete_cart_by_product(product.id)

    return {"message": "Product deleted"}, 200

########### search by image and return category of image ###########
def search_by_image(data):
    try:
        image_result = b64str_to_byte(data['image'])
        ### send request to image prediction server ###
        url = os.environ['IMAGE_PREDICTION_URL']
        files = {'file': image_result}
        r = requests.post(url, files=files)
        ### get category from response (html script) image prediction ###
        response_text = r.text
        category = re.search("Detected Image: (.*?)<", response_text).group(1)
        if category.lower() == "error":
            raise KeyError()
        ### get the category id based on the prediction result ###
        name_list = category.split()
        result = db.session.execute(
            db.select(Category.id)
            .filter(db.or_(*[Category.name.like('%'+name+'%') for name in name_list]))
        ).scalars().all()
        if not result:
            abort(404, c_not_found="There is no category for that image")
        category_id = ','.join([str(e) for e in result])
        response_data = {"category_id": category_id}
    except KeyError:
        abort(500, "Something went wrong")
    except IndexError:
        abort(500, "Something went wrong")

    return response_data

########### Save Images ###########
def _upload_images(data):
    def secure_name(name):
        ### replace some special characters with hyphens ###
        name = name.translate({ord(c): "-" for c in " `~!@#$%^*()_={}[]|\:;'\"<>,.?/"})
        name = name.replace('+', 'plus')
        name = name.replace('&', 'and')
        return name.lower()
    
    name = secure_name(data['product_name'])
    images = list()
    no = 1
    if 'last_image' in data and data['last_image']:
        last_section = data['last_image'].split("-")[-1]
        last_section = last_section.split(".")[0]
        no = int(last_section)+1 if last_section.isdigit() else no

    for e in data['images']:
        image = dict()
        ### validation ###
        media_type = e.split(',')[0]
        media_type = media_type[media_type.find(':')+1 : media_type.find(';')]
        allowed_mimetype(media_type)
        ### decode ###
        result_byte = b64str_to_byte(e)
        ### generate filename ###
        filename = generate_filename(
            name=name,
            media_type=media_type, 
            condition=data['condition'],
            other=str(no).zfill(2)
        )

        image.update({
            "filename": filename,
            "media_type": media_type,
            "file": result_byte
        })
        images.append(image)
        no+=1
    
    for image in images:
        upload_to_gcs.apply_async(args=[image], countdown=3)

    images_name = [e['filename'] for e in images]
    return images_name

def _remove_images(data: list):
    for filename in data:
        remove_from_gcs.apply_async(args=[filename], countdown=3)
    

########### Validation ###########
def _validation(data: dict) -> dict:
    """
    Validations that json schema cannot handle.
    And format the data for the object at the same time.
    """
    result_data = copy.deepcopy(data)
    ########### Product unique based on name, category, and condition ###########
    product_exists = db.session.execute(
        db.select(Product)
        .filter(db.and_(Product.name==result_data['product_name'], Product.deleted=="0"))
        .options(
            db.noload(Product.images),
            db.joinedload(Product.category)
        )
    ).scalars()
    if product_exists:
        for product in product_exists:
            if str(product.category_id) == result_data['category'] \
            and product.condition.value == result_data['condition'].lower():
                if 'product_id' not in result_data:
                    abort(400, 'There is already a product with that name, category, and condition')
                if 'product_id' in result_data and result_data['product_id'] != str(product.id):
                    abort(400, 'There is already a product with that name, category, and condition')

    ### Rename properties to match database model ###
    result_data.update({'name': result_data.pop('product_name')})
    result_data.update({'category_id': result_data.pop('category')})
    ### remove properties ###
    if 'product_id' in result_data:
        result_data.pop('product_id')
    if 'images' in result_data:
        result_data.pop('images')
    return result_data

def _get_user_identity(headers):
    if "Authentication" in headers and headers["Authentication"]:
        user = jwt.decode(headers["Authentication"], os.environ.get('SECRET_KEY'), algorithms=["HS256"])
        current_user = get_user_by_id(user['id'])
        return current_user
    else:
        return None