from marshmallow import Schema, fields


class RequestUserBaseSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class RequestFoodBaseSchema(Schema):
    title = fields.String(required=True)


class RequestRecipeBaseSchema(Schema):
    title = fields.String(required=True)
    ingredients = fields.Dict(required=True)
