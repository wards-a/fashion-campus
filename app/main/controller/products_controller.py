import uuid

from flask import abort, request
from flask_restx import Resource

from app.main.api_model.products_am import ProductsApiModel
from app.main.service.products_service import (
    get_product_detail,
    save_new_product
)


products_ns = ProductsApiModel.api
product_detail_m = ProductsApiModel.product_detail
product_load_mv = ProductsApiModel.product_load

@products_ns.route("")
class ProductsController(Resource):
    def get(self):
        pass

    @products_ns.expect(product_load_mv, validate=True)
    def post(self):
        body = request.json
        return save_new_product(body)

@products_ns.route("/<product_id>")
class ProductController(Resource):
    @products_ns.marshal_with(product_detail_m, envelope="data")
    def get(self, product_id):
        try:
            uuid.UUID(product_id)
            product = get_product_detail(product_id)
            return product
        except ValueError:
            abort(400, description="invalid id")
    
    def put(self, product_id):
        pass
        # body = request.json
        # return save_products(body)

    def delete(self, product_id):
        pass

@products_ns.route("/search_image")
class SearchImageController(Resource):
    def post(self):
        pass