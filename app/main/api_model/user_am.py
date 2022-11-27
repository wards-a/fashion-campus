from flask import url_for
from flask_restx import Namespace, fields


class OrderDetail(fields.Raw):
    def format(self, value):
        products = []
        for e in value:
            if e.product.images:
                image = url_for("api.image", image_extension=e.product.images[0].image)
            else:
                image = url_for("api.image", image_extension="default.jpg")
            
            details = {
                "id": str(e.product.id),
                "details": {
                    "quantity": e.quantity,
                    "size": e.size
                },
                "price": int(e.price),
                "image": image,
                "name": e.product.name
            }
            products.append(details)

        return products


class UserApiModel:
    api = Namespace("user")
    
    ### User balance post expected input ###
    user_balance_post_schema = {
        "type": "object",
        "properties": {
            "amount": {
                "type": "number",
                "minLength": 1,
                "errorMessage": {
                    "required": "amount is required",
                    "minLength": "amount cannot be null"
                },
                "example": 10000
            }
        },
        "required": ["amount"]
    }

    user_balance_post_model = api.schema_model("UserBalancePostModel", user_balance_post_schema)
    

    ### user order ###
    address = api.model("AddressUserOrder", {
        "name": fields.String,
        "phone_number": fields.String,
        "address": fields.String,
        "city": fields.String
    })

    order = api.model("UserOrder", {
        "id": fields.String,
        "created_at": fields.DateTime(dt_format='rfc822'),
        "products": OrderDetail(attribute="details"),
        "shipping_method": fields.String(attribute="shipping_method.value"),
        "shipping_address": fields.Nested(address)
    })