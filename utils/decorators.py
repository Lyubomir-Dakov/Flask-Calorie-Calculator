from flask import request
from werkzeug.exceptions import BadRequest


def validate_schema(schema_name):
    def validated_func(func):
        def wrapper(*args, **kwargs):
            schema = schema_name()
            errors = schema.validate(request.get_json())
            if errors:
                raise BadRequest(errors)
            return func(*args, **kwargs)
        return wrapper
    return validated_func
