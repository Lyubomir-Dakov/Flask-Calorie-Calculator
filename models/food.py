from sqlalchemy import func

from db import db
from models.enums import FoodType


class FoodModel(db.Model):
    __tablename__ = "foods"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False, unique=True)
    carbs_per_100g = db.Column(db.Float, nullable=False)
    fats_per_100g = db.Column(db.Float, nullable=False)
    proteins_per_100g = db.Column(db.Float, nullable=False)
    calories_per_100g = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    updated_on = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    food_type = db.Column(db.Enum(FoodType), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("staffs.id"), nullable=False)
    creator = db.relationship("StaffModel")
