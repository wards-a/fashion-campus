from flask import url_for
from flask_restx import Namespace, fields, reqparse


class OrderDetail(fields.Raw):
    def format(self, value):
        products = []
        for e in value:
            if e.product.images:
                image = url_for("api.image", image_name_extension=e.product.images[0].image)
            else:
                image = url_for("api.image", image_name_extension="default.jpg")
            
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

    headers = reqparse.RequestParser()
    headers.add_argument("Authentication", required=True, location="headers", help="Jwt-Token")
    
    ### GET /user response example ###
    get_user_data = api.model("UserDataDetail", {
        "name": fields.String(example="John Bradley"),
        "email": fields.String(example="john@mail.com"),
        "phone_number": fields.String(example="081222333444")
    })
    get_user_response = api.model("UserDataResponse", {
        "status": fields.Boolean(example="True"),
        "message": fields.String(example="Success"),
        "data": fields.Nested(get_user_data)
    })

    ### GET /user/shipping_address
    user_shipping_address_data = api.model('UserShippingAddressDetail', {
        "id": fields.String(example="a14fc9c3-2896-4df6-8726-3dfde7f7afab", description="uuid"),
        "name": fields.String(example="Home"),
        "phone_number": fields.String(example="081222333444"),
        "address": fields.String(example="Route 66"),
        "city": fields.String(example="Chicago")
    })
    get_shipping_address_response = api.model('UserShippingAddressResponse', {
        "status": fields.Boolean(example="True"),
        "message": fields.String(example="Success"),
        "data": fields.Nested(user_shipping_address_data)
    })

    ### POST /user/shipping_address ###
    post_shipping_address_payload = api.model('SaveShippingAddress', {
        "name": fields.String(example="Home"),
        "phone_number": fields.String(example="081222333444"),
        "address": fields.String(example="Route 66"),
        "city": fields.String(example="Chicago")
    })

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
                "example": 200000
            }
        },
        "required": ["amount"]
    }

    user_balance_post_model = api.schema_model("UserBalancePostModel", user_balance_post_schema)

    ### POST /user/balance response example ###
    balance_amount_response = api.model("BalanceAmount", {
        "balance": fields.Integer(example="200000")
    })
    post_balance_response = api.model("TopUpBalanceResponse", {
        "status": fields.Boolean(example="True"),
        "message": fields.String(example="Top Up balance success"),
        "data": fields.Nested(balance_amount_response)
    })

    ### user order ###
    address = api.model("AddressUserOrder", {
        "name": fields.String(example="Home"),
        "phone_number": fields.String(example="081222333444"),
        "address": fields.String(example="Route 66"),
        "city": fields.String(example="Chicago")
    })

    order = api.model("UserOrder", {
        "id": fields.String(example="755d2f4c-1217-4a2b-978e-bd2c872b3f2b", description="uuid4"),
        "created_at": fields.DateTime(
            dt_format='rfc822',
            example="Wed, 09 Nov 2022 08:27:46 -0000",
            description="Date Format: RFC822"
        ),
        "products": OrderDetail(
            attribute="details",
            example={
                "id": "ecc0c158-2ad5-4aea-a702-b00279940417",
                "details": {
                    "quantity": 1,
                    "size": "L"
                },
                "price": 150000,
                "image": "/image/apolo-shirt-new-01.jpg",
                "name": "Apolo Shirt"
            }
        ),
        "shipping_method": fields.String(attribute="shipping_method.value", example="regular"),
        "shipping_address": fields.Nested(address)
    })