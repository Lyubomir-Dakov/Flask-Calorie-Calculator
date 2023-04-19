from sqlalchemy import func

from db import db


class RecipeModel(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.JSON, nullable=False)
    proteins = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    updated_on = db.Column(db.DateTime, onupdate=func.now())
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    photo_url = db.Column(db.String(2000), nullable=False)
    creator = db.relationship("UserModel")

    def set_ingredients(self, ingredients):
        self.ingredients = ingredients

    def get_ingredients(self):
        return self.ingredients
