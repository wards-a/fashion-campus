import re, json

from flask import request
from functools import wraps
from flask_restx import abort
from jsonschema import validate, exceptions


def validate_payload(schema):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            content_type = request.headers.get('Content-Type')
            if 'application/json' in content_type:
                instance = request.json
            elif 'multipart/form-data' in content_type:
                instance = request.form
            elif 'text/plain' in content_type:
                data = request.get_data()
                instance = json.loads(data.decode('utf-8'))
            try:
                validate(instance=instance, schema=schema)
            except exceptions.ValidationError as e:
                if e.validator == 'type':
                    return {"message": e.message}, 400
                if e.validator == 'required':
                    field_key = re.findall("'(.*?)'", e.message)[0]
                    try:
                        msg = e.schema['properties'][field_key]['errorMessage'][e.validator]
                        return {"message": msg}, 400
                    except KeyError:
                        return {"message": e.message}, 400
                try:            
                    msg = e.schema['errorMessage'][e.validator]
                    return {"message": msg}, 400

                except KeyError:
                    return {"message": e.message}, 400
            return func(*args, **kwargs)
        return decorated_function
    return decorator


def admin_level(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = args[0]
        if user.type.value != 'seller':
            abort(403, "Access denied, you don't have permission to access the source", error="Forbidden")
        return func(*args, **kwargs)
    return decorated_function