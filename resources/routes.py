from resources.auth import RegisterUserResource, LoginUserResource, UpdateUserResource, DeleteUserResource
from resources.food import BasicSearchFoodResource, AdvancedSearchFoodResource
from resources.recipe import CreateRecipeResource, GetRecipesResource, DeleteRecipeResource, GetRecipeResource

routes = (
    (RegisterUserResource, "/user/register"),
    (LoginUserResource, "/user/login"),
    (UpdateUserResource, "/user/<int:pk>/update"),
    (DeleteUserResource, "/user/<int:pk>/delete"),

    (BasicSearchFoodResource, "/food/basic_search"),
    (AdvancedSearchFoodResource, "/food/advanced_search"),

    (CreateRecipeResource, "/recipe"),
    (GetRecipesResource, "/recipes/<int:pk>/get"),
    (GetRecipeResource, "/recipe/<int:pk>/get"),
    (DeleteRecipeResource, "/recipe/<int:pk>/delete"),
)
