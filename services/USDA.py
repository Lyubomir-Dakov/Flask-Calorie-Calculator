# USDA - U.S.Department of Agriculture
import requests
from decouple import config


class USDA_Service:
    def __init__(self):
        self.base_url = config("USDA_URL")
        self.headers = {
            "Content-Type": "application/json",
            "X-Api-Key": "DEMO_KEY"
        }
        self.API_Key = config("USDA_API_KEY")

    def get_food(self, food_name):
        url = f"{self.base_url}/v1/foods/search?api_key={self.API_Key}&query={food_name}"
        response = requests.get(url, headers=self.headers)
        return response

    def get_foods(self, food_list):
        url = f"{self.base_url}/v1/foods/search?api_key={self.API_Key}&query={','.join(food_list)}"
        response = requests.get(url, headers=self.headers)
        return response.json()


