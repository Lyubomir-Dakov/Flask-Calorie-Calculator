import requests
from decouple import config


class Edamam_Service:
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
