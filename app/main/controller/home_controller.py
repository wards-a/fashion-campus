from flask_restx import Resource

from app.main.api_model.home_am import HomeApiModel
from  app.main.service.home_service import get_all_categories


home_ns = HomeApiModel.api
home_category_model = HomeApiModel.home_category_model

@home_ns.route("/banner")
class HomeBannerController(Resource):
    def get(self):
        pass

@home_ns.route("/category")
class HomeCategoryController(Resource):
    @home_ns.marshal_list_with(home_category_model, envelope="data")
    def get(self):
        return get_all_categories()