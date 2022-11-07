import uuid

from flask import abort, request
from flask_restx import Resource

from app.main.api_model.products_am import ProductsApiModel
from app.main.service.products_service import (
    get_product_detail,
    save_new_product,
    save_product_changes,
    mark_as_deleted
)


products_ns = ProductsApiModel.api
product_detail_m = ProductsApiModel.product_detail
product_post_mv = ProductsApiModel.product_load
product_put_mv = ProductsApiModel.product_load_with_id

@products_ns.route("")
class ProductsController(Resource):
    def get(self):
        pass

    @products_ns.expect(product_post_mv, validate=True)
    def post(self):
        body = request.json
        return save_new_product(body)
    
    @products_ns.expect(product_put_mv, validate=True)
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
            abort(400, description="Invalid product")

    def delete(self, product_id):
        try:
            uuid.UUID(product_id)
            return mark_as_deleted(product_id)
        except ValueError:
            abort(400, description="Invalid product")

@products_ns.route("/search_image")
class SearchImageController(Resource):
    def post(self):
        pass