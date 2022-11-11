from flask import request

from flask_restx import Resource

from app.main.api_model.user_am import UserApiModel
from app.main.utils.token import token_required


user_ns = UserApiModel.api

@user_ns.route("")
class UsersController(Resource):
    @token_required
    def get(self):
        pass

@user_ns.route("/shipping_address")
class UserAddressController(Resource):
    def get(self):
        pass

    def post(self):
        pass

@user_ns.route("/balance")
class UserBalanceController(Resource):
    def get(self):
        pass

    def post(self):
        pass