from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager
from models.user import UserModel, AdminModel, StaffModel


class UserManager:
    @staticmethod
    def register(user_data):
        # hash the password from the given data
        user_data["password"] = generate_password_hash(password=user_data["password"], method="sha256")
        # create user with the given data
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.flush()
            return AuthManager.encode_token(user)
        except Exception as ex:
            raise BadRequest(str(ex))

    @staticmethod
    def login(login_data):
        try:
            user = UserModel.query.filter_by(email=login_data["email"]).first()\
                   or StaffModel.query.filter_by(email=login_data["email"]).first()\
                   or AdminModel.query.filter_by(email=login_data["email"]).first()

            if user and check_password_hash(user.password, login_data["password"]):
                token = AuthManager.encode_token(user)
                user_role = user.role.value
                return token, user_role

            raise Exception
        except Exception:
            raise BadRequest("Invalid username or password")

