from db import db
from models import FoodModel


class FoodManager:

    @staticmethod
    def create(data, creator_id):
        data["creator_id"] = creator_id
        food = FoodModel(**data)
        db.session.add(food)
        db.session.flush()
        return food
