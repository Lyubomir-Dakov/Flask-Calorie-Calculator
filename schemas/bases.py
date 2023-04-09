from marshmallow import Schema, fields, validate

from utils.validators import validate_password


class RequestUserBaseSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True, validate=validate.And(validate.Length(min=8, max=50), validate_password))


class RequestFoodBaseSchema(Schema):
    title = fields.String(required=True)


class RequestRecipeBaseSchema(Schema):
    title = fields.String(required=True)
    ingredients = fields.Dict(required=True)
