import json

from app.main.service.category_service import get_all_category, create_category, save_category_changes
from flask_restx import Resource
from flask import request

from app.main.api_model.category_am import CategoryApiModel
from app.main.utils.custom_decorator import validate_payload

category_ns = CategoryApiModel.api
all_category_model = CategoryApiModel.all_category_model
category_post_schema = CategoryApiModel.category_post_schema
category_post_model = CategoryApiModel.category_post_model
category_put_schema = CategoryApiModel.category_put_schema
category_put_model = CategoryApiModel.category_put_model

@category_ns.route("")
class CategoriesController(Resource):
    @category_ns.marshal_list_with(all_category_model, envelope="data")
    def get(self):
        return get_all_category()
    
    @category_ns.expect(category_post_model)
    @validate_payload(category_post_schema)
    def post(self):
        body = request.json
        return create_category(body)

@category_ns.route("/<category_id>")
class CategoryController(Resource):
    def put(self, category_id):
        data = request.get_data()
        data = json.loads(data.decode('utf-8'))
        return save_category_changes(data, str(category_id))

    def delete(self, category_id):
        pass