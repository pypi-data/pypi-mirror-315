import requests
import os


class MokafaaClient:
    def __init__(self, base_url=None, client_id=None, client_secret=None,
                 environment=None, merchant_token=None, access_token=None):
        """
        Initialize the MokafaaClient with either parameters or environment variables.
        :param base_url: Base URL for the API
        :param client_id: Client ID for authentication
        :param client_secret: Client Secret for authentication
        :param environment: API environment (DEV or PROD)
        :param merchant_token: Merchant token for API calls
        :param access_token: Access token (optional, can be fetched dynamically)
        """
        self.base_url = base_url or os.getenv('MOKAFAA_API_BASE_URL')
        self.client_id = client_id or os.getenv('MOKAFAA_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('MOKAFAA_CLIENT_SECRET')
        self.environment = environment or os.getenv('MOKAFAA_ENVIRONMENT', 'DEV')
        self.merchant_token = merchant_token or os.getenv('MOKAFAA_MERCHANT_TOKEN')
        self.access_token = access_token  # Can be fetched later if not provided

        if not all([self.base_url, self.client_id, self.client_secret, self.merchant_token]):
            raise ValueError(
                "Missing required configuration. Ensure that base_url, client_id, "
                "client_secret, and merchant_token are provided either as parameters "
                "or through environment variables."
            )

    def get_oauth_token(self):
        """
        Fetch OAuth token for API authentication.
        """
        url = "https://gwt.alrajhibank.com.sa:9443/api-factory/sit/loyalty-redemption/oauth2/token"
        if self.environment.upper() == 'PROD':
            url = "https://dpw.alrajhibank.com.sa:9443/api-factory/prod/loyalty-redemption/oauth2/token"

        payload = {
            "grant_type": "client_credentials",
            "scope": "customer-authorization otp-validation redemption-transaction-reversal redemption-transactions",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()
            self.access_token = response.json().get("access_token")
            return self.access_token
        except requests.exceptions.HTTPError as e:
            error_content = e.response.json() if e.response.headers.get("Content-Type") == "application/json" else e.response.text
            raise Exception(f"Error during API request: {error_content}")

    def authorize_customer(self, mobile, access_token=None):
        """
        Authorize a customer based on their mobile number.
        """
        url = f"{self.base_url}/customer-authorization"
        access_token = access_token or self.access_token

        headers = {
            "Authorization": f"Bearer {access_token}",
            "merchantToken": self.merchant_token,
            "Content-Type": "application/json"
        }
        payload = {"mobile": mobile, "currency": "SAR", "lang": "ar"}
        return self._post_request(url, payload, headers)

    def redeem_points(self, otp_value, otp_token, amount, access_token=None):
        """
        Redeem loyalty points.
        """
        url = f"{self.base_url}/otp-validation"
        access_token = access_token or self.access_token

        headers = {
            "Authorization": f"Bearer {access_token}",
            "merchantToken": self.merchant_token,
            "Content-Type": "application/json"
        }
        payload = {
            "OTPValue": otp_value,
            "OTPToken": otp_token,
            "amount": amount,
            "language": "ar"
        }
        return self._post_request(url, payload, headers)

    def reverse_transaction(self, transaction_id):
        """
        Reverse a redemption transaction.
        """
        url = f"{self.base_url}/redemption-transaction-reversal"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "merchantToken": self.merchant_token,
            "Content-Type": "application/json"
        }
        payload = {"transactionID": transaction_id}
        return self._post_request(url, payload, headers)

    def _post_request(self, url, payload, headers):
        """
        Helper method to perform a POST request with error handling.
        """
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_content = e.response.json() if e.response.headers.get("Content-Type") == "application/json" else e.response.text
            raise Exception(f"Error during API request: {error_content}")
