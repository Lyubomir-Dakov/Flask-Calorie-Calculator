from unittest.mock import patch

from db import db
from models import UserModel, SubscriptionModel, UserStatus, SubscriptionStatus, AdminModel
from services.pay_pal import PayPal_Service
from tests.base import TestRestAPIBase, generate_token
from tests.factories import UserFactory, SubscriptionFactory, AdminFactory


class TestSubscription(TestRestAPIBase):
    @patch.object(PayPal_Service, "create_subscription", return_value=("some_subscription_id", "some_approval_url"))
    @patch.object(PayPal_Service, "get_access_token", return_value="some_paypal_access_token")
    def test_subscription_create(self, mock_paypal_get_access_token, mock_subscription_id):
        users = UserModel.query.all()
        assert len(users) == 0
        subscriptions = SubscriptionModel.query.all()
        assert len(subscriptions) == 0

        user = UserFactory()
        assert len(UserModel.query.all()) == 1
        assert user.status == UserStatus.basic

        token = generate_token(user)

        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}
        res = self.client.post("/subscription/create", headers=headers)

        assert res.status_code == 201
        assert user.status == UserStatus.premium
        assert res.json["subscription_data"]["initial_tax"] == 3
        assert res.json["subscription_data"]["monthly_tax"] == 5
        assert res.json["subscription_data"]["paypal_id"] == "some_subscription_id"
        assert res.json["subscription_data"]["status"] == SubscriptionStatus.active.value
        assert not res.json["subscription_data"]["updated_on"]
        assert res.json["url to approve"] == "some_approval_url"
        assert res.json["subscription_data"]["title"] == "Premium membership"
        assert len(SubscriptionModel.query.all()) == 1

        mock_paypal_get_access_token.assert_called_once_with()
        mock_subscription_id.assert_called_once_with("some_paypal_access_token")

    @patch.object(PayPal_Service, "cancel_subscription", return_value="subscription is canceled")
    @patch.object(PayPal_Service, "activate_subscription", return_value="subscription is activated")
    @patch.object(PayPal_Service, "suspend_subscription", return_value="subscription is paused")
    @patch.object(PayPal_Service, "get_access_token", return_value="some_paypal_access_token")
    def test_subscription_pause_active_cancel_process(self, mock_paypal_get_access_token,
                                                      mock_paypal_suspend_subscription,
                                                      mock_paypal_activate_subscription,
                                                      mock_paypal_cancel_subscription):
        # 1) Create user who subscribes. User become premium, subscription is active
        assert len(UserModel.query.all()) == 0
        assert len(SubscriptionModel.query.all()) == 0

        user = UserFactory()
        assert user.status == UserStatus.basic
        assert len(UserModel.query.all()) == 1

        subscription = SubscriptionFactory(subscriber_id=user.id)
        assert len(SubscriptionModel.query.all()) == 1
        assert subscription.status == SubscriptionStatus.active

        user.status = UserStatus.premium
        db.session.commit()
        assert UserModel.query.filter_by(id=1).first().status == UserStatus.premium

        token = generate_token(user)
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}

        # 2) Pause the subscription => user become basic, subscription become paused

        # test with wrong subscription paypal_id
        data = {"paypal_id": "wrong_paypal_id"}
        res = self.client.put("/subscription/1/pause", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": {"paypal_id": ["There is no active subscription with id"
                                                      " 'wrong_paypal_id' that you can pause!"]}}

        # test with incorrect pk
        data = {"paypal_id": subscription.paypal_id}
        res = self.client.put("/subscription/2/pause", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "There is not active subscription with such id!"}

        # test happy case - user pauses his subscription => user.status = basic and subscription.status = paused
        data = {"paypal_id": subscription.paypal_id}
        res = self.client.put("/subscription/1/pause", headers=headers, json=data)
        assert res.status_code == 200
        assert res.json == {"message": "subscription is paused"}
        assert user.status == UserStatus.basic
        assert subscription.status == SubscriptionStatus.paused

        # 3) User activates the subscription => user becomes premium, subscription becomes active

        # test with wrong subscription paypal_id
        data = {"paypal_id": "wrong paypal_id"}
        res = self.client.put("/subscription/1/activate", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "You provided wrong paypal_id!"}

        # test with wrong subscription id
        data = {"paypal_id": subscription.paypal_id}
        res = self.client.put("/subscription/2/activate", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "There is not paused subscription with such id!"}

        # test happy case - user activates his subscription => user becomes premium, subscription becomes active
        data = {"paypal_id": subscription.paypal_id}
        res = self.client.put("/subscription/1/activate", headers=headers, json=data)
        assert res.status_code == 200
        assert res.json == {"message": "subscription is activated"}
        assert subscription.status == SubscriptionStatus.active
        assert user.status == UserStatus.premium

        # 4) User cancel his subscription => user becomes basic, subscription becomes canceled

        # test with wrong paypal_id
        data = {"paypal_id": "wrong paypal_id"}
        res = self.client.put("/subscription/1/cancel", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "You provided wrong paypal_id!"}

        # test with wrong subscription id
        data = {"paypal_id": subscription.paypal_id}
        res = self.client.put("/subscription/2/cancel", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "There is not active or paused subscription with such id!"}

        # test happy case - user cancel his subscription => user becomes basic, subscription becomes canceled
        data = {"paypal_id": subscription.paypal_id}
        res = self.client.put("/subscription/1/cancel", headers=headers, json=data)
        assert res.status_code == 200
        assert res.json == {"message": "subscription is canceled"}
        assert user.status == UserStatus.basic
        assert subscription.status == SubscriptionStatus.canceled

        mock_paypal_get_access_token.assert_called()
        mock_paypal_suspend_subscription.assert_called_once_with(subscription.paypal_id, "some_paypal_access_token")
        mock_paypal_activate_subscription.assert_called_once_with(subscription.paypal_id, "some_paypal_access_token")
        mock_paypal_cancel_subscription.assert_called_once_with(subscription.paypal_id, "some_paypal_access_token")

    @patch.object(PayPal_Service, "cancel_subscription", return_value="subscription is canceled")
    @patch.object(PayPal_Service, "get_access_token", return_value="some_paypal_access_token")
    def test_admin_deletes_premium_user_subscription_becomes_canceled(self, mock_paypal_get_access_token,
                                                                      mock_paypal_cancel_subscription):
        assert len(UserModel.query.all()) == 0
        assert len(AdminModel.query.all()) == 0
        assert len(SubscriptionModel.query.all()) == 0

        user = UserFactory()
        admin = AdminFactory()
        subscription = SubscriptionFactory(subscriber_id=user.id)
        user.status = UserStatus.premium
        db.session.commit()
        assert len(UserModel.query.all()) == 1
        assert len(AdminModel.query.all()) == 1
        assert len(SubscriptionModel.query.all()) == 1
        assert UserModel.query.filter_by(id=1).first().status == UserStatus.premium

        token = generate_token(admin)
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}
        res = self.client.put("/user/1/delete", headers=headers)
        assert res.status_code == 200
        assert res.json == {"message": "User with id 1 has been soft deleted successfully"}
        assert user.deleted is True
        assert user.status == UserStatus.basic
        assert subscription.status == SubscriptionStatus.canceled

        mock_paypal_get_access_token.assert_called_once_with()
        mock_paypal_cancel_subscription.assert_called_once_with(subscription.paypal_id, "some_paypal_access_token")

    @patch.object(PayPal_Service, "cancel_subscription", return_value="subscription is canceled")
    @patch.object(PayPal_Service, "suspend_subscription", return_value="subscription is paused")
    @patch.object(PayPal_Service, "get_access_token", return_value="some_paypal_access_token")
    def test_admin_deletes_basic_user_who_has_paused_subscription_subscription_becomes_canceled(self,
                                                                                                mock_paypal_get_access_token,
                                                                                                mock_paypal_pause_subscription,
                                                                                                mock_paypal_cancel_subscription):
        assert len(UserModel.query.all()) == 0
        assert len(AdminModel.query.all()) == 0
        assert len(SubscriptionModel.query.all()) == 0

        user = UserFactory()
        admin = AdminFactory()
        subscription = SubscriptionFactory(subscriber_id=user.id)
        user.status = UserStatus.premium
        db.session.commit()
        assert len(UserModel.query.all()) == 1
        assert len(AdminModel.query.all()) == 1
        assert len(SubscriptionModel.query.all()) == 1
        assert UserModel.query.filter_by(id=1).first().status == UserStatus.premium

        user_token = generate_token(user)
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {user_token}"}
        data = {"paypal_id": subscription.paypal_id}
        res = self.client.put("/subscription/1/pause", headers=headers, json=data)
        assert res.status_code == 200
        assert res.json == {"message": "subscription is paused"}
        assert user.status == UserStatus.basic
        assert subscription.status == SubscriptionStatus.paused

        admin_token = generate_token(admin)
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {admin_token}"}
        res = self.client.put("/user/1/delete", headers=headers)
        assert res.status_code == 200
        assert res.json == {"message": "User with id 1 has been soft deleted successfully"}
        assert user.deleted is True
        assert user.status == UserStatus.basic
        assert subscription.status == SubscriptionStatus.canceled

        # paypal_access_token has been called 2 times - on subscription, on pause subscription
        mock_paypal_get_access_token.assert_called()
        mock_paypal_pause_subscription.assert_called_once_with(subscription.paypal_id, "some_paypal_access_token")
        mock_paypal_cancel_subscription.assert_called_once_with(subscription.paypal_id, "some_paypal_access_token")
