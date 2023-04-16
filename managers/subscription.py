from werkzeug.exceptions import BadRequest

from db import db
from managers.auth import auth
from models import SubscriptionModel, UserStatus, SubscriptionStatus, RoleType
from services.pay_pal import PayPal_Service


class SubscriptionManager:
    @staticmethod
    def create_subscription():
        subscription_data = {}
        current_user = auth.current_user()
        service = PayPal_Service()
        access_token = service.get_access_token()
        subscription_id, approve_url = service.create_subscription(access_token)
        subscription_data["paypal_id"] = subscription_id
        subscription_data["subscriber_id"] = current_user.id
        try:
            subscription = SubscriptionModel(**subscription_data)
            db.session.add(subscription)
            db.session.commit()
            current_user.status = UserStatus.premium
            return subscription, approve_url
        except Exception:
            raise BadRequest("Something went wrong!")

    @staticmethod
    def pause_subscription(subscription_id):
        subscription = SubscriptionModel.query.filter_by(id=subscription_id, status=SubscriptionStatus.active).first()
        if not subscription:
            raise BadRequest("There is not active subscription with such id!")
        current_user = auth.current_user()
        if not subscription.subscriber_id == current_user.id:
            raise BadRequest("You don't have access to this resource!")
        paypal_id = subscription.paypal_id
        service = PayPal_Service()
        access_token = service.get_access_token()
        try:
            message = service.suspend_subscription(paypal_id, access_token)
            subscription.status = SubscriptionStatus.paused
            current_user.status = UserStatus.basic
            return {"message": message}
        except Exception:
            raise BadRequest("Something went wrong!")

    @staticmethod
    def activate_subscription(subscription_id):
        subscription = SubscriptionModel.query.filter_by(id=subscription_id, status=SubscriptionStatus.paused).first()
        if not subscription:
            raise BadRequest("There is not paused subscription with such id!")
        current_user = auth.current_user()
        if not subscription.subscriber_id == current_user.id:
            raise BadRequest("You don't have access to this resource!")
        paypal_id = subscription.paypal_id
        service = PayPal_Service()
        access_token = service.get_access_token()
        try:
            message = service.activate_subscription(paypal_id, access_token)
            subscription.status = SubscriptionStatus.active
            current_user.status = UserStatus.premium
            return {"message": message}
        except Exception:
            raise BadRequest("Something went wrong!")

    @staticmethod
    def cancel_subscription(subscription_id):
        subscription = SubscriptionModel.query.filter_by(id=subscription_id).first()
        if not subscription or subscription.status == SubscriptionStatus.canceled:
            raise BadRequest("There is not active or paused subscription with such id!")
        current_user = auth.current_user()
        if not subscription.subscriber_id == current_user.id and not current_user.role == RoleType.admin:
            raise BadRequest("You don't have access to this resource!")
        paypal_id = subscription.paypal_id
        service = PayPal_Service()
        access_token = service.get_access_token()
        try:
            message = service.cancel_subscription(paypal_id, access_token)
            subscription.status = SubscriptionStatus.canceled
            current_user.status = UserStatus.basic
            return {"message": message}
        except Exception:
            raise BadRequest("Something went wrong!")