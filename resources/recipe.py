from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.recipe import RecipeManager
from schemas.request.recipe import RequestRecipeCreateSchema
from utils.decorators import validate_schema


class CreateRecipeResource(Resource):
    @auth.login_required
    @validate_schema(RequestRecipeCreateSchema)
    def post(self):
        data = request.get_json()
        recipe = RecipeManager.create(data)
