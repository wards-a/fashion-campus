from flask import request
from flask_restx import Resource

from app.main.api_model.cart_am import CartApiModel
from app.main.utils.token import token_required
from app.main.service.cart_service import (
    get_cart,
    add_cart,
    delete_cart
)


cart_ns = CartApiModel.api

headers = CartApiModel.headers
post_cart_model = CartApiModel.post_cart_model

@cart_ns.route("")
class CartsController(Resource):
    @cart_ns.expect(headers, post_cart_model)
    @token_required
    def post(user, self):
        body = request.json
        return add_cart(user.id, body)
    
    @cart_ns.expect(headers)
    @token_required
    def get(user, self):
        return get_cart(user.id)

@cart_ns.route("/<cart_id>")
@cart_ns.expect(headers)
@cart_ns.doc(params={'cart_id': 'Cart details uuid'})
class CartController(Resource):
    @token_required
    def delete(user, sels, cart_id):
        return delete_cart(user.id, cart_id)