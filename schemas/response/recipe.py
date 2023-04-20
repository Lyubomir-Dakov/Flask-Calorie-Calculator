from marshmallow import fields

from schemas.bases import RequestRecipeBaseSchema


class ResponseRecipeCreateSchema(RequestRecipeBaseSchema):
    id = fields.Integer(required=True)
    ingredients = fields.Dict(required=True)
    proteins = fields.Float(required=True)
    fats = fields.Float(required=True)
    carbs = fields.Float(required=True)
    calories = fields.Float(required=True)
    created_on = fields.DateTime(required=True)
    updated_on = fields.DateTime(required=False)
    creator_id = fields.Integer(required=True)
    photo_url = fields.URL(required=True)


class ResponseRecipeGetSchema(ResponseRecipeCreateSchema):
    pass


class ResponseRecipeUpdateSchema(ResponseRecipeCreateSchema):
    pass
