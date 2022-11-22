import re

from flask import request
from functools import wraps
from flask_restx import abort
from jsonschema import validate, exceptions


def validate_payload(schema):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            content_type = request.headers.get('Content-Type')
            if 'multipart/form-data' in content_type:
                instance = request.form
            if 'application/json' in content_type:
                instance = request.json
            try:
                validate(instance=instance, schema=schema)
            except exceptions.ValidationError as e:
                if e.validator == 'type':
                    abort(400, e.message)
                if e.validator == 'required':
                    field_key = re.findall("'(.*?)'", e.message)[0]
                    try:
                        msg = e.schema['properties'][field_key]['errorMessage'][e.validator]
                        abort(400, msg)
                    except KeyError:
                        abort(400, e.message)
                try:            
                    msg = e.schema['errorMessage'][e.validator]
                    abort(400, msg)
                except KeyError:
                    abort(400, e.message)
            return func(*args, **kwargs)
        return decorated_function
    return decorator