from flask import request
from flask_restful import Resource

from db import db
from managers.auth import auth
from managers.recipe import RecipeManager
from schemas.request.recipe import RequestRecipeCreateSchema
from utils.decorators import validate_schema


class CreateRecipeResource(Resource):
    # TODO check in database if that user has already created recipe with that title and if so rais an error message
    # TODO try to do it with decorator
    @auth.login_required
    @validate_schema(RequestRecipeCreateSchema)
    def post(self):
        data = request.get_json()
        recipe = RecipeManager.create(data)
        return recipe
