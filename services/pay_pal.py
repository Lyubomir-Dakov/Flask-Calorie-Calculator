import json

import requests
from decouple import config
from werkzeug.exceptions import BadRequest


class PayPal_Service():
    def __init__(self):
        self.client_id = config("PAY_PAL_CALORIE_CALCULATOR_ID")
        self.secret = config("PAY_PAL_CALORIE_CALCULATOR_SECRET")
        self.base_url = config("PAY_PAL_SANDBOX_BASE_URL")
        self.get_token_url = config("PAY_PAL_GET_ACCESS_TOKEN_URL")
        self.request_id = config('PAY_PAL_REQUEST_ID')
        self.premium_membership_product_id = config('PAY_PAL_PREMIUM_MEMBERSHIP_PRODUCT_ID')
        self.premium_membership_plan_id = config('PAY_PAL_PREMIUM_MEMBERSHIP_PLAN_ID')

    # Token is valid for 9 hours
    def get_access_token(self):
        get_token_url = self.get_token_url
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
        create_product_url = f"{self.base_url}/v1/catalogs/products"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            "PayPal-Request-Id": f"PRODUCT-{self.request_id}"
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
    # Includes a 5 USD fee per month and 5 USD initial fee
    def create_plan(self, access_token):
        create_plan_url = f"{self.base_url}/v1/billing/plans"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "PayPal-Request-Id": f"PLAN-{self.request_id}"
        }
        body = {
            "product_id": self.premium_membership_product_id,
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
        subscription_url = f"{self.base_url}/v1/billing/subscriptions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            'Accept': 'application/json',
        }
        body = {
            "plan_id": self.premium_membership_plan_id
        }
        json_body = json.dumps(body)
        response = requests.post(url=subscription_url, headers=headers, data=json_body)
        return response.json()["id"], response.json()["links"][0]["href"]

    def activate_subscription(self, subscription_id, access_token):
        activate_subscription_url = f"{self.base_url}/v1/billing/subscriptions/{subscription_id}/activate"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        body = {}
        json_body = json.dumps(body)
        try:
            response = requests.post(activate_subscription_url, headers=headers, data=json_body)
            if response.status_code == 204:
                return f"You successfully activated subscription with id '{subscription_id}'!"
        except Exception as ex:
            raise BadRequest("Something went wrong! You can reactivate only paused subscriptions!")

    def cancel_subscription(self, subscription_id, access_token):
        cancel_subscription_url = f"{self.base_url}/v1/billing/subscriptions/{subscription_id}/cancel"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        body = {"reason": ""}
        json_body = json.dumps(body)
        try:
            response = requests.post(cancel_subscription_url, headers=headers, data=json_body)
            if response.status_code == 204:
                return f"You successfully canceled subscription with id {subscription_id}!"
        except Exception as ex:
            raise BadRequest("Something went wrong! Invalid subscription id or access token!")

    def suspend_subscription(self, subscription_id, access_token):
        suspend_subscription_url = f"{self.base_url}/v1/billing/subscriptions/{subscription_id}/suspend"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        body = {"reason": "Just do it!"}
        json_body = json.dumps(body)
        try:
            response = requests.post(suspend_subscription_url, headers=headers, data=json_body)
            if response.status_code == 204:
                return f"Subscription with id '{subscription_id}' was successfully paused!"
        except Exception as ex:
            raise BadRequest("Something went wrong! Invalid subscription id or access token!")


if __name__ == "__main__":
    service = PayPal_Service()
    #
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

    # Activation works only of the subscription is already approved, then SUSPENDED
    # in order to activate it again
    # activate_subscription = service.activate_subscription("I-U08N473HHFB6", access_token)
    # print(activate_subscription)

    # 5) cancel subscription
    cancel_subscription = service.cancel_subscription("I-U08N473HHFB6", access_token)
    print(cancel_subscription)

    # 6) suspend subscription
    # suspend_subscription = service.suspend_subscription("I-U08N473HHFB6", access_token)
    # print(suspend_subscription)
