from marshmallow import Schema, fields


class ResponseSubscriptionCreateSchema(Schema):
    id = fields.Integer(required=True)
    paypal_id = fields.String(required=True)
    title = fields.String(required=True)
    status = fields.String(required=True)
    created_on = fields.DateTime(required=True)
    updated_on = fields.DateTime(required=False)
    initial_tax = fields.Integer(required=True)
    monthly_tax = fields.Integer(required=True)
    subscriber_id = fields.Integer(required=True)
