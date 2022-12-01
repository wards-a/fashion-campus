from flask import request
from flask_restx import Resource

from app.main.api_model.order_am import OrderApiModel
from app.main.utils.token import token_required
from app.main.utils.custom_decorator import validate_payload, admin_level
from app.main.service.order_service import create_order, get_all_orders


order_ns = OrderApiModel.order
orders_ns = OrderApiModel.orders

order_post_schema = OrderApiModel.order_post_schema
order_post_model = OrderApiModel.order_post_model
order_list_model = OrderApiModel.order_list_model
headers = OrderApiModel.headers

@order_ns.route("")
class OrderController(Resource):
    @order_ns.expect(headers, order_post_model)
    @token_required
    @validate_payload(order_post_schema)
    def post(user, self):
        data = request.json
        return create_order(data, user.id)

@orders_ns.route("")
class OrdersController(Resource):
    @orders_ns.expect(headers)
    @orders_ns.marshal_list_with(order_list_model, envelope="data")
    @token_required
    @admin_level
    def get(user, self):
        return get_all_orders()
