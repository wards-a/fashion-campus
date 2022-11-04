from flask_restx import Namespace


class OrderApiModel:
    order = Namespace("order")
    orders = Namespace("orders")