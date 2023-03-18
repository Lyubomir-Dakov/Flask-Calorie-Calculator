from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models import FoodType


class RequestUserBaseSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class RequestFoodBaseSchema(Schema):
    title = fields.String(required=True)
    carbs_per_100g = fields.Float(required=True)
    fats_per_100g = fields.Float(required=True)
    proteins_per_100g = fields.Float(required=True)
    food_type = EnumField(FoodType, by_value=True)