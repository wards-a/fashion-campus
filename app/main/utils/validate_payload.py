import re

from flask_restx import abort
from jsonschema import validate, exceptions


def validate_payload(**kwargs):
    try:
        validate(**kwargs)
    except exceptions.ValidationError as e:
        if e.validator == 'type':
            abort(400, e.message)
        if e.validator == 'required':
            field_key = re.findall(r"\'(.*?)\'", e.message)[0]
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
    