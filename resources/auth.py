from flask import request
from flask_restful import Resource

from managers.user import UserManager
from schemas.request.user import RequestUserRegisterSchema, RequestUserLoginSchema
from utils.decorators import validate_schema


class RegisterUserResource(Resource):
    @validate_schema(RequestUserRegisterSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.register(data)
        return {"token": token}, 201


class LoginUserResource(Resource):
    @validate_schema(RequestUserLoginSchema)
    def post(self):
        data = request.get_json()
        token, user_role = UserManager.login(data)
        return {"token": token, "role": user_role}
