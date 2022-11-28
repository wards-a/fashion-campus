import json

from app.main.service.category_service import get_all_category, create_category, save_category_changes, mark_as_deleted
from flask_restx import Resource
from flask import request

from app.main.api_model.category_am import CategoryApiModel
from app.main.utils.custom_decorator import validate_payload
from app.main.utils.custom_decorator import validate_payload, admin_level
from app.main.utils.token import token_required


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
        return get_all_category(request.headers)
    
    @category_ns.expect(category_post_model)
    @token_required
    @admin_level
    @validate_payload(category_post_schema)
    def post(user, self):
        data = request.get_data()
        data = json.loads(data.decode('utf-8'))
        return create_category(data)

@category_ns.route("/<category_id>")
class CategoryController(Resource):
    @token_required
    @admin_level
    def put(user, self, category_id):
        data = request.get_data()
        data = json.loads(data.decode('utf-8'))
        return save_category_changes(data, str(category_id))
    
    @token_required
    @admin_level
    def delete(user, self, category_id):
        return mark_as_deleted(category_id)
    