from resources.auth import RegisterUserResource, LoginUserResource
from resources.food import BasicSearchFoodResource, AdvancedSearchFoodResource
from resources.recipe import CreateRecipeResource

routes = (
    (RegisterUserResource, "/register"),
    (LoginUserResource, "/login"),
    (BasicSearchFoodResource, "/food/basic_search"),
    (AdvancedSearchFoodResource, "/food/advanced_search"),
    (CreateRecipeResource, "/recipe")
)
