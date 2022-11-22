from app.main.service.category_service import get_all_category
from flask_restx import Resource

from app.main.api_model.category_am import CategoryApiModel

category_ns = CategoryApiModel.api
all_category_model = CategoryApiModel.all_category_model

@category_ns.route("")
class CategoriesController(Resource):
    @category_ns.marshal_list_with(all_category_model, envelope="data")
    def get(self):
        return get_all_category()
    

    def post(self):
        pass

@category_ns.route("/<category_id>")
class CategoryController(Resource):
    def put(self, category_id):
        pass

    def delete(self, category_id):
        pass