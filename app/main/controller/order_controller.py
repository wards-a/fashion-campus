from flask import request
from flask_restx import Resource

from app.main.api_model.order_am import OrderApiModel
from app.main.utils.token import token_required
from app.main.utils.custom_decorator import validate_payload
from app.main.service.order_service import create_order


order_ns = OrderApiModel.order
orders_ns = OrderApiModel.orders

order_post_schema = OrderApiModel.order_post_schema
order_post_model = OrderApiModel.order_post_model

@order_ns.route("")
class OrderController(Resource):
    @order_ns.expect(order_post_model)
    @token_required
    @validate_payload(order_post_schema)
    def post(user, self):
        data = request.json
        return create_order(data, user.id)

@orders_ns.route("")
class OrdersController(Resource):
    def get(self):
        pass