from werkzeug.security import generate_password_hash

from db import db
from models import UserModel
from tests.base import TestRestAPIBase, generate_token
from tests.factories import UserFactory, AdminFactory


class TestRegisterLoginUpdateDeleteUser(TestRestAPIBase):
    # test register
    def test_required_fields_missing_raises(self):
        headers = {"Content-Type": "application/json"}
        data = {}
        res = self.client.post("/user/register", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": {"last_name": ["Missing data for required field."],
                                        "email": ["Missing data for required field."],
                                        "password": ["Missing data for required field."],
                                        "first_name": ["Missing data for required field."]}}

    # test the input password on user register
    def test_validate_password_raises(self):
        assert len(UserModel.query.all()) == 0
        headers = {"Content-Type": "application/json"}

        # test with empty password
        data = {"first_name": "Test", "last_name": "Testov",
                "email": "t.testov@abv.bg", "password": ""}
        res = self.client.post("/user/register", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": {
            "password": ["Length must be between 8 and 50.", "You are not allowed to register with no password!"]}}

        # test with short and very weak password to trigger all errors
        data = {"first_name": "Test", "last_name": "Testov",
                "email": "t.testov@abv.bg", "password": "a"}
        headers = {"Content-Type": "application/json"}
        res = self.client.post("/user/register", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": {"password": ["Length must be between 8 and 50.",
                                                     "You need min 1 upper case letter in your password!",
                                                     "You need min 1 number in your password!",
                                                     "You need min 1 special character in your password!",
                                                     "You need min 1 non-letter characters "
                                                     "(digits, specials, anything) in your password!",
                                                     "Your password strength is 0.0. You have to make it stronger!"]}}

    def test_validate_email_already_exists_raises(self):
        assert len(UserModel.query.all()) == 0
        user_1 = UserFactory()
        assert len(UserModel.query.all()) == 1
        headers = {"Content-Type": "application/json"}
        data = {"first_name": "Test", "last_name": "Testov",
                "email": user_1.email, "password": "Igrach123#PlayeR1"}
        res = self.client.post("/user/register", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "This email is already registered. Please use a different email."}

    def test_user_name_contains_digit_or_special_symbol_raises(self):
        headers = {"Content-Type": "application/json"}
        data = {"first_name": "Te$st1", "last_name": "Te1st%ov",
                "email": "t.testiv@abv.bg", "password": "Igrach123#PlayeR1"}
        res = self.client.post("/user/register", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {
            "message":
                {"first_name":
                     ["You are not allowed to put special symbols into first or last name!",
                      "You are not allowed to put digits into first or last name!"],
                 "last_name":
                     ["You are not allowed to put digits into first or last name!",
                      "You are not allowed to put special symbols into first or last name!"]
                 }
        }

    def test_validate_new_password_and_email_on_user_update_raises(self):
        assert len(UserModel.query.all()) == 0
        user = UserModel(email="t.testov@abv.bg",
                         password="Igrach123#PlayeR1",
                         first_name="Test",
                         last_name="Testov"
                         )
        # in update_user we compare the hashed passwords => need to hash the password for the test
        user.password = generate_password_hash(password=user.password, method="sha256")
        db.session.add(user)
        db.session.commit()
        assert len(UserModel.query.all()) == 1

        token = generate_token(user)
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}
        data = {}

        # test to update user with missing data
        res = self.client.put("/user/2/update", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": {"email": ["Missing data for required field."],
                                        "password": ["Missing data for required field."]}}

        # test to update user with incorrect pk provided
        data = {
            "email": "t.testov@abv.bg",
            "password": "Igrach123#PlayeR1",
            "new_email": "test.testov@abv.bg",
            "new_first_name": "Thetest",
            "new_last_name": "Testoviqt",
            "new_password": "Igrach123#PlayeR2",
            "retype_new_password": "Igrach123#PlayeR2"
        }
        res = self.client.put("/user/2/update", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "You don't have permission to access this resource"}

        # test to update user with incorrect password provided
        data = {
            "email": "t.testov@abv.bg",
            "password": "Igrach123#PlayeR",
            "new_email": "test.testov@abv.bg",
            "new_first_name": "Thetest",
            "new_last_name": "Testoviqt",
            "new_password": "Igrach123#PlayeR2",
            "retype_new_password": "Igrach123#PlayeR2"
        }
        res = self.client.put("/user/1/update", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "Invalid username or password"}

        # test to update user with invalid email
        data = {
            "email": "t.testovvvv@abv.bg",
            "password": "Igrach123#PlayeR1",
            "new_email": "test.testov@abv.bg",
            "new_first_name": "Thetest",
            "new_last_name": "Testoviqt",
            "new_password": "Igrach123#PlayeR2",
            "retype_new_password": "Igrach123#PlayeR2"
        }
        res = self.client.put("/user/1/update", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "Invalid username or password"}

        # test to update user with new_password == password
        data = {
            "email": "t.testov@abv.bg",
            "password": "Igrach123#PlayeR1",
            "new_email": "test.testov@abv.bg",
            "new_first_name": "Thetest",
            "new_last_name": "Testoviqt",
            "new_password": "Igrach123#PlayeR2",
            "retype_new_password": "Igrach123#PlayeR3"
        }
        res = self.client.put("/user/1/update", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "New password and retype password do not match"}

        # test the happy case
        data = {
            "email": "t.testov@abv.bg",
            "password": "Igrach123#PlayeR1",
            "new_email": "test.testov@abv.bg",
            "new_first_name": "Thetest",
            "new_last_name": "Testoviqt",
            "new_password": "Igrach123#PlayeR2",
            "retype_new_password": "Igrach123#PlayeR2"
        }
        res = self.client.put("/user/1/update", headers=headers, json=data)
        assert res.status_code == 200
        assert res.json == {"message": "You successfully updated your email, password, first name and last name."}

    def test_delete_user(self):
        assert len(UserModel.query.all()) == 0
        user = UserFactory()
        admin = AdminFactory()
        assert len(UserModel.query.all()) == 1

        token = generate_token(admin)
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}

        # try to delete user who does not exist
        res = self.client.put("/user/2/delete", headers=headers)
        assert res.status_code == 400
        assert res.json == {"message": "User with id 2 doesn't exist!"}

        # admin successfully deletes the user
        res = self.client.put("/user/1/delete", headers=headers)
        assert res.status_code == 200
        assert res.json == {"message": "User with id 1 has been soft deleted successfully"}
        assert user.deleted is True

        # test deleted user tries to login raises error
        data = {"email": user.email,
                "password": user.password}
        headers = {"Content-Type": "application/json"}
        res = self.client.post("/user/login", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {"message": "Invalid username or password"}
