from flask_restx import Resource

from app.main.api_model.home_am import HomeApiModel


home_ns = HomeApiModel.api

@home_ns.route("/banner")
class HomeBannerController(Resource):
    def get(self):
        pass

@home_ns.route("/category")
class HomeCategoryController(Resource):
    def get(self):
        pass