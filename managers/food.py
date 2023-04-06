from werkzeug.exceptions import BadRequest

from managers.auth import auth
from services.USDA import USDA_Service


# TODO Validate food name with decorator and throw error
#  "There is no food with such name! Check spelling and try again." if needed
class FoodManager:
    @staticmethod
    def get(data):
        service = USDA_Service()
        food_name = data["title"]

        food = service.get_food(food_name).json()
        try:
            food_type = food["foods"][0]["foodCategory"]
            proteins_per_100g, carbs_per_100g, fats_per_100g, calories_per_100g = find_nutrients_per_100g(food)
        except Exception as ex:
            raise BadRequest(f"There is no food with name {food_name}! Check spelling and try again.")

        food = {"title": food_name,
                "proteins_per_100g": round(proteins_per_100g, 2),
                "carbs_per_100g": round(carbs_per_100g, 2),
                "fats_per_100g": round(fats_per_100g, 2),
                "calories_per_100g": round(calories_per_100g, 2),
                "food_type": food_type}

        current_user = auth.current_user()
        if current_user:
            amount = data["amount"]
            if amount < 0:
                raise BadRequest("Amount should be positive float number.")
            proteins, carbs, fats, calories = find_nutrients_for_given_amount(amount, proteins_per_100g, carbs_per_100g,
                                                                              fats_per_100g)
            food = {**food,
                    "amount": amount,
                    "proteins": round(proteins, 2),
                    "carbs": round(carbs, 2),
                    "fats": round(fats, 2),
                    "calories": round(calories, 2)}
            return food

        return food


def find_nutrients_per_100g(food):
    proteins_per_100g = None
    carbs_per_100g = None
    fats_per_100g = None
    for nutrient in food["foods"][0]['foodNutrients']:
        if nutrient['nutrientId'] == 1003:
            proteins_per_100g = nutrient['value']
        elif nutrient['nutrientId'] == 1005:
            carbs_per_100g = nutrient['value']
        elif nutrient['nutrientId'] == 1004:
            fats_per_100g = nutrient['value']
    calories_per_100g = carbs_per_100g * 4 + proteins_per_100g * 4 + fats_per_100g * 9
    return proteins_per_100g, carbs_per_100g, fats_per_100g, calories_per_100g


def find_nutrients_for_given_amount(amount, proteins_per_100g, carbs_per_100g, fats_per_100g):
    proteins = (proteins_per_100g * float(amount)) / 100
    carbs = (carbs_per_100g * float(amount)) / 100
    fats = (fats_per_100g * float(amount)) / 100
    calories = carbs * 4 + proteins * 4 + fats * 9
    return proteins, carbs, fats, calories
