from flask_restx import Namespace


class UserApiModel:
    api = Namespace("user")
    
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
                "example": 10000
            }
        },
        "required": ["amount"]
    }

    user_balance_post_model = api.schema_model("UserBalancePostModel", user_balance_post_schema)
    