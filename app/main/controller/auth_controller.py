import re
from flask import request
# import library for decorator
from functools import wraps

from flask_restx import Resource

from app.main import bcrypt

from app.main.api_model.auth_am import AuthApiModel
from app.main.service.auth_service import (
    get_user_by_email,
    save_new_user
)
from app.main.utils import custom_decorator
from app.main.utils.token import generate_token


sign_up_ns = AuthApiModel.sign_up
sign_in_ns = AuthApiModel.sign_in

sign_up_schema = AuthApiModel.sign_up_schema
sign_up_model = AuthApiModel.sign_up_model

@sign_up_ns.route("")
class SignUpController(Resource):
    @sign_up_ns.expect(sign_up_model)
    def post(self):
        body = request.json
        email = body.get('email')
        password = body.get('password')
        
        if len(password) < 8: # check if password is less than 8 characters
            return {"message": "Password must contain at least 8 characters", "error": "Password must contain at least 8 characters"}, 200
        elif re.search('[a-z]',password) is None: # check if password doesn't contain any lowercase letters
            return {"message": "Password must contain a lowercase letter", "error": "Password must contain a lowercase letter"}, 200
        elif re.search('[A-Z]',password) is None: # check if password doesn't contain any uppercase letters
            return {"message": "Password must contain an uppercase letter", "error": "Password must contain an uppercase letter"}, 200
        elif re.search('[0-9]',password) is None: # check if password doesn't contain any numbers
            return {"message": "Password must contain a number", "error": "Password must contain a number"}, 200
        
        # check existing email
        user = get_user_by_email(email)
        if user:
            return {"message": f"User {email} already exists", "error": f"User {email} already exists"}, 200
        
        # if everything is valid
        return save_new_user(body)

@sign_in_ns.route("")
class SignInController(Resource):
    def post(self):
        try:
            body = request.json
            email = body.get('email')
            password = body.get('password')
            
            if not body:
                return {
                    "message": "Please provide user details",
                    "error": "Bad request"
                }, 400
            user = get_user_by_email(email)
            if user and bcrypt.check_password_hash(user.password, password):
                try:
                    payload = {'id': str(user.id)}
                    return {
                        "user_information": {
                            "name": user.name,
                            "email": user.email,
                            "phone_number": user.phone_number,
                            "type": user.type.value
                        },
                        "token": generate_token(payload),
                        "message": "Login success"
                    }
                except Exception as e:
                    return {
                        "message": "Something went wrong!",
                        "error": str(e)
                    }, 500
            return {
                "message": "Email or password is incorrect",
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e)
            }, 500