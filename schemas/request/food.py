from marshmallow import fields

from schemas.bases import RequestFoodBaseSchema
from utils.validators import validate_food_amount


class RequestGetFoodSchema(RequestFoodBaseSchema):
    pass


class RequestGetFoodSchemaAuth(RequestFoodBaseSchema):
    amount = fields.Float(required=True, validate=validate_food_amount)
