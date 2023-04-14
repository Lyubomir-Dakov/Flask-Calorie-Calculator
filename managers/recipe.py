import json

import requests
from werkzeug.exceptions import BadRequest

from db import db
from managers.auth import auth
from models import RecipeModel
from schemas.response.recipe import ResponseRecipeCreateSchema
from services.Edamam import Edamam_Service
from utils.helpers import find_macros_per_100_grams, find_macros_for_given_amount


class RecipeManager:
    @staticmethod
    def create(recipe_data):
        service = Edamam_Service()
        proteins = 0
        fats = 0
        carbs = 0
        calories = 0

        recipe_ingredients = list(recipe_data["ingredients"].keys())

        # when the recipe contains more than 7 ingredients Edamam_Service returns recipe_ingredients = []
        # split recipe_ingredients to smaller lists up to length = 7 and make request for every list
        split_lists = []
        edamam_limit = 7

        for i in range(0, len(recipe_ingredients), edamam_limit):
            split_lists.append(recipe_ingredients[i:i + edamam_limit])

        for piece in split_lists:
            foods = service.get_food(piece)["parsed"]
            if len(foods) < len(piece):
                raise BadRequest("This recipe contains incorrect ingredient name or it doesn't exists in the database!")
            i = 0
            for food in foods:
                food_data = food["food"]
                food_name = piece[i]
                food_amount = recipe_data["ingredients"][food_name]
                p, f, c, cal = find_macros_per_100_grams(food_data["nutrients"])
                p, c, f, cal = find_macros_for_given_amount(food_amount, p, c, f, cal)
                proteins += p
                fats += f
                carbs += c
                calories += cal
                i += 1

        recipe_data["proteins"] = round(proteins, 2)
        recipe_data["fats"] = round(fats, 2)
        recipe_data["carbs"] = round(carbs, 2)
        recipe_data["calories"] = round(calories, 2)

        current_user = auth.current_user()
        recipe_data["creator_id"] = current_user.id
        # Convert ingredients dictionary to JSON string
        recipe_data["ingredients"] = json.dumps(recipe_data["ingredients"])
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
            raise BadRequest(f"You don't have a recipe with title {recipe_title}!")
        return recipe

    @staticmethod
    def delete_recipe(pk, recipe_title):
        if not auth.current_user().id == pk:
            raise BadRequest("You don't have permission to access this resource!")
        recipe = RecipeModel.query.filter_by(title=recipe_title).first()
        if not recipe:
            raise BadRequest(f"You don't have a recipe with title {recipe_title}!")
        db.session.delete(recipe)
        return "", 204
