from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash

from managers.auth import auth
from services.edamam import Edamam_Service
from services.open_ai import OpenAI_Service
from utils.validators import validate_if_email_already_exists


def find_macros_per_100_grams(food_data):
    return food_data["PROCNT"], food_data["FAT"], food_data["CHOCDF"], food_data["ENERC_KCAL"]


def find_macros_for_given_amount(amount, proteins_per_100g, carbs_per_100g, fats_per_100g, calories_per100g):
    proteins = (proteins_per_100g * float(amount)) / 100
    carbs = (carbs_per_100g * float(amount)) / 100
    fats = (fats_per_100g * float(amount)) / 100
    calories = (calories_per100g * float(amount)) / 100
    return proteins, carbs, fats, calories


def update_email(update_data, updated_data, user):
    if "new_email" in update_data:
        validate_if_email_already_exists(update_data["new_email"], user)
        user.email = update_data["new_email"]
        updated_data.append("email")
    return None


def update_password(update_data, updated_data, user):
    if "new_password" in update_data and not check_password_hash(user.password, update_data["new_password"]):
        user.password = generate_password_hash(password=update_data["new_password"], method="sha256")
        updated_data.append("password")
    return None


def update_first_name(update_data, updated_data, user):
    if "new_first_name" in update_data and not update_data["new_first_name"] == user.first_name:
        user.first_name = update_data["new_first_name"]
        updated_data.append("first name")
    return None


def update_last_name(update_data, updated_data, user):
    if "new_last_name" in update_data and not update_data["new_last_name"] == user.last_name:
        user.last_name = update_data["new_last_name"]
        updated_data.append("last name")
    return None


def updated_user_result_message(updated_data):
    if len(updated_data) == 0:
        return "The given data is the same as your current data"
    elif len(updated_data) == 1:
        return f"You successfully updated your {updated_data[0]}."
    else:
        return f"You successfully updated your {', '.join(updated_data[0:-1])} and {updated_data[-1]}."


def count_macronutrients_in_recipe(recipe_data):
    food_service = Edamam_Service()
    open_ai_service = OpenAI_Service()
    proteins = 0
    fats = 0
    carbs = 0
    calories = 0

    recipe_ingredients = list(recipe_data["ingredients"].keys())

    # when the recipe contains more than 7 ingredients Edamam_Service returns recipe_ingredients = []
    # split recipe_ingredients to smaller lists up to length = 7 and make request for every list
    split_lists = []
    edamam_limit = 7

    for i in range(0, len(recipe_ingredients), edamam_limit):
        split_lists.append(recipe_ingredients[i:i + edamam_limit])

    for piece in split_lists:
        foods = food_service.get_food_for_recipe(piece)
        if len(foods) < len(piece):
            raise BadRequest("This recipe contains incorrect ingredient name or it doesn't exists in the database!")
        i = 0
        for food in foods:
            food_data = food["food"]
            food_name = piece[i]
            food_amount = recipe_data["ingredients"][food_name]
            p, f, c, cal = find_macros_per_100_grams(food_data["nutrients"])
            p, c, f, cal = find_macros_for_given_amount(food_amount, p, c, f, cal)
            proteins += p
            fats += f
            carbs += c
            calories += cal
            i += 1

    recipe_data["photo_url"] = open_ai_service.create_image(recipe_data["title"])
    recipe_data["proteins"] = round(proteins, 2)
    recipe_data["fats"] = round(fats, 2)
    recipe_data["carbs"] = round(carbs, 2)
    recipe_data["calories"] = round(calories, 2)

    current_user = auth.current_user()
    recipe_data["creator_id"] = current_user.id
    return recipe_data
