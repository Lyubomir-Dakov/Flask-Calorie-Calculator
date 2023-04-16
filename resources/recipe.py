from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from managers.auth import auth
from managers.recipe import RecipeManager
from models import RecipeModel, UserStatus
from schemas.bases import RequestRecipeBaseSchema
from schemas.request.recipe import RequestRecipeCreateSchema, RequestRecipeDeleteSchema, RequestRecipeGetSchema, \
    RequestRecipeUpdateSchema
from schemas.response.recipe import ResponseRecipeCreateSchema, ResponseRecipeGetSchema, ResponseRecipeUpdateSchema
from utils.decorators import validate_schema, validate_user_status


class CreateRecipeResource(Resource):
    @auth.login_required
    @validate_schema(RequestRecipeCreateSchema)
    @validate_user_status(UserStatus.premium)
    def post(self):
        data = request.get_json()
        current_user_id = auth.current_user().id
        if RecipeModel.query.filter_by(creator_id=current_user_id, title=data["title"]).first():
            raise BadRequest("You already have a recipe with that title.")
        recipe = RecipeManager.create_recipe(data)
        return ResponseRecipeCreateSchema().dump(recipe)


class GetRecipesResource(Resource):
    @auth.login_required
    @validate_user_status(UserStatus.premium)
    def get(self, pk):
        recipes = RecipeManager.get_your_recipes(pk)
        return RequestRecipeBaseSchema().dump(recipes, many=True)


class DeleteRecipeResource(Resource):
    @auth.login_required
    @validate_schema(RequestRecipeDeleteSchema)
    @validate_user_status(UserStatus.premium)
    def delete(self, pk):
        data = request.get_json()
        return RecipeManager.delete_recipe(pk, data["title"])


class GetRecipeResource(Resource):
    @auth.login_required
    @validate_schema(RequestRecipeGetSchema)
    @validate_user_status(UserStatus.premium)
    def get(self, pk):
        data = request.get_json()
        recipe = RecipeManager.get_one_recipe(pk, data["title"])
        return ResponseRecipeGetSchema().dump(recipe)


class UpdateRecipeResource(Resource):
    @auth.login_required
    @validate_schema(RequestRecipeUpdateSchema)
    @validate_user_status(UserStatus.premium)
    def put(self, pk):
        data = request.get_json()
        recipe = RecipeManager.update_recipe(pk, data)
        return ResponseRecipeUpdateSchema().dump(recipe)

