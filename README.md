# Flask-Calorie-Calculator

## **REST API Calorie Calculator application**

### **Introduction:**
Flask-Calorie-Calculator is a REST API application that allows every user to get information about food - proteins, fats, carbs and calories per 100 grams.<br>
Food data is taken from EDAMAM nutrition database.<br>
Registered Users can pay via PayPal for subscription to become premium users. The application uses sandbox environment.<br>
As a premium, the users are allowed to perform advanced search for food with a given amount.<br>
Premium users are also able to create their own recipes and the application provides them information about macronutrients for the whole recipe.<br>
When a user search for food or create recipe, a picture url based on the food title or recipe title is generated through Open AI and returned to the user as response.<br>
The application is built using the Flask web framework and can be run on any Python environment with the required dependencies installed.<br>

### **The application has integrations with:**<br>
- EDAMAM - Leading provider of nutrition data and analytics: https://www.edamam.com/<br>
- PayPal - https://www.paypal.com<br>
- Open AI - https://platform.openai.com/<br>

### **Install:**
pip install -r requirements.txt

### **Run the app**

- **Windows**<br>
    Open command prompt terminal<br>
    set FLASK_APP=./main.py

- **Linux/macOS**<br>
    export FLASK_APP=main.py

**Run the tests**

Windows
Navigate to the root directory of the application.
Open the command prompt and execute 'pytest tests/'. This will run all the test cases in the 'tests' directory.

**Linux/macOS**
Navigate to the root directory of the application.
Open the terminal and execute './run-tests.sh'. This will run all the test cases in the tests directory.

**REST API**

The REST API to the Calorie Calculator app is described below.

Register
Request method POST
curl -i -H 'Content-Type: application/json'
        -d 'first_name=Ivan&last_name=Georgiev&email=i.georgiev@abv.bg&password=$#@24vxcvf1%'
        http://127.0.0.1:5000/user/register
Response
{"token": token}

Login
Request method POST
curl -i -H 'Content-Type: application/json'
        -d 'email=i.georgiev@abv.bg&password=$#@24vxcvf1%'
        http://127.0.0.1:5000/user/login
Response
{"token": token}

Update user
Every registered user is allowed to update his/her credentials
Request method PUT
curl -i -H 'Content-Type: application/json, Authorization: Bearer <access_token>'
        -d 'email=i.georgiev@abv.bg
        &password=$#@24vxcvf1%'
        &new_first_name=Vankata
        &new_last_name=Georgievich
        &new_email=v.georgievich@abv.bg
        &new_password=$#@24vxcvf1%2
        &retype_new_password=$#@24vxcvf1%2
        http://127.0.0.1:5000/food/advanced_search
Response
{"message": "You successfully updated your first name, last name, email and password."}

Delete user
Only the admin is allowed to SOFT deleted a user i.e. to change his/her status deleted=True. If the deleted user has subscription with status active/paused
the status becomes canceled
Request method PUT
curl -i -H 'Content-Type: application/json, Authorization: Bearer <access_token>'
        -d 'email=i.georgiev@abv.bg
        &password=$#@24vxcvf1%'
        &new_first_name=Vankata
        &new_last_name=Georgievich
        &new_email=v.georgievich@abv.bg
        &new_password=$#@24vxcvf1%2
        &retype_new_password=$#@24vxcvf1%2
        http://127.0.0.1:5000/user/<user id to delete>/delete
Response
{"message": "User with id {pk} has been soft deleted successfully"}

Basic food search
This is the public part of the application. Every user is allowed to use this resource including non registered/logged users
Request method GET
curl -i -H 'Content-Type: application/json' -d 'title=apple' http://127.0.0.1:5000/food/basic_search
Response
{
    "calories_per_100g": 52.0,
    "carbs_per_100g": 13.81,
    "photo_url": "some_created_photo_url",
    "fats_per_100g": 0.17,
    "title": "apple",
    "proteins_per_100g": 0.26
}

Advanced food search
Every registerd and logged in user can search food by given title and amount
The user can be both basic or premium to perform this action. Non registered users have no access to this resource.
Request method GET
curl -i -H 'Content-Type: application/json, Authorization: Bearer <access_token>' -d 'title=apple&amount=130' http://127.0.0.1:5000/food/advanced_search
Response
{
    "photo_url": "some_created_photo_url",
    "fats_per_100g": 0.17,
    "carbs": 17.95,
    "proteins": 0.34,
    "carbs_per_100g": 13.81,
    "calories": 67.6,
    "proteins_per_100g": 0.26,
    "fats": 0.22,
    "calories_per_100g": 52.0,
    "title": "apple",
    "amount": 130.0
}

Create recipe

Get your all recipes

Get one recipe

Update recipe

Delete recipe

Create subscription

Pause subscription

Activate subscription

Cancel subscription

