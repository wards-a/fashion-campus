from flask_restx import Resource

from app.main.api_model.shipping_am import ShippingApiModel


shipping_ns = ShippingApiModel.api

@shipping_ns.route("")
class ShippingController(Resource):
    def get(self):
        pass