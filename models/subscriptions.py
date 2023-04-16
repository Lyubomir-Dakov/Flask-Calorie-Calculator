from sqlalchemy import func

from db import db
from models.enums import SubscriptionStatus


class SubscriptionModel(db.Model):
    __tablename__ = "subscriptions"
    id = db.Column(db.Integer, primary_key=True)
    paypal_id = db.Column(db.String, nullable=False)
    title = db.Column(db.String, default="Premium membership", nullable=False)
    status = db.Column(db.Enum(SubscriptionStatus), default=SubscriptionStatus.active, nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    updated_on = db.Column(db.DateTime, onupdate=func.now())
    initial_tax = db.Column(db.Numeric(10, 2), default=3, nullable=False)
    monthly_tax = db.Column(db.Numeric(10, 2), default=5, nullable=False)
    subscriber_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    subscriber = db.relationship("UserModel")
