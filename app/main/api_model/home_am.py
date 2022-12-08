from flask import url_for
from flask_restx import Namespace, fields, reqparse


class BannerImage(fields.Raw):
    __schema_type__ = "string"

    def format(self, value):
        if value:
            return url_for("api.image", image_name_extension=value)
        else:
            return url_for("api.image", image_name_extension="default.jpg")

class CategoryImage(fields.Raw):
    __schema_type__ = "string"

    def format(self, value):
        if value:
            return url_for("api.image", image_name_extension=value)
        else:
            return url_for("api.image", image_name_extension="default.jpg")


class HomeApiModel:
    api = Namespace("home")

    headers = reqparse.RequestParser()
    headers.add_argument("Authentication", required=True, location="headers", help="Jwt-Token")

    home_category_model = api.model("HomeCategory", {
        "id": fields.String(description="uuid4"),
        "title": fields.String(attribute="name"),
        "image": CategoryImage(example="/image/kaus-apolo-new-01.jpg")
    })

    home_banner_model = api.clone("HomeBanner", home_category_model, {
        "title": fields.String(example="Winter sale banner"),
        "image": BannerImage(example="/image/winter-sale-banner.jpg")
    })

    post_banner_schema = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "minLength": 1,
                "errorMessage": {
                    "required": "Title is required",
                    "minLength": "Title cannot be null"
                },
                "example": "Special offer"
            },
            "image": {
                "type": "string",
                "minLength": 1,
                "errorMessage": {
                    "required": "Image is required",
                    "minLength": "Image is required"
                },
                "example": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEBLAEsAAD/7gAOQWRvYmUAZAAAAAAA/+EQ3EV4aWYAAE1NACoAAAAIAAQBOwACAAAABgAACEqHaQAEAAAAAQAACFCcnQABAAAADAAAEMjqHAAAAv8Antd/99r/APE0Uf8ACNWf/PW4/wC+l/",
                "description": "base64"
            }
        },
        "required": ["title", "image"]
    }

    post_banner_model = api.schema_model("AddBanner", post_banner_schema)