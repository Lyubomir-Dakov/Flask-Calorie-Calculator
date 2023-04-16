from flask_restful import Resource

from managers.auth import auth
from managers.subscription import SubscriptionManager
from models import UserStatus
from schemas.request.subscription import RequestSubscriptionPauseSchema
from schemas.response.subscription import ResponseSubscriptionCreateSchema
from utils.decorators import validate_user_status, validate_schema


class CreateSubscriptionResource(Resource):
    @auth.login_required
    @validate_user_status(UserStatus.basic)
    def post(self):
        subscription, approve_url = SubscriptionManager.create_subscription()
        return {"subscription_data": ResponseSubscriptionCreateSchema().dump(subscription),
                "url to approve": approve_url}


class PauseSubscriptionResource(Resource):
    @auth.login_required
    @validate_user_status(UserStatus.premium)
    @validate_schema(RequestSubscriptionPauseSchema)
    def put(self, pk):
        subscription = SubscriptionManager.pause_subscription(pk)
        return ResponseSubscriptionCreateSchema().dump(subscription)


class ActivateSubscriptionResource(Resource):
    @auth.login_required
    @validate_user_status(UserStatus.basic)
    def put(self, pk):
        pass


class CancelSubscriptionResource(Resource):
    @auth.login_required
    def put(self, pk):
        pass
