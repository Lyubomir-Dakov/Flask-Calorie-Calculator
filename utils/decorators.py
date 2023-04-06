from flask import request
from werkzeug.exceptions import BadRequest

from managers.auth import auth


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


def permission_required(staff):
    def validated_func(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if not current_user.role == staff:
                raise BadRequest("You don't have permission to access this resource")
            return func(*args, **kwargs)
        return wrapper
    return validated_func
