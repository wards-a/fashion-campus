import os
import jwt
from flask import abort, jsonify, request
from functools import wraps
from datetime import datetime, timedelta

from app.main.service.auth_service import get_user_by_id

def generate_token(payload: dict) -> str:
    # token should expire after 24 hrs
    exp_time = datetime.now() + timedelta(days=1)
    payload['exp'] = exp_time
    return jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm="HS256").decode('utf-8')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # if "Authorization" in request.headers:
        #     token = request.headers["Authorization"].split(" ")[1]
        if "Authentication" in request.headers:
            token = request.headers["Authentication"]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "error": "Unauthorized"
            }, 401
        
        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
            current_user = get_user_by_id(data['id'])
            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "error": "Unauthorized"
                }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "error": str(e)
            }, 500
        
        return f(current_user, *args, **kwargs)
    return decorated
