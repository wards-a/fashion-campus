from flask_restx import Resource

from app.main.api_model.cart_am import CartApiModel


cart_ns = CartApiModel.api

@cart_ns.route("")
class CartsController(Resource):
    def post(self):
        pass

    def get(self):
        pass

@cart_ns.route("/<cart_id>")
class CartController(Resource):
    def delete(sels, cart_id):
        pass