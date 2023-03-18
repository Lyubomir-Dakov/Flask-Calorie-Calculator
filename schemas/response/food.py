from marshmallow import fields

from schemas.bases import RequestFoodBaseSchema


class FoodResponseSchema(RequestFoodBaseSchema):
    id = fields.Integer(required=True)
    calories_per_100g = fields.Float(required=True)
    created_on = fields.DateTime(required=True)
    creator_id = fields.Integer(required=True)

    # updated_on = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
