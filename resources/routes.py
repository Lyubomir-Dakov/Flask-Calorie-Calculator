from resources.auth import RegisterUserResource, LoginUserResource, UpdateUserResource, DeleteUserResource
from resources.food import BasicSearchFoodResource, AdvancedSearchFoodResource
from resources.recipe import CreateRecipeResource

routes = (
    (RegisterUserResource, "/user/register"),
    (LoginUserResource, "/user/login"),
    (UpdateUserResource, "/user/<int:pk>/update"),
    (DeleteUserResource, "/user/delete"),
    (BasicSearchFoodResource, "/food/basic_search"),
    (AdvancedSearchFoodResource, "/food/advanced_search"),
    (CreateRecipeResource, "/recipe")
)
