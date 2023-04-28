from werkzeug.exceptions import BadRequest

from db import db
from managers.auth import auth
from models import RecipeModel
from services.open_ai import OpenAI_Service
from utils.helpers import count_macronutrients_in_recipe


class RecipeManager:
    @staticmethod
    def create_recipe(recipe_data):
        recipe_data = count_macronutrients_in_recipe(recipe_data)
        open_ai_service = OpenAI_Service()
        recipe_data["photo_url"] = open_ai_service.create_image(recipe_data["title"])
        recipe = RecipeModel(**recipe_data)
        try:
            db.session.add(recipe)
            db.session.commit()
            return recipe

        except Exception as ex:
            raise Exception

    @staticmethod
    def get_your_recipes():
        current_user = auth.current_user()
        recipes = RecipeModel.query.filter_by(creator_id=current_user.id).all()
        if not recipes:
            raise BadRequest("You still don't have any recipes."
                             " You could create some at 'http://127.0.0.1:5000/recipe'.")
        return recipes

    @staticmethod
    def get_one_recipe(pk, recipe_title):
        current_user = auth.current_user()
        recipe = RecipeModel.query.filter_by(id=pk).first()
        if not recipe or not recipe.title == recipe_title:
            raise BadRequest(f"You don't have a recipe with title '{recipe_title}'!")
        if not recipe.creator_id == current_user.id:
            raise BadRequest("You don't have permission to access this resource!")
        return recipe

    @staticmethod
    def delete_recipe(pk, recipe_title):
        if not auth.current_user().id == pk:
            raise BadRequest("You don't have permission to access this resource!")
        recipe = RecipeModel.query.filter_by(title=recipe_title).first()
        if not recipe:
            raise BadRequest(f"You don't have a recipe with title '{recipe_title}'!")
        db.session.delete(recipe)
        db.session.commit()
        return f"You successfully deleted recipe with title '{recipe_title}'"

    @staticmethod
    def update_recipe(pk, recipe_data):
        if not auth.current_user().id == pk:
            raise BadRequest("You don't have permission to access this resource!")
        recipe = RecipeModel.query.filter_by(title=recipe_data["title"]).first()
        if not recipe:
            raise BadRequest(f"You don't have a recipe with title '{recipe_data['title']}'!")
        if "new_title" not in recipe_data and recipe.get_ingredients() == recipe_data["ingredients"]:
            raise BadRequest("To update this recipe you need to provide different title or change its ingredients.")
        if "new_title" in recipe_data:
            recipe.title = recipe_data["new_title"]
        if not recipe.get_ingredients() == recipe_data["ingredients"]:
            recipe.set_ingredients(recipe_data["ingredients"])
            recipe_data = count_macronutrients_in_recipe(recipe_data)
            recipe.proteins = recipe_data["proteins"]
            recipe.fats = recipe_data["fats"]
            recipe.carbs = recipe_data["carbs"]
            recipe.calories = recipe_data["calories"]
        db.session.commit()
        return recipe
