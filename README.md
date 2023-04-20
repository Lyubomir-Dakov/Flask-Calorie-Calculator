# Flask-Calorie-Calculator

## **REST API Calorie Calculator application**

## **Introduction:**
Flask-Calorie-Calculator is a REST API application that allows every user to get information about food - proteins, fats, carbs and calories per 100 grams.<br>
Food data is taken from EDAMAM nutrition database.<br>
Registered Users can pay via PayPal for subscription to become premium users. The application uses sandbox environment.<br>
As a premium, the users are allowed to perform advanced search for food with a given amount.<br>
Premium users are also able to create their own recipes and the application provides them information about macronutrients for the whole recipe.<br>
When a user search for food or create recipe, a picture url based on the food title or recipe title is generated through Open AI and returned to the user as response.<br>
The application is built using the Flask web framework and can be run on any Python environment with the required dependencies installed.<br>

## **The application has integrations with:**

EDAMAM - Leading provider of nutrition data and analytics: https://www.edamam.com/

PayPal - https://www.paypal.com

Open AI - https://platform.openai.com/

## **Install:**

    pip install -r requirements.txt

## **Run the app**

**Windows**

Open command prompt terminal

    set FLASK_APP=./main.py

**Linux/macOS**

    export FLASK_APP=main.py

## **Run the tests**

**Windows**

Navigate to the root directory of the application. Open the command prompt and execute 'pytest tests/'.

    pytest tests/

**Linux/macOS**

Navigate to the root directory of the application. Open the terminal and execute './run-tests.sh'.

    ./run-tests.sh
    
This will run all the test cases in the 'tests' directory.

## **REST API**

The REST API to the Calorie Calculator app is described below.

### **Register**

Request method **POST**

    curl http://127.0.0.1:5000/user/register
    -H "Content-Type: application/json"
    -d "first_name=Ivan
        &last_name=Georgiev
        &email=i.georgiev@abv.bg
        &password=$#@24vxcvf1%"
        
        
Response status **201**

    {
        "token": "access_token"
    }

### **Login**

Request method **POST**

    curl http://127.0.0.1:5000/user/login
    -H "Content-Type: application/json"
    -d "email=i.georgiev@abv.bg
        &password=$#@24vxcvf1%"
        
        
Response status **200**

    {
        "token": "access_token"
    }

### **Update user**

Every registered user is allowed to update his/her credentials.

Request method **PUT**

    curl http://127.0.0.1:5000/user/<int:pk>/update
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <access_token>"
    -d "email=i.georgiev@abv.bg
        &password=$#@24vxcvf1%
        &new_first_name=Vankata
        &new_last_name=Georgievich
        &new_email=v.georgievich@abv.bg
        &new_password=$#@24vxcvf1%2
        &retype_new_password=$#@24vxcvf1%2"
        
        
Response status **200**

    {
        "message": "You successfully updated your first name, last name, email and password."
    }

### **Delete user**

Only the admin is allowed to **SOFT** delete a user i.e. to change his/her status deleted=True. If the deleted user has subscription with status active/paused
the status of the subscription becomes canceled.

Request method **PUT**

    curl http://127.0.0.1:5000/user/<int:pk>/delete
    -H "Content-Type: application/json, Authorization: Bearer <access_token>"
    -d "email=i.georgiev@abv.bg
        &password=$#@24vxcvf1%
        &new_first_name=Vankata
        &new_last_name=Georgievich
        &new_email=v.georgievich@abv.bg
        &new_password=$#@24vxcvf1%2
        &retype_new_password=$#@24vxcvf1%2"
        
Response status **200**

    {
        "message": "User with id {pk} has been soft deleted successfully"
    }

### **Basic food search**
    
This is the public part of the application. Every user is allowed to use this resource including non registered/logged users.
    
Request method **GET**<br>
    
    curl http://127.0.0.1:5000/food/basic_search
    -H "Content-Type: application/json"
    -d "title=apple" 

Response status **200**
    
    {
        "calories_per_100g": 52.0,
        "carbs_per_100g": 13.81,
        "photo_url": "some_created_photo_url",
        "fats_per_100g": 0.17,
        "title": "apple",
        "proteins_per_100g": 0.26
    }

### **Advanced food search**
    
Every registerd and logged in user can search food by given title and amount.The user can be both basic or premium to perform this action. Non registered users have no access to this resource.
    
Request method **GET**
    
    curl http://127.0.0.1:5000/food/advanced_search
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <access_token>"
    -d "title=apple
        &amount=130"
    
Response status **200**
    
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

### **Create recipe**

Premium users can create their own recipes.

Request method **POST**

    curl http://127.0.0.1:5000/recipe/create
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <access_token>"
    -d "title=Big Caprice Salad,
       &ingredients={
            'tomatoes': 400,
            'mozzarella': 200,
            'basil leaves': 12,
            'olive oil': 30,
            'balsamic vinegar': 15,
            'salt': 2}"
            
