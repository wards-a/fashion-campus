from flask import request
from flask_restx import Resource

from app.main.api_model.home_am import HomeApiModel
from app.main.service.home_service import (
    get_home_categories,
    get_banner,
    save_new_banner,
    delete_banner
)
from app.main.utils.token import token_required
from app.main.utils.custom_decorator import validate_payload, admin_level


home_ns = HomeApiModel.api
headers = HomeApiModel.headers
home_category_model = HomeApiModel.home_category_model
home_banner_model = HomeApiModel.home_banner_model
post_banner_schema = HomeApiModel.post_banner_schema
post_banner_model = HomeApiModel.post_banner_model

@home_ns.route("/banner")
class HomeBannerController(Resource):
    @home_ns.marshal_list_with(home_banner_model, envelope="data")
    def get(self):
        return get_banner()

    @home_ns.expect(headers, post_banner_model)
    @home_ns.response(201, "Object created")
    @token_required
    @admin_level
    @validate_payload(post_banner_schema)
    def post(user, self):
        data = request.json
        return save_new_banner(data)
    
@home_ns.route("/banner/<banner_id>")
@home_ns.doc(params={'banner_id': 'uuid4'})
class HomeBannerController(Resource):
    @home_ns.expect(headers)
    @token_required
    @admin_level
    def delete(user, self, banner_id):
        return delete_banner(banner_id)

@home_ns.route("/category")
class HomeCategoryController(Resource):
    @home_ns.marshal_list_with(home_category_model, envelope="data")
    def get(self):
        return get_home_categories()