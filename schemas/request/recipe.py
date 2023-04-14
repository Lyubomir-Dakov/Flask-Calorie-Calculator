from marshmallow import fields, validates

from schemas.bases import RequestRecipeBaseSchema
from utils.validators import validate_food_title, validate_food_amount


class RequestRecipeCreateSchema(RequestRecipeBaseSchema):
    ingredients = fields.Dict(required=True)

    @validates("ingredients")
    def validate_ingredients(self, ingredients):
        for ingredient, amount in ingredients.items():
            validate_food_title(ingredient)
            validate_food_amount(amount)


class RequestRecipeDeleteSchema(RequestRecipeBaseSchema):
    pass


class RequestRecipeGetSchema(RequestRecipeBaseSchema):
    pass


class RequestRecipeUpdateSchema(RequestRecipeCreateSchema):
    pass
