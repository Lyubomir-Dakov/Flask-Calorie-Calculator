from unittest.mock import patch

from db import db
from models import RecipeModel, UserModel, SubscriptionModel, UserStatus
from services.edamam import Edamam_Service
from services.open_ai import OpenAI_Service
from tests.base import TestRestAPIBase, generate_token
from tests.factories import UserFactory, RecipeFactory
from tests.helpers import edamam_response_test_recipe


class TestRecipe(TestRestAPIBase):
    @patch.object(OpenAI_Service, "create_image", return_value="some_created_image_url")
    @patch.object(Edamam_Service, "get_food_for_recipe", return_value=edamam_response_test_recipe)
    def test_create_recipe(self, mock_get_food_for_recipe, mock_create_image):
        users = UserModel.query.all()
        subscriptions = SubscriptionModel.query.all()
        recipes = RecipeModel.query.all()
        assert len(users) == 0
        assert len(subscriptions) == 0
        assert len(recipes) == 0

        user = UserFactory()

        token = generate_token(user)
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}
        data = {
            "title": "Caprice Salad",
            "ingredients": {
                "tomatoes": 400,
                "mozzarella": 200,
                "basil leaves": 12,
                "olive oil": 30,
                "balsamic vinegar": 15,
                "salt": 2
            }
        }

        # test user tries to create recipe without being premiium
        res = self.client.post("/recipe/create", headers=headers, json=data)
        assert res.status_code == 403
        assert res.json == {"message": "You don't have the correct status to access this resource!"}

        # for the purpose of this test we don't need to create subscription for the user
        # its enough to make him premium
        user.status = UserStatus.premium
        db.session.commit()

        # user creates a recipe
        res = self.client.post("/recipe/create", headers=headers, json=data)
        json_message = res.json
        json_message["created_on"] = "its created"
        assert res.status_code == 201
        assert json_message == {"proteins": 9.1,
                                "calories": 351.66,
                                "updated_on": None,
                                "title": "Caprice Salad",
                                "fats": 33.99,
                                "carbs": 6.49,
                                "created_on": "its created",
                                "id": 1,
                                "ingredients": {"balsamic vinegar": 15,
                                                "basil leaves": 12,
                                                "mozzarella": 200,
                                                "olive oil": 30,
                                                "salt": 2,
                                                "tomatoes": 400},
                                "photo_url": "some_created_image_url",
                                "creator_id": 1}
        assert len(RecipeModel.query.all()) == 1

        # test to create one more recipe with the same title raises
        res = self.client.post("/recipe/create", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "You already have a recipe with that title."}

        # test to get one recipe
        data = {"title": "Caprice Salad"}
        res = self.client.get("/user/1/recipe/get", headers=headers, json=data)
        assert res.status_code == 200
        assert res.json["updated_on"] is None

        # test to update recipe
        data = {
            "title": "Caprice Salad",
            "new_title": "Very big Caprice Salad",
            "ingredients": {
                "tomatoes": 400,
                "mozzarella": 200,
                "basil leaves": 12,
                "olive oil": 30,
                "balsamic vinegar": 15,
                "salt": 2
            }
        }
        res = self.client.put("/user/1/recipe/update", headers=headers, json=data)
        assert res.status_code == 200
        assert res.json["title"] == "Very big Caprice Salad"
        assert res.json["updated_on"] is not None

        # if the tested recipe had more than 7 ingredients mock_get_food_for_recipe would be called more times
        mock_get_food_for_recipe.assert_called_once_with(["balsamic vinegar",
                                                          "basil leaves",
                                                          "mozzarella",
                                                          "olive oil",
                                                          "salt",
                                                          "tomatoes"])
        mock_create_image.assert_called_once_with("Caprice Salad")

    def test_get_recipes(self):
        assert len(RecipeModel.query.all()) == 0
        assert len(UserModel.query.all()) == 0
        recipe = RecipeFactory()
        user = recipe.creator
        user.status = UserStatus.premium
        db.session.commit()
        assert len(RecipeModel.query.all()) == 1
        assert user == UserModel.query.filter_by(status=UserStatus.premium).first()

        token = generate_token(user)
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}

        # test to get recipe which starts with lowercase raises
        data = {"title": "incorrect recipe title"}
        res = self.client.get("/recipe/1/get", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": {"title": ["The title of every recipe should start with uppercase!"]}}

        # test to get invalid recipe raises
        data = {"title": "Incorrect recipe title"}
        res = self.client.get("/recipe/1/get", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "You don't have a recipe with title 'Incorrect recipe title'!"}

        # test to get all user's recipes
        res = self.client.get("/recipe/get", headers=headers)
        assert res.status_code == 200
        assert res.json == [{"title": "Caprice Salad"}]

        # test delete recipe
        data = {"title": recipe.title}
        res = self.client.delete("/user/1/recipe/delete", headers=headers, json=data)
        assert res.status_code == 204
        assert len(RecipeModel.query.all()) == 0
