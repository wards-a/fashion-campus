from flask import url_for
from flask_restx import Namespace, fields


class CategoryImage(fields.Raw):
    __schema_type__ = "string"

    def format(self, value):
        return url_for("api.image", image_extension=value)

class HomeApiModel:
    api = Namespace("home")

    all_category_model = api.model("AllCategory", {
        "id": fields.String(),
        "image": CategoryImage(),
        "title": fields.String(attribute="name")
    })