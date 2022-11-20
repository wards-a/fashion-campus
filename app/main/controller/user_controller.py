import json
from flask import jsonify, request

from flask_restx import Resource

from app.main.api_model.user_am import UserApiModel
from app.main.utils import validate_payload
from app.main.utils.token import token_required
from app.main.service.user_service import (
    get_user_balance,
    get_user_shipping_address,
    change_shipping_address,
    top_up_balance
)


user_ns = UserApiModel.api
user_balance_post_schema = UserApiModel.user_balance_post_schema
user_balance_post_model = UserApiModel.user_balance_post_model

@user_ns.route("")
class UsersController(Resource):
    @token_required
    def get(user, self):
        return {
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number
        }

@user_ns.route("/shipping_address")
class UserAddressController(Resource):
    @token_required
    def get(user, self):
        return get_user_shipping_address(user.id)
    
    @token_required
    def post(user, self):
        body = request.json
        return change_shipping_address(user.id, body)

@user_ns.route("/balance")
class UserBalanceController(Resource):
    @token_required
    def get(user, self):
        balance = get_user_balance(user.id)
        return {"balance": balance}
    
    @user_ns.expect(user_balance_post_model)
    @token_required
    def post(user, self):
        body = request.json
        # validate_payload(instance=body, schema=user_balance_post_schema)
        return top_up_balance(user.id, body)