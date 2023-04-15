import json

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


class ResponseRecipeGetSchema(ResponseRecipeCreateSchema):
    ingredients = fields.String(required=True)

    def dump(self, obj):
        recipe_data = super().dump(obj)
        recipe_data['ingredients'] = json.loads(recipe_data['ingredients'])
        return recipe_data
