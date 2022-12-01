from flask_restx import Namespace, Resource, reqparse, fields

from app.main.utils.token import token_required
from app.main.service.shipping_service import get_shipping_price


shipping_ns = Namespace("shipping_price")

headers = reqparse.RequestParser()
headers.add_argument("Authentication", required=True, location="headers", help="Jwt-Token")

_response_data = shipping_ns.model("ShippingPriceData", {
    "name": fields.String(example="regular"),
    "price": fields.Integer(example="30000")
})

_response = shipping_ns.model("ShippingPriceResponse", {
    "status": fields.Boolean(example="True"),
    "message": fields.String(example="Success"),
    "data": fields.List(fields.Nested(_response_data))
})

@shipping_ns.route("")
class ShippingController(Resource):
    @shipping_ns.expect(headers)
    @shipping_ns.response(200, "Success", _response)
    @token_required
    def get(user, self):
        return get_shipping_price(user.id)