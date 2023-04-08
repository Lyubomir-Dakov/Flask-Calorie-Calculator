from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from managers.auth import auth
from managers.recipe import RecipeManager
from models import RecipeModel
from schemas.request.recipe import RequestRecipeCreateSchema
from utils.decorators import validate_schema


class CreateRecipeResource(Resource):
    # TODO check in database if that user has already created recipe with that title and if so rais an error message
    # TODO try to do it with decorator
    @auth.login_required
    @validate_schema(RequestRecipeCreateSchema)
    def post(self):
        data = request.get_json()
        current_user_id = auth.current_user().id
        if RecipeModel.query.filter_by(creator_id=current_user_id, title=data["title"]).first():
            raise BadRequest("You already have a recipe with that title.")
        recipe = RecipeManager.create(data)
        return recipe
