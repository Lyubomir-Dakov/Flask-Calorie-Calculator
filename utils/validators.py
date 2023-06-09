import string

from marshmallow import ValidationError
from password_strength import PasswordPolicy
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash

from models import UserModel, AdminModel, SubscriptionModel


def validate_password(value):
    if value == "":
        raise ValidationError("You are not allowed to register with no password!")
    policy = PasswordPolicy.from_names(
        uppercase=1,
        numbers=1,
        special=1,
        nonletters=1,
        strength=0.33
    )

    errors_mapper = {
        "uppercase": "You need min 1 upper case letter in your password!",
        "numbers": "You need min 1 number in your password!",
        "special": "You need min 1 special character in your password!",
        "nonletters": "You need min 1 non-letter characters (digits, specials, anything) in your password!",
        "strength": f"Your password strength is {round(policy.password(value).strength(), 3)}. You have to make it stronger!"
    }

    errors = policy.test(value)

    if errors:
        error_message = []
        for error in errors:
            error_message.append(errors_mapper[error.name()])

        raise ValidationError(error_message)


def validate_if_email_already_exists(email, user):
    if user_mapper(user.__class__.__name__).query.filter_by(email=email).first():
        raise BadRequest("This email is already registered. Please use a different email.")
    return None


def validate_user_name(name):
    if name == "":
        raise ValidationError("You are not allowed to register with empty first or last name!")
    special_symbols = string.punctuation
    errors = []
    for ch in name:
        if ch.isdigit():
            error_message = "You are not allowed to put digits into first or last name!"
            if error_message not in errors:
                errors.append(error_message)
        if ch in special_symbols:
            error_message = "You are not allowed to put special symbols into first or last name!"
            if error_message not in errors:
                errors.append(error_message)
    if errors:
        raise ValidationError(errors)


def validate_recipe_title(title):
    special_symbols = string.punctuation
    for ch in title:
        if ch.isdigit():
            raise ValidationError("You are not allowed to put digits into recipe title!")
        if ch in special_symbols:
            raise ValidationError("You are not allowed to put special symbols into recipe title!")
    if not title[0].isupper():
        raise ValidationError("The title of every recipe should start with uppercase!")


def validate_food_title(title):
    special_symbols = string.punctuation
    for ch in title:
        if ch.isdigit():
            raise ValidationError("You are not allowed to put digits into food title!")
        if ch in special_symbols:
            raise ValidationError("You are not allowed to put special symbols into food title!")


def validate_food_amount(amount):
    if amount < 0:
        raise ValidationError("Food amount could not be less than 0 grams!")


def validate_email_and_password_on_update(update_data, user):
    if user and user_mapper(user.__class__.__name__).query.filter_by(email=update_data["email"]).first() \
            and check_password_hash(user.password, update_data["password"]):
        return None
    raise BadRequest("Invalid username or password")


def user_mapper(user_type):
    x = {"UserModel": UserModel,
         "AdminModel": AdminModel}
    return x[user_type]


def validate_subscription_pause_status(paypal_id):
    subscription = SubscriptionModel.query.filter_by(paypal_id=paypal_id, status="pause")
    if not subscription:
        raise ValidationError(f"There is no paused subscription with id '{paypal_id}' that you can activate!")
    return None


def validate_subscription_cancel_status(paypal_id):
    subscription = SubscriptionModel.query.filter_by(paypal_id=paypal_id)
    if not subscription or subscription.status == "canceled":
        raise ValidationError(f"There is not active or paused subscription with id '{paypal_id}' that you can cancel!")
    return None
