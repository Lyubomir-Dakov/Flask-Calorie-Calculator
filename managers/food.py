from werkzeug.exceptions import BadRequest

from services.Edamam import Edamam_Service
from utils.helpers import find_macros_per_100_grams, find_macros_for_given_amount


# TODO Validate food name with decorator and throw error
#  "There is no food with such name! Check spelling and try again." if needed

class FoodManager:
    @staticmethod
    def basic_search(data):
        service = Edamam_Service()
        food_name = data["title"]

        try:
            food_data = service.get_food(food_name)["parsed"][0]["food"]["nutrients"]
            proteins_per_100g, fats_per_100g, carbs_per_100g, calories_per100g = find_macros_per_100_grams(food_data)
        except Exception as ex:
            raise BadRequest(f"There is no food with name {food_name}! Check spelling and try again.")

        food = {"title": food_name,
                "proteins_per_100g": proteins_per_100g,
                "carbs_per_100g": carbs_per_100g,
                "fats_per_100g": fats_per_100g,
                "calories_per_100g": calories_per100g}

        return food

    # TODO Validate if user has posted one food or more. ??
    @staticmethod
    def advanced_search(data):
        food = FoodManager.basic_search(data)
        proteins_per_100g = food["proteins_per_100g"]
        carbs_per_100g = food["carbs_per_100g"]
        fats_per_100g = food["fats_per_100g"]
        calories_per_100g = food["calories_per_100g"]
        amount = data["amount"]
        proteins, carbs, fats, calories = find_macros_for_given_amount(amount, proteins_per_100g, carbs_per_100g,
                                                                       fats_per_100g, calories_per_100g)
        food = {**food,
                "amount": amount,
                "proteins": round(proteins, 2),
                "carbs": round(carbs, 2),
                "fats": round(fats, 2),
                "calories": round(calories, 2)}
        return food
