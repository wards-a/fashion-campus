from flask_restx import Namespace, fields

from app.main.model.enum_model import ShippingMethod


class TotalPrice(fields.Raw):
    def format(self, value):
        return int(sum(e.quantity*e.price for e in value))

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

    order_list_model = orders.model("OrdersList", {
        "id": fields.String(attribute="id"),
        "user_name": fields.String(attribute="user.name"),
        "created_at": fields.DateTime(dt_format="rfc822"),
        "user_id": fields.String(attribute="user.id"),
        "user_email": fields.String(attribute="user.email"),
        "total": fields.Integer(attribute="total_price")
    })