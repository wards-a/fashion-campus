import uuid, copy
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

    def format(self, value):
        return url_for("api.image", image_extension=value[0].image)

class ProductImagesList(fields.Raw):
    __schema_type__ = "string"

    def format(self, value):
        images_url = list()
        for i in value:
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

    product_list_format = api.model("ProductList", {
        "id": fields.String(example='ecc0c158-2ad5-4aea-a702-b00279940417'),
        "image": ProductImage(attribute="images", example="/image/kaus-apolo.jpg"),
        "title": fields.String(attribute="name", example='Kaus apolo'),
        "price": fields.Integer(example='150000')
    })

    product_list_response = api.model("ProductListResponse", {
        "data": fields.List(fields.Nested(product_list_format)),
        "total_rows": fields.Integer(example='1'),
        "success": fields.Boolean(default=True),
        "message": fields.String(default="Items successfully retrieved"),
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
    product_post_schema = {
        "type": "object",
        "properties": {
            "product_name": {
                "type": "string",
                "minLength": 1,
                "errorMessage": {
                    "required": "Product name is required",
                    "minLength": "Product name cannot be null"
                },
                "example": "Kaus Apolo"
            },
            "description": {
                "type": "string",
                "example": "Kaus apolo dengan bahan lembut dan halus dijamin nyaman di badan anda"
            },
            "images": {
                "type": "string",
                "minLength": 1,
                "errorMessage": {
                    "required": "Image is required",
                    "minLength": "Image is required"
                },
                "example": "[kaus-apolo-depan.jpg, kaus-apolo-samping.jpg, kaus-apolo-belakang.jpg]"
            },
            "condition": {
                "type": "string",
                "minLength": 1,
                "errorMessage": {
                    "required": "Condition is required",
                    "minLength": "Condition cannot be null"
                },
                "example": "new"
            },
            "category": {
                "type": "string",
                "minLength": 1,
                "errorMessage": {
                    "required": "Category is required",
                    "minLength": "Category is required"
                },
                "example": "c86ffcfe-5108-4f99-9c6a-52560d9c667b"
            },
            "price": {
                "type": "number",
                "minimum": 1,
                "errorMessage": {
                    "required": "Price is required",
                    "minimum": "Price must be positive"
                },
                "example": 150000
            }
        },
        "required": ["product_name", "images", "condition", "category", "price"]
    }

    product_post_model = api.schema_model("ProductPostModel", product_post_schema)
    
    product_put_schema = copy.deepcopy(product_post_schema)
    product_put_schema['properties']['product_id'] = {
        "type": "string",
        "minLength": 1,
        "errorMessage": {
            "required": "Product id is required",
            "minLength": "Product id is required"
        },
        "example": "02815e33-e4aa-4973-b4e0-22ed2e82966c"
    }
    product_put_schema['required'] = ["product_name", "images", "condition", "category", "price", "product_id"]
    product_put_model = api.schema_model("ProductPutModel", product_put_schema)
