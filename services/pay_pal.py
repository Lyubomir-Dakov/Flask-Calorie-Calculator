import json

import requests
from decouple import config


class PayPal_Service():
    def __init__(self):
        self.sandbox_account = "sb-q2xxi25498399@business.example.com"
        self.account_password_number = "'_mv0h1N"
        self.account_phone = "3593682101"
        self.account_id = "75LKXXYQJR7WQ"
        self.account_type = "Business"

        self.client_id = "Aby3OYRV4nN9CQd-0JsFmw06I7ALxzvVfgvT0GYNyOMYmUDy-8Qh2zTu6dXL0WH-snT6y7P0pWbmHuiB"
        self.secret = "EI-D10HP7EAfO6Qz4WgYSgbalUvMP5q43Z-W2-diNJj_HpDYUACJThMnCQHYBSO77Bsi8wdlG9x-qI-5"
        self.return_url = "nativexo://paypalpay"

        self.user_email_id = "sb-n6ih725498596@personal.example.com"
        self.user_password = "DX#mN5^<"
        self.user_phone_number = "3597341739"
        self.user_account_id = "PZ7ESLJW45VS8"
        self.user_first_name = "John"
        self.user_last_name = "Doe"
        self.user_account_type = "Personal"

        self.headers = {
            "Content-Type": "application/json"
        }

        self.create_product_url = "https://api-m.sandbox.paypal.com/v1/catalogs/products"

        # self.headers = {
        #     "Content-Type: application/json",
        #     "Accept-Language: en_US"
        #     "Authorization: Bearer Access-Token",
        #     "PayPal-Request-Id: PRODUCT-18062020-001"
        # }

        self.body = {
            "name": "Video Streaming Service",
            "description": "A video streaming service",
            "type": "SERVICE",
            "category": "SOFTWARE",
            "image_url": "https://example.com/streaming.jpg",
            "home_url": "https://example.com/home"
        }

    # Token is valid for 9 hours
    def get_access_token(self):
        get_token_url = config("PAY_PAL_GET_ACCESS_TOKEN_URL")
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US",
            "Authorization": f"Basic {self.client_id}:{self.secret}"
        }
        payload = {
            "grant_type": "client_credentials",
        }
        auth = (self.client_id, self.secret)

        response = requests.post(get_token_url, headers=headers, data=payload, auth=auth)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            return access_token
        else:
            print("Failed to get access token. Status code:", response.status_code)
            return None

        # This is how the response looks like

    #  {
    # "scope":"https://uri.paypal.com/services/checkout/one-click-with-merchant-issued-token https://uri.paypal.com/services/invoicing https://uri.paypal.com/services/disputes/read-buyer https://uri.paypal.com/services/payments/realtimepayment https://uri.paypal.com/services/disputes/update-seller https://uri.paypal.com/services/payments/payment/authcapture openid https://uri.paypal.com/services/disputes/read-seller https://uri.paypal.com/services/payments/refund https://api.paypal.com/v1/vault/credit-card https://uri.paypal.com/services/billing-agreements https://api.paypal.com/v1/payments/.* https://uri.paypal.com/payments/payouts https://api.paypal.com/v1/vault/credit-card/.* https://uri.paypal.com/services/shipping/trackers/readwrite https://uri.paypal.com/services/subscriptions https://uri.paypal.com/services/applications/webhooks",
    # "access_token":"A21AAIrDxZEgoZXTZSSwCliuLZVZn6oADUcInu3y6Sej_xUNW0O2jQtaSVbRLExIMi_DwufaubMx4apkKESdhfeUIcHsyQewQ",
    # "token_type":"Bearer",
    # "app_id":"APP-80W284485P519543T",
    # "expires_in":32400,
    # "nonce":"2023-04-11T03:11:44Z6o4yXIiXY43wWofmpUW-qgUItXKUUnKGEwKWHZQkGQs"
    #  }

    def create_product(self):
        create_product_url = config("PAY_PAL_CREATE_PRODUCT_URL")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('PAY_PAL_ACCESS_TOKEN')}",
            "PayPal-Request-Id": f"PRODUCT-{config('PAY_PAL_REQUEST_ID')}"
        }
        payload = {
            "name": "Calorie Calculator premium membership",
            "description": "A premium membership subscription for Calorie Calculator app"
        }

        json_payload = json.dumps(payload)
        response = requests.post(create_product_url, headers=headers, data=json_payload)
        product_id = response.json()["id"]
        return product_id

    # 12-month, fixed-price subscription
    # Includes a 15 BGN set up fee per month
    def create_plan(self):
        create_plan_url = "https://api-m.sandbox.paypal.com/v1/billing/plans"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {config('PAY_PAL_ACCESS_TOKEN')}",
            "Content-Type": "application/json",
            "PayPal-Request-Id": f"PLAN-{config('PAY_PAL_REQUEST_ID')}"
        }
        payload = {
            "product_id": config('PAY_PAL_PREMIUM_MEMBERSHIP_PRODUCT_ID'),
            "name": "Premium membership",
            "description": "Premium members are allowed to create their own recipes",
            "billing_cycles": [
                {
                    "frequency": {
                        "interval_unit": "MONTH",
                        "interval_count": 1
                    },
                    "tenure_type": "REGULAR",
                    "sequence": 1,
                    "total_cycles": 12,
                    "pricing_scheme": {
                        "fixed_price": {
                            "value": "15",
                            "currency_code": "USD"
                        }
                    }
                }
            ],
            "payment_preferences": {
                "auto_bill_outstanding": True,
                "setup_fee": {
                    "value": "15",
                    "currency_code": "USD"
                }
            }
        }
        json_payload = json.dumps(payload)
        response = requests.post(url=create_plan_url, headers=headers, data=json_payload)
        return response.json()


if __name__ == "__main__":
    servive = PayPal_Service()
    access_token = servive.get_access_token()
    print(access_token)
    create_premuim_membership = servive.create_product()
    print(create_premuim_membership)
    premium_membership_data = servive.create_plan()
    print(premium_membership_data)

