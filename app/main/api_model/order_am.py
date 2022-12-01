from flask_restx import Namespace, fields, reqparse

from app.main.model.enum_model import ShippingMethod


class TotalPrice(fields.Raw):
    def format(self, value):
        return int(sum(e.quantity*e.price for e in value))

class OrderApiModel:
    order = Namespace("order")
    orders = Namespace("orders")

    headers = reqparse.RequestParser()
    headers.add_argument("Authentication", required=True, location="headers", help="Jwt-Token")

    order_post_schema = {
        "type": "object",
        "properties": {
            "shipping_method": {
                "type": "string",
                "enum": [e.value for e in ShippingMethod],
                "errorMessage":{
                    "required": "Shipping method is required",
                    "enum": "Shipping method is invalid, shipping method must be regular or next day"
                },
                "example": "regular"
            },
            "shipping_address": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "example": "Home"
                    },
                    "phone_number": {
                        "type": "string",
                        "example": "081222333444"
                    },
                    "address": {
                        "type": "string",
                        "example": "Route 66"
                    },
                    "city": {
                        "type": "string",
                        "example": "Chicago"
                    }
                },
                "required": ["name", "phone_number", "city", "address"]
            }
        },
        "required": ["shipping_method", "shipping_address"],
    }

    order_post_model = order.schema_model("Order", order_post_schema)

    order_list_model = orders.model("OrdersList", {
        "id": fields.String(
            attribute="id",
            example="755d2f4c-1217-4a2b-978e-bd2c872b3f2b",
            description="uuid4"
        ),
        "user_name": fields.String(attribute="user.name", example="John Bradley"),
        "created_at": fields.DateTime(
            dt_format="rfc822",
            example="Wed, 09 Nov 2022 08:27:46 -0000",
            description="Date Format: RFC822"
        ),
        "user_id": fields.String(
            attribute="user.id", 
            example="f35ea1b2-22d3-40b9-972a-58e85919671f",
            description="uuid4"
        ),
        "user_email": fields.String(attribute="user.email", example="john@mail.com"),
        "total": fields.Integer(attribute="total_price", example='180000')
    })