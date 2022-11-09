import re, uuid, copy

from flask_restx import abort

from app.main import db
from app.main.model.product import Product, ProductCondition
from app.main.model.product_image import ProductImage
from app.main.model.category import Category
from app.main.service.image_service import check_extension


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

def get_product_detail(product_id):
    result = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
    if not result:
        abort(404, c_not_found='Item not available')
    return result


########### Admin Page ###########
def save_new_product(data):
    result_data = _validation(data)
    try:
        new_product = Product(**result_data)
        db.session.add(new_product)
        db.session.flush()
        images = re.sub('[[\] ]', '', data['images']).split(',')
        images_obj = list()
        for image in images:
            check_extension(image)
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
    else:
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
            check_extension(image)
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

def mark_as_deleted(product_id):
    try:
        product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar_one()
    except db.exc.NoResultFound:
        abort(404, "Item not available")
    
    product.is_deleted = "1"
    db.session.commit()

    return {"message": "Product deleted"}, 200

def _validation(data):
    result_data = copy.deepcopy(data)
    
    ### Product unique based on name, category, and condition ###
    product_exists = db.session.execute(db.select(Product).filter_by(name=result_data['product_name'])).first()
    if product_exists:
        if str(product_exists[0].category_id) == result_data['category'] \
        and product_exists[0].condition.value == result_data['condition'].lower():
            if 'product_id' in result_data and result_data['product_id'] != str(product_exists[0].id):
                abort(400, 'There is already a product with that name, category, and condition')
        abort(400, 'There is already a product with that name, category, and condition')

    ### condition ###
    if result_data['condition'].lower() not in [e.value for e in ProductCondition]:
        abort(400, 'Condition is invalid, condition must be new or used')

    ### category ###
    category_exist = db.session.execute(db.select(Category).filter_by(id=result_data['category'])).first()
    if not category_exist:
        abort(400, 'Category does not exist')

    ### product id ###
    if 'product_id' in result_data:
        try:
            uuid.UUID(result_data['product_id'])
        except ValueError:
            abort(400, 'Invalid product id')
        result_data.pop('product_id')

    result_data.update({'name': result_data.pop('product_name')})
    result_data.update({'category_id': result_data.pop('category')})
    result_data.pop('images')
    return result_data