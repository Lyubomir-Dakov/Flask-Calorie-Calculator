import requests
from decouple import config


class Edamam_Service():
    def __init__(self):
        self.base_url = config("EDAMAM_URL")
        self.headers = {
            "Content-Type": "application/json"
        }
        self.app_id = config("EDAMAM_APP_ID")
        self.app_key = config("EDAMAM_APP_KEY")

    def get_food(self, food_name):
        url = f"{self.base_url}/api/food-database/v2/parser?app_id={self.app_id}&app_key={self.app_key}&ingr={food_name}&nutrition-type=cooking&category=generic-foods"
        response = requests.get(url, headers=self.headers)
        return response.json()


if __name__ == "__main__":
    service = Edamam_Service()
    food_name = "banana"
    result = service.get_food(food_name)["parsed"][0]["food"]["nutrients"]
    proteins, fats, carbs, calories = result["PROCNT"], result["FAT"], result["CHOCDF"], result["ENERC_KCAL"]
    print(f"{food_name}: {proteins} proteins, {carbs} carbs {fats} fats, {calories} calories")

    print()
    food_name2 = "meat, banana, kiwi, salmon"
    result2 = service.get_food(food_name2)["parsed"]
    for food in result2:
        food_name = food["food"]["label"]
        data = food["food"]["nutrients"]
        proteins, fats, carbs, calories = data["PROCNT"], data["FAT"], data["CHOCDF"], data["ENERC_KCAL"]
        print(f"{food_name}: {proteins} proteins, {carbs} carbs {fats} fats, {calories} calories")
