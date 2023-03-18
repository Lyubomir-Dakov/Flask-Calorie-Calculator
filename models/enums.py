import enum


class RoleType(enum.Enum):
    user = "user"
    staff = "staff"
    admin = "admin"


class FoodType(enum.Enum):
    grain = "grain"
    vegetable = "vegetable"
    fruit = "fruit"
    meat_and_other_proteins = "meat_and_other_proteins"
    milk_product = "milk_product"
    nut = "nut"
