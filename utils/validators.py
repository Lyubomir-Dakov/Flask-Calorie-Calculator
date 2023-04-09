from marshmallow import ValidationError
from password_strength import PasswordPolicy


def validate_password(value):
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
