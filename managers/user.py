from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager, auth
from models.user import UserModel, AdminModel, StaffModel
from utils.helpers import user_mapper
from utils.validators import validate_password, validate_if_email_already_exists


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
        except IntegrityError as ex:
            db.session.rollback()  # Rollback the session to prevent database inconsistencies
            error_info = ex.orig.args[0]  # Get the error message from the original exception
            if "email" in error_info:
                error_message = "This email is already registered. Please use a different email."
            else:
                error_message = "An error occurred while registering the user."
            raise BadRequest(error_message)

    @staticmethod
    def login(login_data):
        try:
            user = UserModel.query.filter_by(email=login_data["email"]).first() \
                   or StaffModel.query.filter_by(email=login_data["email"]).first() \
                   or AdminModel.query.filter_by(email=login_data["email"]).first()

            if user and check_password_hash(user.password, login_data["password"]):
                token = AuthManager.encode_token(user)
                user_role = user.role.value
                return token, user_role

            raise Exception
        except Exception:
            raise BadRequest("Invalid username or password")

    @staticmethod
    def update(update_data):
        user = auth.current_user()
        # Check if the email and password from requested data match with the current user email and password
        # and if not throws an error ""Invalid username or password""
        if user and user_mapper(user.__class__.__name__).query.filter_by(email=update_data["email"]).first() \
                and check_password_hash(user.password, update_data["password"]):
            validate_if_email_already_exists(update_data["new_email"])
            updated_data = []
            if update_data["new_email"] and update_data["new_email"] != user.email:
                user.email = update_data["new_email"]

                updated_data.append("email")
            if update_data["new_password"] and not check_password_hash(user.password, update_data["new_password"]):
                user.password = generate_password_hash(password=update_data["new_password"], method="sha256")
                updated_data.append("password")
            if update_data["new_first_name"] and update_data["new_first_name"] != user.first_name:
                user.first_name = update_data["new_first_name"]
                updated_data.append("first name")
            if update_data["new_last_name"] and update_data["new_last_name"] != user.last_name:
                user.last_name = update_data["new_last_name"]
                updated_data.append("last name")

            if len(updated_data) == 0:
                return "The given data is the same as your current data"
            elif len(updated_data) == 1:
                return f"You successfully updated your {updated_data[0]}."
            else:
                return f"You successfully updated your {', '.join(updated_data[0:-1])} and {updated_data[-1]}."

        else:
            raise BadRequest("Invalid username or password")

    @staticmethod
    def delete_user(pk):
        user_to_delete = UserModel.query.filter_by(id=pk).first()
        if not user_to_delete:
            raise BadRequest(f"User with id {pk} doesn't exist!")
        db.session.delete(user_to_delete)
        return "", 204
