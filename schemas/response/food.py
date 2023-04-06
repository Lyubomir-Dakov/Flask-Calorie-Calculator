from marshmallow import fields

from schemas.request.food import RequestGetFoodSchema, RequestGetFoodSchemaAuth


class ResponseFoodSchema(RequestGetFoodSchema):
    carbs_per_100g = fields.Float(required=True)
    fats_per_100g = fields.Float(required=True)
    proteins_per_100g = fields.Float(required=True)
    calories_per_100g = fields.Float(required=True)
    food_type = fields.String(required=True)


class ResponseFoodSchemaAuth(ResponseFoodSchema, RequestGetFoodSchemaAuth):
    proteins = fields.Float(required=True)
    carbs = fields.Float(required=True)
    fats = fields.Float(required=True)
    calories = fields.Float(required=True)
