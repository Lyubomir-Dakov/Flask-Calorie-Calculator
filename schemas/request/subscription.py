from marshmallow import Schema, fields, ValidationError, validates

from models import SubscriptionModel
from utils.validators import validate_subscription_pause_status, validate_subscription_cancel_status


class RequestSubscriptionCreateSchema(Schema):
    pass


class RequestSubscriptionPauseSchema(Schema):
    paypal_id = fields.String(required=True)

    @validates("paypal_id")
    def validate_subscription_active_status(self, paypal_id):
        subscription = SubscriptionModel.query.filter_by(paypal_id=paypal_id, status="active").first()
        if not subscription:
            raise ValidationError(f"There is no active subscription with id '{paypal_id}' that you can pause!")
        return None


class RequestSubscriptionActivateSchema(Schema):
    paypal_id = fields.String(required=True, validate=validate_subscription_pause_status)


class RequestSubscriptionCancelSchema(Schema):
    paypal_id = fields.String(required=True, validate=validate_subscription_cancel_status)
