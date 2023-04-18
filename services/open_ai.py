import requests
from decouple import config
from werkzeug.exceptions import BadRequest


class OpenAI_Service:
    def __init__(self):
        self.secret_key = config("OPEN_AI_SECRET_KEY")
        self.base_url = config("OPEN_AI_BASE_URL")

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.secret_key}"
        }

    def create_image(self, recipe_title):
        url = f"{self.base_url}/v1/images/generations"
        body = {
            "prompt": f"{recipe_title}",
            "n": 1,
            "size": "256x256"
        }
        response = requests.post(url=url, headers=self.headers, json=body)
        if response.status_code == 200:
            return response.json()["data"][0]["url"]
        raise BadRequest("Something went wrong")
