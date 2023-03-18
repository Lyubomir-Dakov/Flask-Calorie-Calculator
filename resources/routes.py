from resources.auth import RegisterUserResource, LoginUserResource
from resources.food import CreateFoodResource

routes = (
    (RegisterUserResource, '/register'),
    (LoginUserResource, '/login'),
    (CreateFoodResource, '/food/create')
)
