from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.food import FoodManager
from schemas.request.food import RequestGetFoodSchema, RequestGetFoodSchemaAuth
from schemas.response.food import ResponseFoodSchema, ResponseFoodSchemaAuth
from utils.decorators import validate_schema


class BasicSearchFoodResource(Resource):
    @validate_schema(RequestGetFoodSchema)
    def get(self):
        data = request.get_json()
        food = FoodManager.basic_search(data)
        return ResponseFoodSchema().dump(food)


class AdvancedSearchFoodResource(Resource):
    @auth.login_required
    @validate_schema(RequestGetFoodSchemaAuth)
    def get(self):
        data = request.get_json()
        food = FoodManager.advanced_search(data)
        return ResponseFoodSchemaAuth().dump(food)
