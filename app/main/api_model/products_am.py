import uuid
from flask import abort, url_for
from flask_restx import Namespace, fields


class UUID(fields.Raw):
    __schema_type__ = "string"
    
    def format(self, id):
        try:
            uuid.UUID(id)
            return str(id)
        except ValueError:
            abort(400, description="Invalid id")

class ProductImage(fields.Raw):
    __schema_type__ = "string"
    __schema_example__ = "/image/kaus-apolo.jpg"

    def format(self, images):
        return url_for("api.image", image_extension=images[0].image)

class ProductImagesList(fields.Raw):
    __schema_type__ = "string"

    def format(self, images):
        images_url = list()
        for i in images:
            images_url.append(url_for("api.image", image_extension=i.image))
        return images_url


class ProductsApiModel:
    api = Namespace("products")

    ### Product list expected input ###

    product_list_input = api.parser()
    product_list_input.add_argument('page', type=int, help='Page number', location='path')
    product_list_input.add_argument('page_size', help='Products per page', type=int, location='path')
    product_list_input.add_argument('sort_by', type=str, help='Sort by price asc or desc; Price a_z/Price z_a', location='path')
    product_list_input.add_argument('category', type=str, help='Filter by category id ', location='path')
    product_list_input.add_argument('price', type=str, help='Filter by price range; start,end', location='path')
    product_list_input.add_argument('condition', type=str, help='Filter by product condition; new/used', location='path')
    product_list_input.add_argument('product_name', type=str, help='Filter by product name', location='path')

    ### Product list response ###

    product_list = api.model("ProductList", {
        "id": fields.String(example='ecc0c158-2ad5-4aea-a702-b00279940417'),
        "image": ProductImage(attribute="images"),
        "title": fields.String(attribute="name", example='Kaus apolo'),
        "price": fields.Integer(example='150000')
    })

    product_list_rows = api.model("ProductListRows", {
        "data": fields.List(fields.Nested(product_list)),
        "total_rows": fields.Integer(example='1')
    })

    ### Product detail response ###

    product_detail = api.model("ProductDetail", {
        "id": fields.String,
        "title": fields.String(attribute="name"),
        "size": fields.Raw,
        "product_detail": fields.Raw(attribute="description"),
        "price": fields.Integer,
        "images_url": ProductImagesList(attribute="images")
    })

    ### Product post and put expected input ###
    product_load = api.model("ProductLoad", {
        "product_name": fields.String(required=True, example="Kaus Apolo"),
        "description": fields.String(example= "Kaus apolo dengan bahan lembut dan halus dijamin nyaman di badan anda"),
        "images": fields.String(required=True, example="[kaus-apolo-depan.jpg, kaus-apolo-samping.jpg, kaus-apolo-belakang.jpg]"),
        "condition": fields.String(required=True, example="new"),
        "category": UUID(required=True, example="c86ffcfe-5108-4f99-9c6a-52560d9c667b"),
        "price": fields.Integer(required=True, example="150000")
    })

    product_load_with_id = api.clone("ProductLoadWithId", product_load, {
        "product_id": UUID(required=True, example="ecc0c158-2ad5-4aea-a702-b00279940417")
    })
