from flask_restx import Namespace


class AuthApiModel:
    sign_up = Namespace("sign-up")
    sign_in = Namespace("sign-in")
    
    ### Sign-Up post expected parameters ###
    sign_up_schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "minLength": 1,
                "errorMessage": {
                    "required": "name is required",
                    "minLength": "name is required"
                },
                "example": "John Bradley"
            },
            "email": {
                "type": "string",
                "format": "email",
                "minLength": 1,
                "errorMessage": {
                    "required": "email is required",
                    "minLength": "email is required"
                },
                "example": "john@mail.com"
            },
            "phone_number": {
                "type": "string",
                "minLength": 1,
                "errorMessage": {
                    "required": "phone_number is required",
                    "minLength": "phone_number is required"
                },
                "example": "081222333444"
            },
            "password": {
                "type": "string",
                "minLength": 8,
                "errorMessage": {
                    "required": "password is required",
                    "minLength": "password is required"
                },
                "example": "John1234"
            }
        },
        "required": ["name","email","phone_number","password"]
    }

    sign_up_model = sign_up.schema_model("AuthApiModel", sign_up_schema)
    