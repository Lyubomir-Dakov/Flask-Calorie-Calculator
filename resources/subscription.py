from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.subscription import SubscriptionManager
from models import UserStatus
from schemas.request.subscription import RequestSubscriptionCreateSchema
from schemas.response.subscription import ResponseSubscriptionCreateSchema
from utils.decorators import validate_schema, validate_user_status


class CreateSubscriptionResource(Resource):
    @auth.login_required
    @validate_user_status(UserStatus.basic)
    def post(self):
        subscription = SubscriptionManager.create_subscription()
        return ResponseSubscriptionCreateSchema().dump(subscription)


class PauseSubscriptionResource(Resource):
    @auth.login_required
    @validate_user_status(UserStatus.premium)
    def put(self, pk):
        pass


class ActivateSubscriptionResource(Resource):
    @auth.login_required
    @validate_user_status(UserStatus.basic)
    def put(self, pk):
        pass


class CancelSubscriptionResource(Resource):
    @auth.login_required
    def put(self, pk):
        pass
