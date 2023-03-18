from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized


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
            return token
        except Exception as ex:
            return ex


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    try:
        user_id, type_user = AuthManager.decode_token(token)
        return eval(f"{type_user}.query.filter_by(id={user_id}).first()")
    except Exception as ex:
        raise Unauthorized("Invalid or missing token")
