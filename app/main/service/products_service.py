import re

from flask import abort

from app.main import db
from app.main.model.product import Product, ProductCondition
from app.main.model.product_image import ProductImage
from app.main.model.category import Category
from app.main.service.image_service import check_extension


def get_product_list(data):
    # order / sort by price
    sort_price = None
    if 'sort_by' in data.keys():
        if data['sort_by'].lower() == "price a_z":
            sort_price = db.asc(Product.price)
        elif data['sort_by'].lower() == "price z_a":
            sort_price = db.desc(Product.price)

    filters = tuple()

    # filter by category
    if 'category' in data.keys():
        category = re.sub('[ ]', '', data['category']).split(',')
        filters += (Product.category_id.in_(category), )
    

    # filter by price (lower, higher)
    if 'price' in data.keys():
        start, end = re.sub('[ ]', '', data['price']).split(',')
        filters += (Product.price.between(int(start), int(end)), )

    # Filters by similar names
    if 'product_name' in data.keys():
        filters += (Product.name.like('%'+data['product_name']+'%'), )
    
    # query; get product list
    products = db.paginate(
        db.select(Product)
            .where(Product.is_deleted == "0")
            .filter(*filters)
            .order_by(sort_price),
        page=int(data['page']),
        per_page=int(data['page_size'])
    )

    # dict formatting for response marshalling
    result = {"data": products.items, "total_rows": len(products.items)}
    return result

def get_product_detail(product_id):
    result = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
    return result


########### Admin Page ###########
def save_new_product(data):
    _validation(data)
    try:
        new_product = Product(
            name = data['product_name'],
            description = data['description'],
            condition = data['condition'].lower(),
            category_id = data['category'],
            price = data['price']
        )
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
        abort(400, "Product could not be added")
    else:
        db.session.commit()

    return {"message": "Product added"}, 201

def save_product_changes(data):
    _validation(data)
    try:
        db.session.execute(
            db.update(Product)
            .where(Product.id == data['product_id'])
            .values({
                "name": data['product_name'],
                "description": data['description'],
                "condition": data['condition'].lower(),
                "category_id": data['category'],
                "price": data['price']
            })
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
        abort(400, "Product could not be updated")
    else:
        db.session.commit()

    return {"message": "Product updated"}, 200

def mark_as_deleted(product_id):
    try:
        db.session.execute(
        db.update(Product)
        .where(Product.id == product_id)
        .values(is_deleted="1"))
    except:
        db.session.rollback()
        abort(400, "Product cannot be deleted")
    else:
        db.session.commit()

    return {"message": "Product deleted"}, 200

def _validation(data):
    ### Product unique based on name, category, and condition ###
    if 'product_id' not in data.keys():
        product_exists = db.session.execute(db.select(Product).filter_by(name=data['product_name'])).first()[0]
        if str(product_exists.category_id) == data['category'] \
        and product_exists.condition.value == data['condition'].lower():
            abort(400, 'There is already a product with that name, category, and condition')

    ### Product name ###
    if len(data['product_name']) < 1:
        abort(400, 'Product is required')

    ### images ###
    if len(data['images']) < 1:
        abort(400, 'Image is required')
    
    ### condition ###
    if len(data['condition']) < 1:
        abort(400, 'Condition is required')
    
    if data['condition'].lower() not in ProductCondition.__members__.values():
        abort(400, 'Condition is invalid, condition must be new or used')

    ### category ###
    if len(data['category']) < 1:
        abort(400, 'Category is required')
    
    category_exist = db.session.execute(db.select(Category).filter_by(id=data['category'])).first()
    if not category_exist:
        abort(400, 'Category does not exist')
    
    ### price ###
    if len(data['price']) < 1:
        abort(400, 'Price is required')
    if data['price'] < 1:
        abort(400, 'Price value must be positive')
