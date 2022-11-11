import re

from flask_restx import abort
from jsonschema import validate, exceptions

def validate_payload(**kwargs):
    try:
        validate(**kwargs)
    except exceptions.ValidationError as e:
        if e.validator == 'type':
            abort(400, e.message)

        msg = e.schema['errorMessage'][e.validator]
        abort(400, msg)
    
