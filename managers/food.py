from werkzeug.exceptions import BadRequest

from services.edamam import Edamam_Service
from services.open_ai import OpenAI_Service
from utils.helpers import find_macros_per_100_grams, find_macros_for_given_amount


class FoodManager:
    @staticmethod
    def basic_search(data):
        food_service = Edamam_Service()
        open_ai_service = OpenAI_Service()
        food_name = data["title"]

        try:
            food_data = food_service.get_food(food_name)
            proteins_per_100g, fats_per_100g, carbs_per_100g, calories_per100g = find_macros_per_100_grams(food_data)
        except Exception as ex:
            raise BadRequest(f"There is no food with name {food_name}! Check spelling and try again.")

        picture_url = open_ai_service.create_image(food_name)

        food = {"title": food_name,
                "proteins_per_100g": proteins_per_100g,
                "carbs_per_100g": carbs_per_100g,
                "fats_per_100g": fats_per_100g,
                "calories_per_100g": calories_per100g,
                "photo_url": picture_url}

        return food

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