Response status **201**

    {
        "photo_url": "some_created_photo_url",
        "carbs": 22.81,
        "created_on": "2023-04-20T10:37:03.059567",
        "proteins": 48.31,
        "id": 94,
        "ingredients": {
            "tomatoes": 400,
            "mozzarella": 200,
            "basil leaves": 12,
            "olive oil": 30,
            "balsamic vinegar": 15,
            "salt": 2
        },
        "creator_id": 67,
        "calories": 953.16,
        "updated_on": null,
        "fats": 75.58,
        "title": "Big Caprice Salad"
    }


### **Get your all recipes**

Premium users can get list of thei recipes

Request method **GET**

    curl http://127.0.0.1:5000/user/<int:pk>/recipes/get
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <access_token>"
    
Response status **200**

    [
        {"title": "Bulgarian Bean Soup"},
        {"title": "Very big Bulgarian Moussaka"},
        {"title": "Big Caprice Salad"}
    ]

### **Get one recipe**

Premium users can get information for one of their recipes

Request method **GET**

    curl http://127.0.0.1:5000/user/<int:pk>/recipe/get
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <access_token>"
    -d "title=Big Caprice Salad"

Response status **200**

    {
        "photo_url": "some_created_photo_url",
        "carbs": 22.81,
        "created_on": "2023-04-20T10:37:03.059567",
        "proteins": 48.31,
        "id": 94,
        "ingredients": {
            "tomatoes": 400,
            "mozzarella": 200,
            "basil leaves": 12,
            "olive oil": 30,
            "balsamic vinegar": 15,
            "salt": 2
        },
        "creator_id": 67,
        "calories": 953.16,
        "updated_on": null,
        "fats": 75.58,
        "title": "Big Caprice Salad"
    }

### **Update recipe**

Premium users can update their recipes

Request method **PUT**

    curl http://127.0.0.1:5000/user/<int:pk>/recipe/update
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <access_token>"
    -d "title=Big Caprice Salad,
        &new_title=Very Big Caprice Salad,
        &ingredients={
            'tomatoes': 4000,
            'mozzarella': 2000,
            'basil leaves': 120,
            'olive oil': 300,
            'balsamic vinegar': 150,
            'salt': 20}"
            
Response status **200**

    {
        "photo_url": "some_created_photo_url",
        "carbs": 228.12,
        "created_on": "2023-04-20T10:37:03.059567",
        "proteins": 483.11,
        "id": 94,
        "ingredients": {
            "tomatoes": 4000,
            "mozzarella": 2000,
            "basil leaves": 120,
            "olive oil": 300,
            "balsamic vinegar": 150,
            "salt": 20
        },
        "creator_id": 67,
        "calories": 9531.6,
        "updated_on": "2023-04-20T10:58:10.153839",
        "fats": 755.77,
        "title": "Very Big Caprece Salad"
    }
    
### **Delete recipe**

Premium users can delete recipe

Request method **DELETE**

    curl http://127.0.0.1:5000/user/<int:pk>/recipe/delete
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <access_token>"
    -d "title=Very Big Caprece Salad"

Response status **204**


### **Create subscription**

Basic user can subscribe via Paypal to become premium user. In response the user receives from paypal url to approve the subscription. 

Request method **POST**

    curl http://127.0.0.1:5000/subscription/create
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <access_token>"
    
Response status **201**

    {
        "subscription_data": {
            "initial_tax": 3,
            "subscriber_id": 67,
            "paypal_id": "I-SUVX4D1UH58F",
            "status": "active",
            "created_on": "2023-04-20T05:23:36.666082",
            "updated_on": null,
            "monthly_tax": 5,
            "id": 19,
            "title": "Premium membership"
        },
        "url to approve": "some_url_approve"
    }


### **Pause subscription**

Premium user can pause his/her subscription and become basic user.

Request method **PUT**

    curl http://127.0.0.1:5000/subscription/<int:pk>/pause
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <access_token>"
    -d "paypal_id=I-JYCMLT6FJH7J"
    
Response status **200**

    {
        "message": "Subscription with id 'I-JYCMLT6FJH7J' was successfully paused!"
    }


### **Activate subscription**

If a basic user has paused subscription he can activate it.

Request method **PUT**

    curl http://127.0.0.1:5000/subscription/<int:pk>/activate
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <access_token>"
    -d "paypal_id=I-JYCMLT6FJH7J"
    
Response status **200**

    {
        "message": "Subscription with id 'I-JYCMLT6FJH7J' was successfully activated!"
    }
    

### **Cancel subscription**

Premium user can cancel his/her subscription. If basic user has paused subscription he/she is allowed to cancel it.
Once a subscription is canceled it can never be activated again. If the user want to become premium he has to create new subscription and pay again.

Request method **PUT**

    curl http://127.0.0.1:5000/subscription/<int:pk>/cancel
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <access_token>"
    -d "paypal_id=I-JYCMLT6FJH7J"
    
Response status **200**

    {
        "message": "Subscription with id 'I-JYCMLT6FJH7J' was successfully canceled!"
    }



