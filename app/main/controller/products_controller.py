import uuid

from flask import abort, request
from flask_restx import Resource

from app.main.api_model.products_am import ProductsApiModel
from app.main.service.products_service import (
    get_product_list,
    get_product_detail,
    save_new_product,
    save_product_changes,
    mark_as_deleted
)
from app.main.utils.validate_payload import validate_payload


products_ns = ProductsApiModel.api
product_list_input = ProductsApiModel.product_list_input
product_list_response_m = ProductsApiModel.product_list_response
product_detail_m = ProductsApiModel.product_detail
product_post_schema = ProductsApiModel.product_post_schema
product_post_model = ProductsApiModel.product_post_model
product_put_model = ProductsApiModel.product_put_model

@products_ns.route("")
class ProductsController(Resource):
    @products_ns.marshal_with(product_list_response_m)
    @products_ns.expect(product_list_input)
    def get(self):
        params = request.args
        return get_product_list(params)

    @products_ns.expect(product_post_model)
    def post(self):
        body = request.json
        validate_payload(instance=body, schema=product_post_schema)
        return save_new_product(body)
    
    @products_ns.expect(product_put_model)
    def put(self):
        body = request.json
        return save_product_changes(body)

@products_ns.route("/<product_id>")
class ProductController(Resource):
    @products_ns.marshal_with(product_detail_m, envelope="data")
    def get(self, product_id):
        try:
            uuid.UUID(product_id)
            return get_product_detail(product_id)
        except ValueError:
            abort(400, "Invalid product id")

    def delete(self, product_id):
        try:
            uuid.UUID(product_id)
            return mark_as_deleted(product_id)
        except ValueError:
            abort(400, "Invalid product id")

@products_ns.route("/search_image")
class SearchImageController(Resource):
    def post(self):
        pass
