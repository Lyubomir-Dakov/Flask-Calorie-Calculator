from resources.auth import RegisterUserResource, LoginUserResource, UpdateUserResource, DeleteUserResource
from resources.food import BasicSearchFoodResource, AdvancedSearchFoodResource
from resources.recipe import CreateRecipeResource, GetRecipesResource, DeleteRecipeResource, GetRecipeResource, \
    UpdateRecipeResource
from resources.subscription import CreateSubscriptionResource, PauseSubscriptionResource, ActivateSubscriptionResource, \
    CancelSubscriptionResource

routes = (
    (RegisterUserResource, "/user/register"),
    (LoginUserResource, "/user/login"),
    (UpdateUserResource, "/user/<int:pk>/update"),
    (DeleteUserResource, "/user/<int:pk>/delete"),

    (BasicSearchFoodResource, "/food/basic_search"),
    (AdvancedSearchFoodResource, "/food/advanced_search"),

    (CreateRecipeResource, "/recipe/create"),
    (GetRecipesResource, "/user/<int:pk>/recipes/get"),
    (GetRecipeResource, "/user/<int:pk>/recipe/get"),
    (DeleteRecipeResource, "/user/<int:pk>/recipe/delete"),
    (UpdateRecipeResource, "/user/<int:pk>/recipe/update"),

    (CreateSubscriptionResource, "/subscription/create"),
    (PauseSubscriptionResource, "/subscription/<int:pk>/pause"),
    (ActivateSubscriptionResource, "/subscription//<int:pk>/activate"),
    (CancelSubscriptionResource, "/subscription/<int:pk>/cancel")
)
