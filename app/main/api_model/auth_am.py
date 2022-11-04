from flask_restx import Namespace


class AuthApiModel:
    sign_up = Namespace("sign-up")
    sign_in = Namespace("sign-in")