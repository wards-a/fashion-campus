from flask_restx import Resource

from app.main.api_model.order_am import OrderApiModel


order_ns = OrderApiModel.order
orders_ns = OrderApiModel.orders

@order_ns.route("")
class OrderController(Resource):
    def get(self):
        pass

    def post(self):
        pass

@orders_ns.route("")
class OrdersController(Resource):
    def get(self):
        pass