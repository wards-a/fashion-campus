import copy, requests, os, jwt, re

from flask_restx import abort

from app.main import db
from app.main.model.product import Product
from app.main.model.product_image import ProductImage
from app.main.model.category import Category
from app.main.service.auth_service import get_user_by_id
from app.main.service.cart_service import delete_cart_by_product
from app.main.dependencies.elasticsearch_manage import ES
from app.main.utils.image_helper import (
    generate_filename, 
    b64str_to_byte,
    allowed_mimetype,
    resize_image,
    secure_name
)
from app.main.utils.celery_tasks import (
    upload_to_gcs,
    remove_from_gcs,
    insert_to_es,
    update_to_es,
    deleted_to_es
)


########### GET PRODUCT LIST ###########
def get_product_list(data, headers):
    es = ES()
    current_user = _get_user_identity(headers)
    if current_user and current_user.type.value == "seller":
        resp = es.get_all_data(index="products")
        products_list = [e['_source'] for e in resp]
        response_body = {"data": products_list, "total_rows": len(products_list)}
    else:
        response_body = _product_list(data)

    return response_body

def _product_list(data):
    # order / sort by price
    es = ES()
    query = {"bool": {}, }
    must = list()
    filter = list()

    sort = None
    if 'sort_by' in data:
        if data['sort_by'] == "Price a_z":
            sort = [{"price": "asc"}]
        elif data['sort_by'] == "Price z_a":
            sort = [{"price": "desc"}]

    # only available product and category
    must.append({"term": {"category_deleted": "false"}})
    must.append({"term": {"deleted": "false"}})
    # filter by category
    if 'category' in data:
        categories = data['category'].split(',')
        filter.append({
            "terms": {
                "category_id": categories
            }
        })
    # filter by price (lower, higher)
    if 'price' in data:
        start, end = data['price'].split(',')
        must.append({
            "range": {
                "price": {
                    "gte": start,
                    "lte": end
                }
            }
        })
    # filter by conditon new/used
    if 'condition' in data:
        condition = data['condition'].split(',')
        filter.append({
            "terms": {
                "condition": condition
            }
        })
    # filter by similar names
    if 'product_name' in data and data['product_name']:
        must.append({"wildcard": {"name": f"*{data['product_name']}*"}})
    # query; get product list
    try:
        result_data = list()
        query['bool']['must'] = must
        query['bool']['filter'] = filter
        from_ = (int(data['page'])-1)*int(data['page_size'])
        size = int(data['page_size'])
        es.get_pagination_data(index="products", query=query, from_=from_, size=size, sort=sort)
        total_rows = es.resp['hits']['total']['value']
        
        for hit in es.resp['hits']['hits']:
            result_data.append(hit["_source"])
        
        response_body = {"data": result_data, "total_rows": total_rows}
        if total_rows <= 0:
            response_body.update({'success': True, 'message': 'No items available'})
            return response_body, 404
    except ValueError as e:
        return {"message": "Page and page size must be numeric"}, 400
    
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
        return {"message": "Something went wrong", "error": str(e.orig)}, 500
    if not result:
        abort(404, c_not_found='Item not available')
    return result

########### Admin Page ###########
########### Save new product ###########
def save_new_product(data):
    _data_to_es = dict()
    result_data = _validation(data)
    try:
        ### store new product ###
        new_product = Product(**result_data)
        db.session.add(new_product)
        db.session.flush()
        _data_to_es.update({"product": new_product})
        ### upload image ###
        if 'images' in data:
            images_name = _upload_images(data)
            _data_to_es.update({"images": images_name})
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
        return {"message": "Product could not be added"}, 500
    
    db.session.commit()

    category = db.session.execute(db.select(Category).where(Category.id==new_product.category_id)).scalar()
    _data_to_es.update({"category": category})
    insert_to_es.apply_async(kwargs=_data_to_es, countdown=3)
    return {"message": "Product added"}, 201

def save_product_changes(data):
    _data_to_es = dict()
    result_data = _validation(data)
    try:
        db.session.execute(
            db.update(Product)
            .where(Product.id == data['product_id'])
            .values(**result_data)
        )

        _data_to_es.update({"product": result_data})
        _data_to_es['product']['id'] = data['product_id']
        deleted = db.session.execute(db.select(Product.deleted).where(Product.id==data['product_id'])).scalar()
        _data_to_es['product']['deleted'] = deleted.value

        if 'images' in data:
            keep_images = [e.split('/')[-1] for e in data['images'] if 'data' not in e]
            new_images = [e for e in data['images'] if 'data' in e]

            if keep_images:
                _data_to_es.update({"images": keep_images})

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
                _data_to_es['images'] += new_images
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
        return {"message": "Product could not be updated"}, 500
    
    db.session.commit()

    category = db.session.execute(db.select(Category).where(Category.id==result_data['category_id'])).scalar()
    _data_to_es.update({"category": category})
    update_to_es.apply_async(kwargs=_data_to_es, countdown=3)

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
        return {"message": "Item not available"}, 404
    
    delete_cart_by_product(product.id)

    deleted_to_es.apply_async(kwargs={"data": {"key": "id", "value": product_id}, "field": "deleted"})
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
            .filter(db.or_(*[Category.name.ilike('%'+name+'%') for name in name_list]))
        ).scalars().all()
        if not result:
            return {"message": "Category not available"}, 404
    except KeyError as e:
        return {"message": "Something went wrong", "error": str(e)}, 500
    except IndexError:
        return {"message": "Something went wrong", "error": str(e)}, 500

    return {"category_id": result}

########### Save Images ###########
def _upload_images(data):
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
        ### compress ###
        im = resize_image(result_byte, basewidth=600)
        ### generate filename ###
        filename = generate_filename(
            name=name,
            media_type=media_type, 
            condition=data['condition'],
            other=str(no).zfill(2)
        )

        image.update({
            "filename": filename,
            "media_type": "image/jpeg",
            "file": im
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