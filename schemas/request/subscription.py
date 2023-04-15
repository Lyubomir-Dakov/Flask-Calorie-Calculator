from marshmallow import Schema, fields, ValidationError, validates

from models import SubscriptionModel


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


class RequestSubscriptionUpdateBaseSchema(Schema):
    paypal_id = fields.String(required=True)


class RequestSubscriptionCreateSchema(Schema):
    pass


class RequestSubscriptionPauseSchema(RequestSubscriptionUpdateBaseSchema):

    @validates("paypal_id")
    def validate_subscription_active_status(self, paypal_id):
        subscription = SubscriptionModel.query.filter_by(paypal_id=paypal_id, status="active")
        if not subscription:
            raise ValidationError(f"There is no active subscription with id '{paypal_id}' that you can pause!")
        return None


class RequestSubscriptionActivateSchema(Schema):
    paypal_id = fields.String(required=True, validate=validate_subscription_pause_status)


class RequestSubscriptionCancelSchema(Schema):
    paypal_id = fields.String(required=True, validate=validate_subscription_cancel_status)
