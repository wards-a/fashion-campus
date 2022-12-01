from flask_restx import Namespace, reqparse, fields


class CartApiModel:
    api = Namespace("cart")

    headers = reqparse.RequestParser()
    headers.add_argument("Authentication", required=True, location="headers", help="Jwt-Token")

    ### swagger doc ###
    post_cart_model = api.model("AddItemToCart", {
        "id": fields.String(example="02815e33-e4aa-4973-b4e0-22ed2e82966c", description="product_id (uuid)")
    })