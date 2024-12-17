import unittest
from unittest.mock import patch, MagicMock
from mokafaa_client.client import MokafaaClient

class TestMokafaaClient(unittest.TestCase):
    def setUp(self):
        # Initialize the client with test parameters
        self.client = MokafaaClient(
            base_url="https://api.test.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
            environment="DEV",
            merchant_token="test-merchant-token"
        )

    @patch("requests.post")
    def test_get_oauth_token(self, mock_post):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "test-access-token"}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        # Call the method
        token = self.client.get_oauth_token()

        # Assertions
        self.assertEqual(token, "test-access-token")
        mock_post.assert_called_once_with(
            "https://gwt.alrajhibank.com.sa:9443/api-factory/sit/loyalty-redemption/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "scope": "customer-authorization otp-validation redemption-transaction-reversal redemption-transactions",
                "client_id": "test-client-id",
                "client_secret": "test-client-secret"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    @patch("requests.post")
    def test_authorize_customer(self, mock_post):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success", "customerID": "12345"}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        # Call the method
        response = self.client.authorize_customer(mobile="0555555555", access_token="test-access-token")

        # Assertions
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["customerID"], "12345")
        mock_post.assert_called_once_with(
            "https://api.test.com/customer-authorization",
            json={"mobile": "0555555555", "currency": "SAR", "lang": "ar"},
            headers={
                "Authorization": "Bearer test-access-token",
                "merchantToken": "test-merchant-token",
                "Content-Type": "application/json"
            }
        )

    @patch("requests.post")
    def test_redeem_points(self, mock_post):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success", "transactionID": "txn123"}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        # Call the method
        response = self.client.redeem_points(otp_value="123456", otp_token="otp-token", amount=100)

        # Assertions
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["transactionID"], "txn123")
        mock_post.assert_called_once_with(
            "https://api.test.com/otp-validation",
            json={
                "OTPValue": "123456",
                "OTPToken": "otp-token",
                "amount": 100,
                "language": "ar"
            },
            headers={
                "Authorization": f"Bearer {self.client.access_token}",
                "merchantToken": "test-merchant-token",
                "Content-Type": "application/json"
            }
        )

    @patch("requests.post")
    def test_reverse_transaction(self, mock_post):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "reversed"}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        # Call the method
        response = self.client.reverse_transaction(transaction_id="txn123")

        # Assertions
        self.assertEqual(response["status"], "reversed")
        mock_post.assert_called_once_with(
            "https://api.test.com/redemption-transaction-reversal",
            json={"transactionID": "txn123"},
            headers={
                "Authorization": f"Bearer {self.client.access_token}",
                "merchantToken": "test-merchant-token",
                "Content-Type": "application/json"
            }
        )

    @patch("requests.post")
    def test_error_handling(self, mock_post):
        # Simulate an API error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Test Error")
        mock_response.json.return_value = {"error": "Invalid request"}
        mock_post.return_value = mock_response

        # Call the method and expect an exception
        with self.assertRaises(Exception) as context:
            self.client.get_oauth_token()

        # Assertions
        self.assertIn("Error during API request", str(context.exception))
        mock_post.assert_called_once()

if __name__ == "__main__":
    unittest.main()

