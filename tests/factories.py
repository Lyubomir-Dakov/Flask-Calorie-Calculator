import factory

from db import db
from models import UserModel, AdminModel, SubscriptionModel, RecipeModel


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.commit()
        return object


class UserFactory(BaseFactory):
    class Meta:
        model = UserModel

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class AdminFactory(BaseFactory):
    class Meta:
        model = AdminModel

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


def get_user_id():
    user = UserFactory()
    return user.id


class SubscriptionFactory(BaseFactory):
    class Meta:
        model = SubscriptionModel

    paypal_id = "some_paypal_id"
    subscriber_id = factory.LazyFunction(get_user_id)


class RecipeFactory(BaseFactory):
    class Meta:
        model = RecipeModel

    title = "Caprice Salad"
    ingredients = {"tomatoes": 400,
                   "mozzarella": 200,
                   "basil leaves": 12,
                   "olive oil": 30,
                   "balsamic vinegar": 15,
                   "salt": 2}
    proteins = 48.31
    fats = 75.58
    carbs = 22.81
    calories = 953.16
    creator_id = factory.LazyFunction(get_user_id)
    photo_url = "some_photo_url"
