from flask_restx import Namespace, fields


class CategoryApiModel:
    api = Namespace("categories")

    all_category_model = api.model("AllCategory", {
        "id": fields.String(),
        "title": fields.String(attribute="name")
    })