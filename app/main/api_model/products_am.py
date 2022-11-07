import uuid
from flask import abort, url_for
from flask_restx import Namespace, fields

from app.main.model.product import ProductCondition


class UUID(fields.Raw):
    __schema_type__ = "string"
    
    def format(self, id):
        try:
            uuid.UUID(id)
            return str(id)
        except ValueError:
            abort(400, description="Invalid id")

class ImagesValidation(fields.Raw):
    __schema_type__ = "string"
    pass


class ProductImagesList(fields.Raw):
    def format(self, images):
        images_url = list()
        for i in images:
            images_url.append(url_for("api.image", image_extension=i.image))
        return images_url


class ProductsApiModel:
    api = Namespace("products")
    product_detail = api.model("Product", {
        "id": fields.String(),
        "title": fields.String(attribute="name"),
        "size": fields.Raw(),
        "product_detail": fields.Raw(attribute="description"),
        "price": fields.Integer(),
        "images_url": ProductImagesList(attribute="images")
    })
    product_load = api.model("Product", {
        "product_name": fields.String(required=True),
        "description": fields.String(required=True),
        "images": ImagesValidation(required=True),
        "condition": fields.String(required=True),
        "category": UUID(required=True),
        "price": fields.Integer(required=True, min=1)
    })
    product_load_with_id = api.model("Product", {
        "product_name": fields.String(required=True),
        "description": fields.String(required=True),
        "images": ImagesValidation(required=True),
        "condition": fields.String(required=True),
        "category": UUID(required=True),
        "price": fields.Integer(required=True, min=1),
        "product_id": UUID(required=True)
    })
    # product_load =
