import json

from flask import request
from flask_restx import Resource

from app.main.api_model.products_am import ProductsApiModel
from app.main.service.products_service import (
    get_product_list,
    get_product_detail,
    save_new_product,
    save_product_changes,
    mark_as_deleted,
    search_by_image
)
from app.main.utils.custom_decorator import validate_payload, admin_level
from app.main.utils.token import token_required


products_ns = ProductsApiModel.api
### response marshaling ###
product_list_response_m = ProductsApiModel.product_list_response
product_detail_response_m = ProductsApiModel.product_detail_response
### validation schema ###
product_post_schema = ProductsApiModel.product_post_schema
product_put_schema = ProductsApiModel.product_put_schema
search_by_image_schema = ProductsApiModel.search_by_image_schema
### swagger only (doc) ###
product_list_model = ProductsApiModel.product_list_model
product_post_model = ProductsApiModel.product_post_model
product_put_model = ProductsApiModel.product_put_model
search_by_image_model = ProductsApiModel.search_by_image_model

@products_ns.route("")
class ProductsController(Resource):
    @products_ns.expect(product_list_model)
    @products_ns.marshal_with(product_list_response_m)
    def get(self):
        headers = request.headers
        params = request.args
        return get_product_list(params, headers=headers)

    @products_ns.expect(product_post_model)
    @token_required
    @admin_level
    @validate_payload(product_post_schema)
    def post(user, self):
        data = request.json
        return save_new_product(data)
    
    @products_ns.expect(product_put_model)
    @token_required
    @admin_level
    @validate_payload(product_put_schema)
    def put(user, self):
        data = request.json
        return save_product_changes(data)

@products_ns.route("/<product_id>")
class ProductController(Resource):
    @products_ns.marshal_with(product_detail_response_m, envelope="data")
    def get(self, product_id):
        return get_product_detail(product_id)

    @token_required
    @admin_level
    def delete(user, self, product_id):
        return mark_as_deleted(product_id)

@products_ns.route("/search_image")
class SearchImageController(Resource):
    @products_ns.expect(search_by_image_model)
    @validate_payload(search_by_image_schema)
    def post(self):
        image_b64 = request.get_json('image')
        return search_by_image(image_b64)
