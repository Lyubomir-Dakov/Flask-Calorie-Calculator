def find_macros_per_100_grams(food_data):
    return food_data["PROCNT"], food_data["FAT"], food_data["CHOCDF"], food_data["ENERC_KCAL"]


def find_macros_for_given_amount(amount, proteins_per_100g, carbs_per_100g, fats_per_100g, calories_per100g):
    proteins = (proteins_per_100g * float(amount)) / 100
    carbs = (carbs_per_100g * float(amount)) / 100
    fats = (fats_per_100g * float(amount)) / 100
    calories = (calories_per100g * float(amount)) / 100
    return proteins, carbs, fats, calories
