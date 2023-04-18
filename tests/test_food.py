from tests.base import TestRestAPIBase, generate_token
from tests.factories import UserFactory


class TestRequestFoodSchema(TestRestAPIBase):
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

