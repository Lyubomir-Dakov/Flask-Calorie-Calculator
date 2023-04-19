from unittest.mock import patch

from db import db
from models import UserModel, UserStatus, SubscriptionModel, SubscriptionStatus
from services.edamam import Edamam_Service
from services.open_ai import OpenAI_Service
from tests.base import TestRestAPIBase, generate_token
from tests.factories import UserFactory, SubscriptionFactory


class TestSearchFood(TestRestAPIBase):
    # test RequestGetFoodSchema
    def test_required_fields_missing_raises(self):
        data = {}
        headers = {"Content-Type": "application/json"}
        res = self.client.get("/food/basic_search", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": {"title": ["Missing data for required field."]}}

    def test_food_title_contains_digit_raises(self):
        data = {"title": "Apple5"}
        headers = {"Content-Type": "application/json"}
        res = self.client.get("/food/basic_search", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": {"title": ["You are not allowed to put digits into food title!"]}}

    def test_food_title_contains_special_symbols_raises(self):
        data = {"title": "Apple&"}
        headers = {"Content-Type": "application/json"}
        res = self.client.get("/food/basic_search", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": {"title": ["You are not allowed to put special symbols into food title!"]}}

    # test RequestGetFoodSchemaAuth
    def test_amount_is_negative_raises(self):
        data = {"title": "Apple", "amount": -1}
        user = UserFactory()
        token = generate_token(user)
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}
        res = self.client.get("/food/advanced_search", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": {"amount": ["Food amount could not be less than 0 grams!"]}}

    # test basic search food when the food name is wrong or does not exist in Edamam database
    @patch.object(OpenAI_Service, "create_image", return_value="some_created_food_picture")
    @patch.object(Edamam_Service, "get_food", return_value={"wrong food name"})
    def test_basic_search(self, mock_get_food, mock_create_image):
        headers = {"Content-Type": "application/json"}
        data = {"title": "sddsfgsdf"}
        res = self.client.get("/food/basic_search", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {'message': 'There is no food with name sddsfgsdf! Check spelling and try again.'}
        mock_get_food.assert_called_once_with(data["title"])
        # assert it will never reach the OpenAI_Service.create_image because it raises the error before it
        mock_create_image.assert_not_called()

    # test basic search foods successfully
    @patch.object(OpenAI_Service, "create_image", return_value="some_created_food_picture")
    @patch.object(Edamam_Service, "get_food", return_value={"PROCNT": 5, "FAT": 2, "CHOCDF": 10, "ENERC_KCAL": 200})
    def test_basic_food_search(self, mock_get_food, mock_create_image):
        headers = {"Content-Type": "application/json"}
        data = {"title": "apple"}
        res = self.client.get("/food/basic_search", headers=headers, json=data)
        assert res.status_code == 200
        assert res.json == {'carbs_per_100g': 10.0,
                            'title': 'apple',
                            'proteins_per_100g': 5.0,
                            'photo_url': 'some_created_food_picture',
                            'calories_per_100g': 200.0,
                            'fats_per_100g': 2.0}
        mock_get_food.assert_called_once_with(data["title"])
        mock_create_image.assert_called_once_with(data["title"])

    # test advanced search - need premium user
    @patch.object(OpenAI_Service, "create_image", return_value="some_created_food_picture")
    @patch.object(Edamam_Service, "get_food", return_value={"PROCNT": 5, "FAT": 2, "CHOCDF": 10, "ENERC_KCAL": 200})
    def test_advanced_food_search(self, mock_get_food, mock_create_image):
        assert len(UserModel.query.all()) == 0
        user = UserFactory()
        assert len(UserModel.query.all()) == 1
        assert user.status == UserStatus.basic

        subscription = SubscriptionFactory(subscriber_id=user.id)
        user.status = UserStatus.premium
        db.session.commit()

        assert len(SubscriptionModel.query.all()) == 1
        assert subscription.status == SubscriptionStatus.active
        assert UserModel.query.filter_by(id=1).first().status == UserStatus.premium

        token = generate_token(user)

        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}
        data = {"title": "apple", "amount": 200}
        res = self.client.get("/food/advanced_search", headers=headers, json=data)
        assert res.status_code == 200
        assert res.json == {'title': 'apple',
                            'photo_url': 'some_created_food_picture',
                            'calories_per_100g': 200.0,
                            'amount': 200.0,
                            'carbs': 20.0,
                            'proteins_per_100g': 5.0,
                            'fats': 4.0,
                            'fats_per_100g': 2.0,
                            'carbs_per_100g': 10.0,
                            'calories': 400.0,
                            'proteins': 10.0}
        mock_get_food.assert_called_once_with(data["title"])
        mock_create_image.assert_called_once_with(data["title"])
