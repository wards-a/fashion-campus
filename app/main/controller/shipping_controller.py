from flask import abort
from flask_restx import Namespace, Resource

from app.main.utils.token import token_required
from app.main.service.shipping_service import (
    get_shipping_price
)


shipping_ns = Namespace("shipping_price")

@shipping_ns.route("")
class ShippingController(Resource):
    @token_required
    def get(user, self):
        return get_shipping_price(user.id)