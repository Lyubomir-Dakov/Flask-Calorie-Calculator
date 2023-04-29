from db import db
from models import UserStatus
from tests.base import TestRestAPIBase, generate_token
from tests.factories import UserFactory, AdminFactory


class TestLoginAndAuthorizationRequired(TestRestAPIBase):
    def test_auth_is_required(self):
        res = None
        all_guarded_urls = [
            ("PUT", "/user/1/update"),
            ("PUT", "/user/1/delete"),
            ("GET", "/food/advanced_search"),
            ("POST", "/recipe/create"),
            ("GET", "/recipe/get"),
            ("GET", "/recipe/1/get"),
            ("DELETE", "/recipe/1/delete"),
            ("PUT", "/recipe/1/update"),
            ("POST", "/subscription/create"),
            ("PUT", "/subscription/2/pause"),
            ("PUT", "/subscription/2/activate"),
            ("PUT", "/subscription/2/cancel")
        ]
        for method, url in all_guarded_urls:
            if method == "GET":
                res = self.client.get(url)
            elif method == "POST":
                res = self.client.post(url)
            elif method == "PUT":
                res = self.client.put(url)
            elif method == "DELETE":
                res = self.client.delete(url)

            assert res.status_code == 401
            assert res.json == {"message": "Invalid or missing token"}

    # only admin can delete a user
    def test_permission_required_delete_user_requires_admin_user(self):
        # user tries to delete another user
        user_1 = UserFactory()
        user_2 = UserFactory()
        token = generate_token(user_1)

        headers = {"Authorization": f"Bearer {token}"}
        res = self.client.put("/user/2/delete", headers=headers)

        assert res.status_code == 403
        assert res.json == {"message": "You don't have permission to access this resource!"}

        # admin deletes a user
        admin = AdminFactory()
        user = UserFactory()
        token = generate_token(admin)

        headers = {"Authorization": f"Bearer {token}"}
        res = self.client.put("/user/1/delete", headers=headers)

        assert res.status_code == 200
        assert res.json == {"message": "User with id 1 has been soft deleted successfully"}

    # if user is basic he is not allowed to create, delete, update, get recipe/s and pause subscription
    def test_validate_user_status_requires_premium(self):
        res = None
        user = UserFactory()
        token = generate_token(user)
        headers = {"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json"}
        all_guarded_urls = [
            ("POST", "/recipe/create"),
            ("GET", "/recipe/get"),
            ("GET", "/recipe/1/get"),
            ("DELETE", "/recipe/1/delete"),
            ("PUT", "/recipe/1/update"),
            ("PUT", "/subscription/2/pause"),
        ]
        for method, url in all_guarded_urls:
            if method == "GET":
                res = self.client.get(url, headers=headers)
            elif method == "POST":
                res = self.client.post(url, headers=headers)
            elif method == "PUT":
                res = self.client.put(url, headers=headers)
            elif method == "DELETE":
                res = self.client.delete(url, headers=headers)
            assert res.status_code == 403
            assert res.json == {"message": "You don't have the correct status to access this resource!"}

    # if user is premium he is not allowed to create and activate subscriptions
    def test_validate_user_status_requires_basic(self):
        res = None
        user = UserFactory()
        assert user.status == UserStatus.basic
        user.status = UserStatus.premium
        db.session.commit()

        token = generate_token(user)
        headers = {"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json"}
        all_guarded_urls = [
            ("POST", "/subscription/create"),
            ("PUT", "/subscription/1/activate")
        ]
        for method, url in all_guarded_urls:
            if method == "POST":
                res = self.client.post(url, headers=headers)
            elif method == "PUT":
                res = self.client.put(url, headers=headers)
            assert res.status_code == 403
            assert res.json == {"message": "You don't have the correct status to access this resource!"}
