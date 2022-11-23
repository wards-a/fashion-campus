import copy

from flask import url_for
from flask_restx import Namespace, fields

from app.main.model.product import ProductCondition


class ProductImage(fields.Raw):
    __schema_type__ = "string"

    def format(self, value):
        if value:
            return url_for("api.image", image_extension=value[0].image)
        else:
            return url_for("api.image", image_extension="default.jpg")

class ProductImagesList(fields.Raw):
    __schema_type__ = "string"

    def format(self, value):
        images_url = list()
        if value:
            for i in value:
                images_url.append(url_for("api.image", image_extension=i.image))
        else:
            images_url.append(url_for("api.image", image_extension="default.jpg"))
        return images_url


class ProductsApiModel:
    api = Namespace("products")

    ### Product list expected input (for swagger documentaion only) ###
    product_list_model = api.parser()
    product_list_m_dict = {
        "page": {
            "type": int,
            "help": "Page number",
            "location": "path"
        },
        "page_size": {
            "type": int,
            "help": "Products per page",
            "location": "path"
        },
        "sort_by": {
            "type": str,
            "help": "Sort by price asc or desc; Price a_z/Price z_a",
            "location": "path"
        },
        "category": {
            "type": str,
            "help": "Filter by category id",
            "location": "path"
        },
        "harga": { # price
            "type": str,
            "help": "Filter by price range; start,end",
            "location": "path"
        },
        "kondisi": { # condition
            "type": str,
            "help": "Filter by product condition; new/used",
            "location": "path"
        },
        "product_name": {
            "type": str,
            "help": "Filter by product name",
            "location": "path"
        }
    }

    for field, attr in product_list_m_dict.items():
        product_list_model.add_argument(field, **attr)

    ### Product list response marshalling ###
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

    ### Product detail response marshalling ###
    product_detail_response = api.model("ProductDetail", {
        "id": fields.String,
        "title": fields.String(attribute="name"),
        "size": fields.Raw,
        "product_detail": fields.Raw(attribute="description"),
        "price": fields.Integer,
        "condition": fields.String,
        "images_url": ProductImagesList(attribute="images"),
        "category_id": fields.String,
        "category_name": fields.String(attribute="category.name")
    })

    ### Product post and put expected input - validation and swagger doc ###
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
                "type": ["string", "null"],
                "example": "Kaus apolo dengan bahan lembut dan halus dijamin nyaman di badan anda"
            },
            "condition": {
                "type": "string",
                "minLength": 1,
                "enum": [e.value for e in ProductCondition],
                "errorMessage": {
                    "required": "Condition is required",
                    "minLength": "Condition cannot be null",
                    "enum": "Condition is invalid, condition must be new or used"
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
                "type": "integer",
                "minimum": 1,
                "errorMessage": {
                    "required": "Price is required",
                    "minimum": "Price must be positive"
                },
                "example": 150000
            },
            "image": {
                "type": "string"                
            }
        },
        "required": ["product_name", "condition", "category", "price"]
    }
    product_post_model = api.schema_model("ProductPostModel", product_post_schema)

    ### put ###
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
    product_put_schema['required'] = ["product_name", "condition", "category", "price", "product_id"]
    product_put_model = api.schema_model("ProductPutModel", product_put_schema)

    ###### Search by image ######
    search_by_image_schema = {
        "type": "object",
        "properties": {
            "image": {
                "type": "string",
                "minLength": 1,
                "errorMessage": {
                    "required": "Image is required",
                    "minLength": "Image is required"
                },
                "example": "base64 string"
            }
        },
        "required": ["image"]
    }
    search_by_image_model = api.schema_model("SearchByImage", search_by_image_schema)