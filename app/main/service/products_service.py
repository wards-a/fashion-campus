import re

from flask import abort

from app.main import db
from app.main.model.product import Product
from app.main.model.product_image import ProductImage
from app.main.service.image_service import check_extension


def get_product_detail(id):
    result = db.session.execute(db.select(Product).filter_by(id=id)).scalar()
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
        db.session.commit()
    except:
        db.session.rollback()
        abort(400, description="product was unable to save ")

    return {"message": "Product added"}, 201
