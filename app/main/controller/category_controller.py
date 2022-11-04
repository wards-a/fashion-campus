from flask_restx import Resource

from app.main.api_model.category_am import CategoryApiModel

category_ns = CategoryApiModel.api

@category_ns.route("")
class CategoriesController(Resource):
    def get(self):
        pass

    def post(self):
        pass

@category_ns.route("/<category_id>")
class CategoryController(Resource):
    def put(self, category_id):
        pass

    def delete(self, category_id):
        pass