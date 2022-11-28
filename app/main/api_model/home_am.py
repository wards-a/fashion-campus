from flask import url_for
from flask_restx import Namespace, fields

from app.main.api_model.products_am import ProductImage


class BannerImage(fields.Raw):
    __schema_type__ = "string"

    def format(self, value):
        if value:
            return url_for("api.image", image_extension=value[0].image)
        else:
            return url_for("api.image", image_extension="defaultbanner.jpg")


class HomeApiModel:
    api = Namespace("home")

    home_category_model = api.model("HomeCategory", {
        "id": fields.String(),
        "title": fields.String(attribute="name"),
        "image": BannerImage(attribute='images')
    })

    home_banner_model = api.clone("HomeBanner", home_category_model, {
        "image": ProductImage(attribute='images')
    })