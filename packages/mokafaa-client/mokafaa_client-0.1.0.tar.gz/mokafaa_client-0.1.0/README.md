### **`README.md`**

```markdown
# Mokafaa Client

A Python client for interacting with the Mokafaa loyalty API. This library provides an easy-to-use interface for operations such as fetching OAuth tokens, authorizing customers, redeeming loyalty points, and reversing transactions.

---

## Installation

You can install the package using pip:

```bash
pip install mokafaa-client
```

---

## Features

The Mokafaa Client provides the following key functionalities:

1. **Fetch OAuth Token**: Obtain an access token using client credentials.
2. **Authorize a Customer**: Validate and register a customer's mobile number.
3. **Redeem Loyalty Points**: Process loyalty point redemptions using OTP-based verification.
4. **Reverse a Transaction**: Rollback or reverse a redemption transaction.

All operations support both development (`DEV`) and production (`PROD`) environments, configured using parameters or environment variables.

---

## Usage

The `MokafaaClient` can be initialized by passing parameters or by using environment variables.

### Initialization

#### Example with Parameters:
```python
from mokafaa_client import MokafaaClient

client = MokafaaClient(
    base_url="https://api.mokafaa.com",
    client_id="your-client-id",
    client_secret="your-client-secret",
    environment="DEV",  # Use 'PROD' for production
    merchant_token="your-merchant-token"
)
```

#### Example with Environment Variables:
Set the required environment variables:
```bash
export MOKAFAA_API_BASE_URL="https://api.mokafaa.com"
export MOKAFAA_CLIENT_ID="your-client-id"
export MOKAFAA_CLIENT_SECRET="your-client-secret"
export MOKAFAA_ENVIRONMENT="DEV"
export MOKAFAA_MERCHANT_TOKEN="your-merchant-token"
```

Then initialize:
```python
from mokafaa_client import MokafaaClient

client = MokafaaClient()
```

---

### Fetch OAuth Token
This method retrieves an access token using the provided client credentials.

```python
token = client.get_oauth_token()
print(f"Access Token: {token}")
```

---
### URLS 
SIT
https://gwt.alrajhibank.com.sa:9443/api-factory/sit/blu-loyalty/1.0.0

PROD
https://dpw.alrajhibank.com.sa:9443/api-factory/prod/blu-loyalty/1.0.0


### Authorize a Customer
Authorize a customer by their mobile number. This returns the customer's unique identifier if successful.

```python
response = client.authorize_customer(mobile="0555555555")
print(response)
```

Example Response:
```json
{
  "status": "success",
  "customerID": "12345"
}
```

---

### Redeem Loyalty Points
Redeem loyalty points using OTP verification. You need the OTP value, OTP token, and the amount to redeem.

```python
response = client.redeem_points(
    otp_value="123456",
    otp_token="otp-token",
    amount=100
)
print(response)
```

Example Response:
```json
{
  "status": "success",
  "transactionID": "txn123"
}
```

---

### Reverse a Transaction
Reverse a redemption transaction using the transaction ID.

```python
response = client.reverse_transaction(transaction_id="txn123")
print(response)
```

Example Response:
```json
{
  "status": "reversed"
}
```

---

## Development

### Running Tests
Unit tests are provided to verify the functionality of the `MokafaaClient`. Use the following commands to run the tests:

#### Using `unittest`:
```bash
python -m unittest discover tests
```

#### Using `pytest`:
```bash
pytest tests/
```

---

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your fork.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Links

- **Source Code**: [GitHub Repository](https://github.com/ahmad18189/mokafaa-client)
- **Issue Tracker**: [Report Issues](https://github.com/ahmad18189/mokafaa-client/issues)
```

---

### Key Enhancements:
1. **Features Section**:
   - Expanded explanation of available features.
   - Aligned with the methods provided in `MokafaaClient`.

2. **Usage Section**:
   - Detailed examples for each feature.
   - Includes expected responses for better clarity.


