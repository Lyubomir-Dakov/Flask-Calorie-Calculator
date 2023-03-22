from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.food import FoodManager
from schemas.request.food import RequestCreateFoodSchema
from schemas.response.food import ResponseFoodSchema
from utils.decorators import validate_schema


class CreateFoodResource(Resource):
    @auth.login_required
    @validate_schema(RequestCreateFoodSchema)
    def post(self):
        creator_id = auth.current_user().id
        data = request.get_json()
        data["calories_per_100g"] = data["carbs_per_100g"] * 4 + data["proteins_per_100g"] * 4 + data[
            "fats_per_100g"] * 9
        food = FoodManager.create(data, creator_id)
        return ResponseFoodSchema().dump(food)
