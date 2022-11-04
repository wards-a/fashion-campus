from flask_restx import Resource

from app.main.api_model.auth_am import AuthApiModel


sign_up_ns = AuthApiModel.sign_up
sign_in_ns = AuthApiModel.sign_in

@sign_up_ns.route("")
class SignUpController(Resource):
    def post(self):
        pass

@sign_in_ns.route("")
class SignInController(Resource):
    def post(self):
        pass