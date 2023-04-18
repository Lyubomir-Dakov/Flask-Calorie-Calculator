from models import RecipeModel, UserModel, SubscriptionModel
from tests.base import TestRestAPIBase, generate_token
from tests.factories import UserFactory


class TestRecipe(TestRestAPIBase):
    def test_create_recipes(self):
        users = UserModel.query.all()
        subscriptions = SubscriptionModel.query.all()
        recipes = RecipeModel.query.all()
        assert len(users) == 0
        assert len(subscriptions) == 0
        assert len(recipes) == 0

        user = UserFactory()
        data = {"title": "Apple", "amount": -1}

        token = generate_token(user)
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}
        # res = self.client.get("/food/advanced_search", headers=headers, json=data)
