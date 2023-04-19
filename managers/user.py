from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager, auth
from managers.subscription import SubscriptionManager
from models import SubscriptionModel, SubscriptionStatus, UserStatus
from models.user import UserModel, AdminModel
from utils.helpers import update_email, update_password, update_first_name, \
    update_last_name, updated_user_result_message
from utils.validators import validate_email_and_password_on_update


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
            user = UserModel.query.filter_by(email=login_data["email"], deleted=False).first() \
                   or AdminModel.query.filter_by(email=login_data["email"]).first()

            if user and check_password_hash(user.password, login_data["password"]):
                token = AuthManager.encode_token(user)
                return token

            raise Exception
        except Exception:
            raise BadRequest("Invalid username or password")

    @staticmethod
    def update(update_data):
        user = auth.current_user()
        updated_data = []

        # Check if the email and password from requested data match with the current user email and password
        validate_email_and_password_on_update(update_data, user)

        # updates the email if a new email is provided
        update_email(update_data, updated_data, user)

        # updates the password if a new password is provided
        update_password(update_data, updated_data, user)

        # updates the fist_name if a new first_name is provided
        update_first_name(update_data, updated_data, user)

        # updates the last_name if a new_last_name is provided
        update_last_name(update_data, updated_data, user)

        return updated_user_result_message(updated_data)

    @staticmethod
    def soft_delete_user(pk):
        user_to_delete = UserModel.query.filter_by(id=pk, deleted=False).first()
        if not user_to_delete:
            raise BadRequest(f"User with id {pk} doesn't exist!")
        user_to_delete.deleted = True
        user_to_delete.status = UserStatus.basic
        subscription = SubscriptionModel.query.filter_by(subscriber_id=pk, status=SubscriptionStatus.active).first() or \
                       SubscriptionModel.query.filter_by(subscriber_id=pk, status=SubscriptionStatus.paused).first()
        if subscription:
            SubscriptionManager.cancel_subscription(subscription.id, subscription.paypal_id)
        db.session.commit()
        return {"message": f"User with id {pk} has been soft deleted successfully"}
