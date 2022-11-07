import re

from flask import abort

from app.main import db
from app.main.model.product import Product
from app.main.model.product_image import ProductImage
from app.main.service.image_service import check_extension


def get_product_detail(product_id):
    result = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
    return result

def save_new_product(data):
    try:
        new_product = Product(
            name = data['product_name'],
            description = data['description'],
            condition = data['condition'],
            category_id = data['category'],
            price = data['price']
        )
        db.session.add(new_product)
        db.session.flush()
        images = re.sub('[[\]]', '', data['images']).split(', ')
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
        abort(400, description="Product could not be added")
    else:
        db.session.commit()

    return {"message": "Product added"}, 201

def save_product_changes(data):
    try:
        db.session.execute(
            db.update(Product)
            .where(Product.id == data['product_id'])
            .values({
                "name": data['product_name'],
                "description": data['description'],
                "condition": data['condition'],
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
        abort(400, description="Product could not be updated")
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
        abort(400, description="Product cannot be deleted")
    else:
        db.session.commit()

    return {"message": "Product deleted"}, 200
