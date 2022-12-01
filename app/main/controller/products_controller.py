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
get_products_list_response = ProductsApiModel.get_products_list_response
get_product_detail_response = ProductsApiModel.get_products_detail_response
search_by_image_response = ProductsApiModel.search_by_image_response
### validation schema ###
post_products_schema = ProductsApiModel.post_products_schema
put_products_schema = ProductsApiModel.put_products_schema
search_by_image_schema = ProductsApiModel.search_by_image_schema
### swagger only (doc) ###
get_products_list_query = ProductsApiModel.get_products_list_query # request
post_products_model = ProductsApiModel.post_products_model
put_products_model = ProductsApiModel.put_products_model
search_by_image_model = ProductsApiModel.search_by_image_model
headers = ProductsApiModel.headers

@products_ns.route("")
class ProductsController(Resource):
    @products_ns.expect(get_products_list_query)
    @products_ns.marshal_with(get_products_list_response)
    def get(self):
        headers = request.headers
        params = request.args
        return get_product_list(params, headers=headers)

    @products_ns.expect(headers, post_products_model)
    @products_ns.response(201, "Object created")
    @token_required
    @admin_level
    @validate_payload(post_products_schema)
    def post(user, self):
        data = request.json
        return save_new_product(data)
    
    @products_ns.expect(headers, put_products_model)
    @token_required
    @admin_level
    @validate_payload(put_products_schema)
    def put(user, self):
        data = request.json
        return save_product_changes(data)

@products_ns.route("/<product_id>")
@products_ns.doc(params={'product_id': 'uuid4'})
class ProductController(Resource):
    @products_ns.marshal_with(get_product_detail_response, envelope="data")
    def get(self, product_id):
        return get_product_detail(product_id)

    @products_ns.expect(headers)
    @token_required
    @admin_level
    def delete(user, self, product_id):
        return mark_as_deleted(product_id)

@products_ns.route("/search_image")
class SearchImageController(Resource):
    @products_ns.expect(search_by_image_model)
    @products_ns.marshal_with(search_by_image_response)
    @validate_payload(search_by_image_schema)
    def post(self):
        image_b64 = request.get_json('image')
        return search_by_image(image_b64)
