from managers.food import FoodManager


class RecipeManager:
    @staticmethod
    def create(recipe_data):
        recipe_data["proteins"] = 0
        recipe_data["fats"] = 0
        recipe_data["carbs"] = 0
        recipe_data["calories"] = 0
        for ingredient_name, amount in recipe_data["ingredients"].items():

            data = FoodManager.get({"title": ingredient_name, "amount": amount})
            recipe_data["proteins"] += data["proteins"]
            recipe_data["fats"] += data["fats"]
            recipe_data["carbs"] += data["carbs"]
            recipe_data["calories"] = data["calories"]

        print(f"proteins: {recipe_data['proteins']}")
        print(f"fats: {recipe_data['fats']}")
        print(f"carbs: {recipe_data['carbs']}")
        print(f"calories: {recipe_data['calories']}")
