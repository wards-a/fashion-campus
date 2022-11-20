from flask import abort
from flask_restx import Resource

from app.main.api_model.shipping_am import ShippingApiModel
from app.main.utils.token import token_required
from app.main.service.shipping_service import (
    get_shipping_price
)


shipping_ns = ShippingApiModel.api

@shipping_ns.route("")
class ShippingController(Resource):
    @token_required
    def get(user, self):
        return get_shipping_price(user.id)