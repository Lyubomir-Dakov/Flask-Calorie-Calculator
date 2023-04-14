import json

import requests
from decouple import config


class PayPal_Service():
    def __init__(self):
        self.client_id = config("PAY_PAL_CALORIE_CALCULATOR_ID")
        self.secret = config("PAY_PAL_CALORIE_CALCULATOR_SECRET")

    # Token is valid for 9 hours
    def get_access_token(self):
        get_token_url = config("PAY_PAL_GET_ACCESS_TOKEN_URL")
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US",
            "Authorization": f"Basic {self.client_id}:{self.secret}"
        }
        body = {
            "grant_type": "client_credentials",
        }
        auth = (self.client_id, self.secret)

        response = requests.post(get_token_url, headers=headers, data=body, auth=auth)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            return access_token
        else:
            print("Failed to get access token. Status code:", response.status_code)
            return None

    def create_product(self, access_token):
        create_product_url = f"{config('PAY_PAL_SANDBOX_BASE_URL')}/v1/catalogs/products"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            "PayPal-Request-Id": f"PRODUCT-{config('PAY_PAL_REQUEST_ID')}"
        }
        body = {
            "name": "Calorie Calculator premium membership",
            "description": "A premium membership subscription for Calorie Calculator app"
        }

        json_body = json.dumps(body)
        response = requests.post(create_product_url, headers=headers, data=json_body)
        product_id = response.json()["id"]
        return f"product_id: {product_id}"

    # 12-month, fixed-price subscription
    # Includes a 15 USD set up fee per month and 15 USD initial fee
    def create_plan(self, access_token):
        create_plan_url = f"{config('PAY_PAL_SANDBOX_BASE_URL')}/v1/billing/plans"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "PayPal-Request-Id": f"PLAN-{config('PAY_PAL_REQUEST_ID')}"
        }
        body = {
            "product_id": config('PAY_PAL_PREMIUM_MEMBERSHIP_PRODUCT_ID'),
            "name": "Premium",
            "description": "Premium members are allowed to create their own recipes",
            "status": "ACTIVE",
            "billing_cycles": [
                {
                    "tenure_type": "REGULAR",
                    "sequence": 1,
                    "total_cycles": 12,
                    "pricing_scheme": {
                        "fixed_price": {
                            "value": "5",
                            "currency_code": "USD"
                        }
                    },
                    "frequency": {
                        "interval_unit": "MONTH",
                        "interval_count": 1
                    }
                }
            ],
            "payment_preferences": {
                "auto_bill_outstanding": True,
                "setup_fee": {
                    "value": "3",
                    "currency_code": "USD"
                }
            }
        }
        json_body = json.dumps(body)
        response = requests.post(url=create_plan_url, headers=headers, data=json_body)
        return response.json()

    def create_subscription(self, access_token):
        subscription_url = f"{config('PAY_PAL_SANDBOX_BASE_URL')}/v1/billing/subscriptions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            'Accept': 'application/json',
        }
        body = {
            "plan_id": config('PAY_PAL_PREMIUM_MEMBERSHIP_PLAN_ID'),
            "subscriber": {
                "email_address": "sb-n6ih725498596@personal.example.com",
                "name": {"given_name": "John", "surname": "Doe"}
            }
        }
        json_body = json.dumps(body)
        response = requests.post(url=subscription_url, headers=headers, data=json_body)
        return response.json()

    def activate_subscription(self, subscription_id, access_token):
        activate_subscription_url = f"{config('PAY_PAL_SANDBOX_BASE_URL')}/v1/billing/subscriptions/{subscription_id}/activate"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        body = {"reason": "Reactivating the subscription"}
        json_body = json.dumps(body)
        response = requests.post(activate_subscription_url, headers=headers, data=json_body)
        return response.json()

    def cancel_subscription(self, subscription_id, access_token):
        cancel_subscription_url = f"{config('PAY_PAL_SANDBOX_BASE_URL')}/v1/billing/subscriptions/{subscription_id}/cancel"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        body = {"reason": ""}
        json_body = json.dumps(body)
        response = requests.post(cancel_subscription_url, headers=headers, data=json_body)


if __name__ == "__main__":
    service = PayPal_Service()

    # 1) get access token
    access_token = service.get_access_token()
    print(f"access_token: {access_token}")

    # 2) create a product - premium membership
    # create_premium_membership_product_id = service.create_product(access_token)
    # print(create_premium_membership_product_id)

    # 3) create a subscription plan
    # create_premium_plan = service.create_plan(access_token)
    # print(create_premium_plan)

    # 4) create subscription
    # create_subscription = service.create_subscription(access_token)
    # print(create_subscription)
    # subscription_id = create_subscription['id']
    # print(f"subscription_id: {subscription_id}")

    # 5) cancel subscription
    cancel_subscription = service.cancel_subscription("I-4FJARSW525DV", access_token)
