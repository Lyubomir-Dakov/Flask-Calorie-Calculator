from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.food import FoodManager
from models import FoodType, RoleType
from schemas.request.food import RequestCreateFoodSchema
from schemas.response.food import ResponseFoodSchema
from utils.decorators import validate_schema, permission_required


class CreateFoodResource(Resource):
    @auth.login_required
    @permission_required(RoleType.staff)
    @validate_schema(RequestCreateFoodSchema)
    def post(self):
        creator_id = auth.current_user().id
        data = request.get_json()
        data["calories_per_100g"] = data["carbs_per_100g"] * 4 + data["proteins_per_100g"] * 4 + data[
            "fats_per_100g"] * 9
        data["food_type"] = food_mapper(data["food_type"])
        food = FoodManager.create(data, creator_id)
        return ResponseFoodSchema().dump(food)

    @auth.login_required
    def get(self):
        pass



def food_mapper(food_type):
    mapper = {"grain": FoodType.grain,
              "vegetable": FoodType.vegetable,
              "fruit": FoodType.fruit,
              "meat_and_other_proteins": FoodType.meat_and_other_proteins,
              "milk_product": FoodType.milk_product,
              "nut": FoodType.nut}
    return mapper[food_type]
