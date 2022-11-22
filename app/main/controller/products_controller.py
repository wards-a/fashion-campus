import uuid

from flask import request
from flask_restx import Resource, abort

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
        params = request.args
        return get_product_list(params)

    @products_ns.expect(product_post_model)
    @token_required
    @admin_level
    @validate_payload(product_post_schema)
    def post(user, self):
        data = request.form
        images = request.files
        print(request.form)
        print(request.json)
        return save_new_product(data, files=images)
    
    @products_ns.expect(product_put_model)
    @token_required
    def put(self):
        try:
            body = request.json
        except:
            abort(400, "Request data invalid")
        validate_payload(instance=body, schema=product_put_schema)
        return save_product_changes(body)

@products_ns.route("/<product_id>")
class ProductController(Resource):
    @products_ns.marshal_with(product_detail_response_m, envelope="data")
    def get(self, product_id):
        return get_product_detail(product_id)

    @token_required
    def delete(self, product_id):
        try:
            uuid.UUID(product_id)
            return mark_as_deleted(product_id)
        except ValueError:
            abort(400, "Invalid product id")

@products_ns.route("/search_image")
class SearchImageController(Resource):
    @products_ns.expect(search_by_image_model)
    def post(self):
        try:
            image_b64 = request.get_json('image')
        except:
            abort(400, "Request data invalid")
        validate_payload(instance=image_b64, schema=search_by_image_schema)
        return search_by_image(image_b64)
