from marshmallow import fields

from schemas.bases import RequestFoodBaseSchema


class RequestGetFoodSchema(RequestFoodBaseSchema):
    pass


class RequestGetFoodSchemaAuth(RequestFoodBaseSchema):
    amount = fields.Float(required=True)
