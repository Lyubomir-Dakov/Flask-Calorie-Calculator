from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

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


def permission_required(user_role):
    def validated_func(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if not current_user.role == user_role:
                raise Forbidden("You don't have permission to access this resource!")
            return func(*args, **kwargs)

        return wrapper

    return validated_func


def validate_user_status(user_status):
    def validated_func(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if not current_user.status == user_status:
                raise Forbidden("You don't have the correct status to access this resource!")
            return func(*args, **kwargs)

        return wrapper

    return validated_func
