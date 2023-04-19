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
            current_user.status = UserStatus.premium
            db.session.add(subscription)
            db.session.commit()
            return subscription, approve_url
        except Exception:
            raise BadRequest("Something went wrong!")

    @staticmethod
    def pause_subscription(subscription_id, subscription_paypal_id):
        subscription = SubscriptionModel.query.filter_by(id=subscription_id, status=SubscriptionStatus.active).first()
        current_user = auth.current_user()
        if not subscription:
            raise BadRequest("There is not active subscription with such id!")
        if not subscription.paypal_id == subscription_paypal_id:
            raise BadRequest("You provided wrong paypal_id!")
        if not subscription.subscriber_id == current_user.id:
            raise BadRequest("You don't have access to this resource!")

        service = PayPal_Service()
        access_token = service.get_access_token()
        try:
            message = service.suspend_subscription(subscription_paypal_id, access_token)
            subscription.status = SubscriptionStatus.paused
            current_user.status = UserStatus.basic
            db.session.commit()
            return {"message": message}
        except Exception:
            raise BadRequest("Something went wrong!")

    @staticmethod
    def activate_subscription(subscription_id, subscription_paypal_id):
        subscription = SubscriptionModel.query.filter_by(id=subscription_id, status=SubscriptionStatus.paused).first()
        current_user = auth.current_user()
        if not subscription:
            raise BadRequest("There is not paused subscription with such id!")
        if not subscription.paypal_id == subscription_paypal_id:
            raise BadRequest("You provided wrong paypal_id!")
        if not subscription.subscriber_id == current_user.id:
            raise BadRequest("You don't have access to this resource!")

        service = PayPal_Service()
        access_token = service.get_access_token()
        try:
            message = service.activate_subscription(subscription_paypal_id, access_token)
            subscription.status = SubscriptionStatus.active
            current_user.status = UserStatus.premium
            db.session.commit()
            return {"message": message}
        except Exception:
            raise BadRequest("Something went wrong!")

    @staticmethod
    def cancel_subscription(subscription_id, subscription_paypal_id):
        subscription = SubscriptionModel.query.filter_by(id=subscription_id).first()
        current_user = auth.current_user()
        if not subscription or subscription.status == SubscriptionStatus.canceled:
            raise BadRequest("There is not active or paused subscription with such id!")
        if not subscription.paypal_id == subscription_paypal_id:
            raise BadRequest("You provided wrong paypal_id!")
        if not subscription.subscriber_id == current_user.id and not current_user.role == RoleType.admin:
            raise BadRequest("You don't have access to this resource!")
        service = PayPal_Service()
        access_token = service.get_access_token()
        try:
            message = service.cancel_subscription(subscription_paypal_id, access_token)
            subscription.status = SubscriptionStatus.canceled
            current_user.status = UserStatus.basic
            db.session.commit()
            return {"message": message}
        except Exception:
            raise BadRequest("Something went wrong!")