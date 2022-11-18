import re, uuid, copy, requests, base64, os

from flask_restx import abort

from app.main import db
from app.main.model.product import Product, ProductCondition
from app.main.model.product_image import ProductImage
from app.main.model.category import Category
from app.main.utils.image_helper import allowed_file_media, rename_filestorage
from app.main.utils.celery_tasks import upload_to_gcp

########### GET PRODUCT LIST ###########
def get_product_list(data):
    # order / sort by price
    sort_price = None
    if 'sort_by' in data:
        if data['sort_by'].lower() == "price a_z":
            sort_price = db.asc(Product.price)
        elif data['sort_by'].lower() == "price z_a":
            sort_price = db.desc(Product.price)

    filters = tuple()
    # filter by category
    if 'category' in data:
        category = re.sub('[ ]', '', data['category']).split(',')
        try:
            for id in category:
                uuid.UUID(id)
        except ValueError:
            abort(400, 'Invalid category id')
        filters += (Product.category_id.in_(category), )
    else:
        filters += (Product.category_id.is_not(None), )
    # filter by price (lower, higher)
    if 'price' in data:
        try:
            start, end = re.sub('[ ]', '', data['price']).split(',')
            filters += (Product.price.between(int(start), int(end)), )
        except ValueError:
            abort(400, 'Invalid price range')
    # filter by conditon new/used
    if 'condition' in data:
        if data['condition'].lower() not in [e.value for e in ProductCondition]:
            abort(400, 'Invalid condition, condition must be either new or used')
        filters += (Product.condition == data['condition'].lower(), )
    # filter by similar names
    if 'product_name' in data:
        filters += (Product.name.like('%'+str(data['product_name'])+'%'), )
    # query; get product list
    try:
        products = db.paginate(
            db.select(Product)
                .where(Product.is_deleted == "0")
                .filter(*filters)
                .order_by(sort_price),
            page=int(data['page']),
            per_page=int(data['page_size'])
        )
    except ValueError:
        abort(400, 'Page and page size must be a number')
    except IndexError:
        abort(400, 'Page and page size is required')
    # formatting for response marshalling
    result = {"data": products.items, "total_rows": len(products.items)}
    if not products.items:
        result.update({'success': True, 'message': 'No items available'})

    return result

########### GET PRODUCT DETAIL ###########
def get_product_detail(product_id):
    result = db.session.execute(db.select(Product).filter_by(id=product_id)).get()
    if not result:
        abort(404, c_not_found='Item not available')
    return result

########### Admin Page ###########
########### Save new product ###########
def save_new_product(data, files=None):
    result_data = _validation(data)
    try:
        ### store new product ###
        new_product = Product(**result_data)
        db.session.add(new_product)
        db.session.flush()
        ### upload image ###
        images_name = upload_images(new_product, files=files)
        ### store filename to db ###
        images_obj = list()
        for image in images_name:
            images_obj.append(
                ProductImage(
                    product_id = new_product.id,
                    image = image
                )
            )
        db.session.add_all(images_obj)
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
        db.session.execute(
            db.delete(ProductImage).where(ProductImage.product_id == data['product_id'])
        )

        images = re.sub('[[\]]', '', data['images']).split(', ')
        images_obj = list()
        for image in images:
            allowed_file_media(image)
            images_obj.append(
                ProductImage(
                    product_id = data['product_id'],
                    image = image
                )
            )
        db.session.add_all(images_obj)
    except:
        db.session.rollback()
        abort(500, "Product could not be updated")
    else:
        db.session.commit()

    return {"message": "Product updated"}, 200

########### REMOVE PRODUCT ###########
def mark_as_deleted(product_id):
    try:
        product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar_one()
    except db.exc.NoResultFound:
        abort(404, "Item not available")
    
    product.is_deleted = "1"
    db.session.commit()

    return {"message": "Product deleted"}, 200

########### search by image and return category of image ###########
def search_by_image(data):
    try:
        ### decode base64 string image ###
        is_type_exists = re.search("data", data['image'])
        if is_type_exists:
            media_type, image_b64 = data['image'].split(',')
            media_type = re.findall(":(.*?);", media_type)
            if media_type[0] != 'image/jpeg':
                abort(415, "Unsupported media type; only JPEG is supported")
            image_result = base64.b64decode(image_b64)
        else:
            image_result = base64.b64decode(data['image'])
        ### send request to image prediction server ###
        url = os.environ['IMAGE_PREDICTION_URL']
        files = {'file': image_result}
        r = requests.post(url, files=files)
        ### get category from response (html script) image prediction ###
        category = re.findall("Detected Image: (.*?)<", r.text)
        if category[0].lower() == "error":
            raise IndexError()
        ### get the category id based on the prediction result ###
        result = db.session.execute(db.select(Category).filter_by(name=category[0])).first()
        if not result:
            abort(404, c_not_found="Product not found")
        response_data = {"category_id": result[0].id}
    except KeyError:
        abort(500, "Something went wrong")
    except IndexError:
        abort(500, "Something went wrong")

    return response_data

########### Save Images ###########
def upload_images(data, files=None):
    def secure_name(name):
        ### replace some special characters with hyphens ###
        name = re.sub('[`~!@#$%^*()_={}[\]|\\:;\'\"<>,.?/ ]', "-", name)
        name = name.replace('+', 'plus')
        name = name.replace('&', 'and')
        return name.lower()

    if not files:
        abort(400, "Images required")

    images = files.getlist('images')
    
    for image in images:
        allowed_file_media(image.filename)

    name = secure_name(data.name)
    condition = data.condition
    rename_filestorage(images, name=name, condition=condition, many=True)

    for image in images:
        upload_file = dict(**image.__dict__)
        upload_file['stream'] = base64.b64encode(image.read())
        upload_file.pop('_parsed_content_type')
        upload_data = {
            "file": upload_file,
            "bucket": 'image_fc',
            "path": "product/"
        }
        ### Background task for upload images ###
        upload_to_gcp.apply_async(args=[upload_data], countdown=3)

    images_name = [e.filename for e in images]
    return images_name

########### Validation ###########
def _validation(data: dict) -> dict:
    """
    Validations that json schema cannot handle.
    And format the data for the object at the same time.
    """
    result_data = copy.deepcopy(data)
    result_data = result_data.to_dict()
    ########### Product unique based on name, category, and condition ###########
    product_exists = db.session.execute(db.select(Product).filter_by(name=result_data['product_name'])).first()
    if product_exists:
        if str(product_exists[0].category_id) == result_data['category'] \
        and product_exists[0].condition.value == result_data['condition'].lower():
            if 'product_id' not in result_data:
                abort(400, 'There is already a product with that name, category, and condition')
            if 'product_id' in result_data and result_data['product_id'] != str(product_exists[0].id):
                abort(400, 'There is already a product with that name, category, and condition')
    ########### is category exists ###########
    category_exist = db.session.execute(db.select(Category).filter_by(id=result_data['category'])).first()
    if not category_exist:
        abort(400, 'Category does not exist')
    ########### is product id valid ###########
    if 'product_id' in result_data:
        try:
            uuid.UUID(result_data['product_id'])
        except ValueError:
            abort(400, 'Invalid product id')
        ### remove product id properties ###
        result_data.pop('product_id')
    ### Rename properties to match database model ###
    result_data.update({'name': result_data.pop('product_name')})
    result_data.update({'category_id': result_data.pop('category')})
    ### remove images properties ###
    return result_data
