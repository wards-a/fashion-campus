from flask_restx import Namespace

from app.main.model.enum_model import ShippingMethod


class OrderApiModel:
    order = Namespace("order")
    orders = Namespace("orders")

    order_post_schema = {
        "type": "object",
        "properties": {
            "shipping_method": {
                "type": "string",
                "enum": [e.value for e in ShippingMethod],
                "errorMessage":{
                    "required": "Shipping method is required",
                    "enum": "Shipping method is invalid, shipping method must be regular or next day"
                }
            },
            "shipping_address": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "phone_number": {"type": "string"},
                    "city": {"type": "string"},
                    "address": {"type": "string"}
                },
                "required": ["name", "phone_number", "city", "address"]
            }
        },
        "required": ["shipping_method", "shipping_address"],
    }

    order_post_model = order.schema_model("Order", order_post_schema)