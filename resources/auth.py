from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from managers.auth import auth
from managers.user import UserManager
from models import RoleType
from schemas.request.user import RequestUserRegisterSchema, RequestUserLoginSchema, RequestUserUpdateSchema
from schemas.response.user import ResponseUserRegisterSchema, ResponseUserLoginSchema, ResponseUserUpdateSchema, \
    ResponseUserDeleteSchema
from utils.decorators import validate_schema, permission_required


class RegisterUserResource(Resource):
    @validate_schema(RequestUserRegisterSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.register(data)
        return ResponseUserRegisterSchema().dump({"token": token}), 201


class LoginUserResource(Resource):
    @validate_schema(RequestUserLoginSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.login(data)
        return ResponseUserLoginSchema().dump({"token": token})


class UpdateUserResource(Resource):
    @auth.login_required
    @validate_schema(RequestUserUpdateSchema)
    def put(self, pk):
        current_user = auth.current_user().id
        if not current_user == pk:
            raise BadRequest("You don't have permission to access this resource")

        data = request.get_json()
        # return {"message": UserManager.update(data)}
        return ResponseUserUpdateSchema().dump({"message": UserManager.update(data)})


class DeleteUserResource(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    def put(self, pk):
        result = UserManager.soft_delete_user(pk)
        return ResponseUserDeleteSchema().dump(result)
