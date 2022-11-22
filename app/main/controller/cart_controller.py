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

@cart_ns.route("")
class CartsController(Resource):
    @token_required
    def post(user, self):
        body = request.json
        return add_cart(user.id, body)
    
    @token_required
    def get(user, self):
        return get_cart(user.id)

@cart_ns.route("/<cart_id>")
class CartController(Resource):
    @token_required
    def delete(user, sels, cart_id):
        return delete_cart(user.id, cart_id)