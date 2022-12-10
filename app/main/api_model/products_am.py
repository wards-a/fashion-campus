import copy

from flask import url_for
from flask_restx import Namespace, fields, reqparse

from app.main.model.product import ProductCondition


class ProductImage(fields.Raw):
    __schema_type__ = "string"

    def format(self, value):
        if value:
            return url_for("api.image", image_name_extension=value[0])
        else:
            return url_for("api.image", image_name_extension="default.jpg")

class ProductImagesList(fields.Raw):
    __schema_type__ = "string"

    def format(self, value):
        images_url = list()
        if value:
            for i in value:
                images_url.append(url_for("api.image", image_name_extension=i.image))
        else:
            images_url.append(url_for("api.image", image_name_extension="default.jpg"))
        return images_url

class SearchByImageResponse(fields.Raw):
    def format(self, value):
        return ','.join([str(e) for e in value])

class ProductsApiModel:
    api = Namespace("products")

    headers = reqparse.RequestParser()
    headers.add_argument("Authentication", required=True, location="headers", help="Jwt-Token")

    ################### REQUEST ###################
    ### Product list expected input (for swagger documentaion only) ###
    get_products_list_query = api.parser()
    products_list_query = {
        "page": {
            "type": int,
            "help": "Page number",
            "required": True
        },
        "page_size": {
            "type": int,
            "help": "Products per page",
            "required": True
        },
        "sort_by": {
            "type": str,
            "help": "Sort by price asc or desc; Price a_z/Price z_a"
        },
        "category": {
            "type": str,
            "help": "Filter by category id. Separate multiple category id with comma (,).\n" \
                    "Format id: uuid4"
        },
        "price": {
            "type": str,
            "help": "Filter by price range; start,end"
        },
        "condition": {
            "type": str,
            "help": "Filter by product condition; new/used"
        },
        "product_name": {
            "type": str,
            "help": "Filter by product name"
        }
    }

    for key, attr in products_list_query.items():
        get_products_list_query.add_argument(key, **attr)

    ### Product post and put expected input - validation and swagger doc ###
    post_products_schema = {
        "type": "object",
        "properties": {
            "product_name": {
                "type": "string",
                "minLength": 1,
                "errorMessage": {
                    "required": "Product name is required",
                    "minLength": "Product name cannot be null"
                },
                "example": "Apolo Shirt"
            },
            "description": {
                "type": ["string", "null"],
                "example": "An apolo shirt made of soft and smooth material will feel great on your body."
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
                "example": "c86ffcfe-5108-4f99-9c6a-52560d9c667b",
                "description": "category id (uuid4)"
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
            "images": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "list of encoded images (base64)"            
            }
        },
        "required": ["product_name", "condition", "category", "price"]
    }
    
    post_products_model = api.schema_model("CreateNewProducts", post_products_schema)

    ### put ###
    put_products_schema = copy.deepcopy(post_products_schema)
    put_products_schema['properties']['images'] = {
        "type": "array",
        "items": {
            "type": "string"
        },
        "description": """
            New image: base64, old image: /image/image_name.extension.
            If the old image's /image/image_name.extension is not included, the old image will be deleted.
        """
    }
    put_products_schema['properties']['product_id'] = {
        "type": "string",
        "minLength": 1,
        "errorMessage": {
            "required": "Product id is required",
            "minLength": "Product id is required"
        },
        "example": "02815e33-e4aa-4973-b4e0-22ed2e82966c"
    }
    put_products_schema['required'].append("product_id")
    put_products_model = api.schema_model("ChangeProducts", put_products_schema)

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
                "description": "base64"
            }
        },
        "required": ["image"]
    }
    search_by_image_model = api.schema_model("SearchByImagePayload", search_by_image_schema)

    ################### RESPONSE ###################
    ### Product list response marshalling ###
    list_product_detail = api.model("ProductsListData", {
        "id": fields.String(example='ecc0c158-2ad5-4aea-a702-b00279940417', description="uuid4"),
        "image": ProductImage(
            attribute="images",
            example="/image/apolo-shirt-new-01.jpg",
            description="url for endpoint image"
            ),
        "title": fields.String(attribute="name", example='Apolo Shirt'),
        "price": fields.Integer(example='150000')
    })

    get_products_list_response = api.model("ProductsList", {
        "data": fields.List(fields.Nested(list_product_detail)),
        "total_rows": fields.Integer(example='100'),
        "success": fields.Boolean(default=True),
        "message": fields.String(default="Items successfully retrieved"),
    })

    ### Product detail response marshalling ###
    get_products_detail_response = api.model("ProductsDetail", {
        "id": fields.String(example="ecc0c158-2ad5-4aea-a702-b00279940417", description="uuid4"),
        "title": fields.String(attribute="name", example="Apolo Shirt"),
        "size": fields.Raw(example=["S", "M", "L", "XL"]),
        "product_detail": fields.String(
            attribute="description",
            example="An apolo shirt made of soft and smooth material will feel great on your body."
        ),
        "price": fields.Integer(example="150000"),
        "condition": fields.String(attribute="condition.value", example="new"),
        "images_url": ProductImagesList(
            attribute="images",
            example=[
                "/image/apolo-shirt-new-01.jpg",
                "/image/apolo-shirt-new-02.jpg",
                "/image/apolo-shirt-new-03.jpg",
                "/image/apolo-shirt-new-04.jpg"
            ]
        ),
        "category_id": fields.String(example="c86ffcfe-5108-4f99-9c6a-52560d9c667b", description="uuid4"),
        "category_name": fields.String(attribute="category.name", example="Shirt")
    })

    search_by_image_response = api.model("SearchByImageResponse", {
        "category_id": SearchByImageResponse(
            example="c86ffcfe-5108-4f99-9c6a-52560d9c667b",
            description="uuid4"
        )
    })