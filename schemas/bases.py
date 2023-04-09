from marshmallow import Schema, fields, validate

from utils.validators import validate_password, validate_recipe_title, validate_food_title


class RequestUserBaseSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True, validate=validate.And(validate.Length(min=8, max=50), validate_password))


class RequestFoodBaseSchema(Schema):
    title = fields.String(required=True, validate=validate_food_title)


class RequestRecipeBaseSchema(Schema):
    title = fields.String(required=True, validate=validate_recipe_title)
