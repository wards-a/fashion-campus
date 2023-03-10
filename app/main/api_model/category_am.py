import copy

from flask_restx import Namespace, fields, reqparse


class CategoryApiModel:
    api = Namespace("categories")

    headers = reqparse.RequestParser()
    headers.add_argument("Authentication", required=True, location="headers", help="Jwt-Token")

    all_category_model = api.model("AllCategory", {
        "id": fields.String(example="c86ffcfe-5108-4f99-9c6a-52560d9c667b", description="uuid4"),
        "title": fields.String(attribute="name", example="Shirt")
    })

    category_post_schema = {
        "type": "object",
        "properties": {
            "category_name": {
                "type": "string",
                "minLength": 1,
                "errorMessage": {
                    "required": "category_name is required",
                    "minLength": "category cannot be null"
                },
                "example": "Shirt"
            }
        },
        "required": ["category_name"]
    }
    category_post_model = api.schema_model("CategoryPostModel", category_post_schema) 


    category_put_schema = copy.deepcopy(category_post_schema)
    category_put_schema['properties']['category_id'] = {
        "type": "string",
        "minLength": 1,
        "errorMessage": {
            "required": "Category id is required",
            "minLength": "Category id is required"
        },
        "example": "c86ffcfe-5108-4f99-9c6a-52560d9c667d"
    }
    category_put_schema['required'] = ["category_name","category_id"]
    category_put_model = api.schema_model("CategoryPutModel", category_put_schema)

