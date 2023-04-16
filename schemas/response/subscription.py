from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models import SubscriptionStatus


class ResponseSubscriptionCreateSchema(Schema):
    id = fields.Integer(required=True)
    paypal_id = fields.String(required=True)
    title = fields.String(required=True)
    status = EnumField(SubscriptionStatus, by_value=True, required=True)
    created_on = fields.DateTime(required=True)
    updated_on = fields.DateTime(required=False)
    initial_tax = fields.Integer(required=True)
    monthly_tax = fields.Integer(required=True)
    subscriber_id = fields.Integer(required=True)


class ResponseSubscriptionPauseSchema(Schema):
    message = fields.String(required=True)


class ResponseSubscriptionActivateSchema(Schema):
    message = fields.String(required=True)


class ResponseSubscriptionCancelSchema(Schema):
    message = fields.String(required=True)
