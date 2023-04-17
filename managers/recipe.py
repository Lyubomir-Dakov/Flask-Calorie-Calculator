import json

from werkzeug.exceptions import BadRequest

from db import db
from managers.auth import auth
from models import RecipeModel
from utils.helpers import count_macronutrients_in_recipe


class RecipeManager:
    @staticmethod
    def create_recipe(recipe_data):
        recipe_data = count_macronutrients_in_recipe(recipe_data)
        recipe = RecipeModel(**recipe_data)
        try:
            db.session.add(recipe)
            db.session.flush()
            # Convert ingredients back to dictionary for response
            recipe_data["ingredients"] = json.loads(recipe_data["ingredients"])
            return recipe_data

        except Exception as ex:
            raise Exception

    @staticmethod
    def get_your_recipes(pk):
        if not auth.current_user().id == pk:
            raise BadRequest("You don't have permission to access this resource!")
        recipes = RecipeModel.query.filter_by(creator_id=pk).all()
        if not recipes:
            raise BadRequest("You still don't have any recipes."
                             " You could create some at 'http://127.0.0.1:5000/recipe'.")
        return recipes

    @staticmethod
    def get_one_recipe(pk, recipe_title):
        if not auth.current_user().id == pk:
            raise BadRequest("You don't have permission to access this resource!")
        recipe = RecipeModel.query.filter_by(title=recipe_title).first()
        if not recipe:
            raise BadRequest(f"You don't have a recipe with title '{recipe_title}'!")
        return recipe

    @staticmethod
    def delete_recipe(pk, recipe_title):
        if not auth.current_user().id == pk:
            raise BadRequest("You don't have permission to access this resource!")
        recipe = RecipeModel.query.filter_by(title=recipe_title).first()
        if not recipe:
            raise BadRequest(f"You don't have a recipe with title '{recipe_title}'!")
        db.session.delete(recipe)
        return "", 204

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
        db.session.add(recipe)
        db.session.commit()
        return recipe
