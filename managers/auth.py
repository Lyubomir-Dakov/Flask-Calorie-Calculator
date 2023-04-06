from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized

from models import UserModel, AdminModel, StaffModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(days=2),
            "type": user.__class__.__name__
        }
        return jwt.encode(payload=payload, key=config("SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            token = jwt.decode(jwt=token, key=config("SECRET_KEY"), algorithms=["HS256"])
            return token["sub"], token["type"]
        except Exception as ex:
            return ex


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    try:
        user_id, user_type = AuthManager.decode_token(token)
        user = user_mapper(user_type).query.filter_by(id=user_id).first()
        if not user:
            raise Unauthorized("Invalid or missing token")
        return user
    except Exception as ex:
        raise Unauthorized("Invalid or missing token")


def user_mapper(user_type):
    x = {"UserModel": UserModel,
         "StaffModel": StaffModel,
         "AdminModel": AdminModel}
    return x[user_type]
