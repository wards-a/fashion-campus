from flask_restx import Namespace, fields


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

    sign_up_model = sign_up.schema_model("SignUpPayload", sign_up_schema)

    ### Sign-In post expected parameters ###
    sign_in_schema = {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "format": "email",
                "example": "john@mail.com"
            },
            "password": {
                "type": "string",
                "example": "John1234"
            }
        },
        "required": ["email", "password"]
    }
    sign_in_model = sign_in.schema_model("SignInPayload", sign_in_schema)

    ### Sign In Response Model ###
    user_information_model = sign_in.model("UserInformation", {
        "name": fields.String(example="John Bradley"),
        "email": fields.String(example="john@mail.com"),
        "phone_number": fields.String(example="081222333444"),
        "type": fields.String(example="buyer")
    })
    sign_in_response = sign_in.model("SignInResponse", {
        "user_information": fields.Nested(user_information_model),
        "token": fields.String(description="jwt-token"),
        "message": fields.String(default="Login success")
    })