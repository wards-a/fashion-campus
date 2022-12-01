from flask import request

from flask_restx import Resource

from app.main.api_model.user_am import UserApiModel
from app.main.utils.token import token_required
from app.main.service.user_service import (
    get_user_balance,
    get_user_shipping_address,
    change_shipping_address,
    top_up_balance,
    get_user_order
)


user_ns = UserApiModel.api

headers = UserApiModel.headers
get_user_response = UserApiModel.get_user_response
get_shipping_address_response = UserApiModel.get_shipping_address_response
post_shipping_address_payload = UserApiModel.post_shipping_address_payload
user_balance_post_schema = UserApiModel.user_balance_post_schema
user_balance_post_model = UserApiModel.user_balance_post_model
post_balance_response = UserApiModel.post_balance_response
user_order_model = UserApiModel.order

@user_ns.route("")
class UsersController(Resource):
    @user_ns.expect(headers)
    @user_ns.response(200, "Success", get_user_response)
    @token_required
    def get(user, self):
        return {
            "success": True,
            "message": "Success",
            "data": {
                "name": user.name,
                "email": user.email,
                "phone_number": user.phone_number
            }
        }

@user_ns.route("/shipping_address")
class UserAddressController(Resource):
    @user_ns.expect(headers)
    @user_ns.response(200, "Success", get_shipping_address_response)
    @token_required
    def get(user, self):
        return get_user_shipping_address(user.id)
    
    @user_ns.expect(headers, post_shipping_address_payload)
    @token_required
    def post(user, self):
        body = request.json
        return change_shipping_address(user.id, body)

@user_ns.route("/balance")
class UserBalanceController(Resource):
    @user_ns.expect(headers)
    @token_required
    def get(user, self):
        return get_user_balance(user.id)
    
    @user_ns.expect(headers, user_balance_post_model)
    @user_ns.response(200, "Success", post_balance_response)
    @token_required
    def post(user, self):
        body = request.json
        return top_up_balance(user.id, body)

@user_ns.route("/order")
class UserOrderController(Resource):
    @user_ns.expect(headers)
    @user_ns.marshal_list_with(user_order_model, envelope="data")
    @token_required
    def get(user, self):
        return get_user_order(user.id)