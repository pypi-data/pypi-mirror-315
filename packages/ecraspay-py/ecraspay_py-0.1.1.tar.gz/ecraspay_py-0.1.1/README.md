[![Test and Deploy Python Wrapper](https://github.com/thelimeskies/ecraspay-sdk/actions/workflows/test-and-deploy-python.yml/badge.svg)](https://github.com/thelimeskies/ecraspay-sdk/actions/workflows/test-and-deploy-python.yml)



# ECRASPAY Python SDK [Alpha]


`ecraspay-py` is a Python wrapper for the ECRASPAY API, providing a seamless interface for initiating and managing payments via card, USSD, bank transfer, and checkout methods. It abstracts away the complexities of interacting with ECRASPAY's API endpoints, allowing you to focus on your application logic.

## Key Features

- **Card Payments**: 
  - Initiate card payments.
  - Submit and resend OTPs.
  - Verify card payments.
  - Fetch card transaction details.

- **USSD Payments**:
  - Initiate USSD payments.
  - Retrieve a list of supported banks for USSD payments.

- **Bank Transfers**:
  - Initialize bank transfer transactions.
  
- **Transaction Management**:
  - Initiate transactions.
  - Fetch transaction details.
  - Verify transactions.
  - Check transaction status.
  - Cancel transactions.

- **Checkout Payments**:
  - Initiate redirect-based checkout payments.
  - Verify checkout transactions.

- **Utility Functions**:
  - Store payment data.
  - Update payment statuses.
  - Dynamic service initialization.

- **Dynamic Initialization**:
  - Switch between `sandbox` and `live` environments easily.
  - Configure API keys via environment variables or during initialization.

---

## Installation

Install the package using `pip`:

```bash
pip install ecraspay-py
```

---

## Configuration

The wrapper supports two ways to pass your credentials:

1. **Environment Variables**:
   Set your API key and environment in your `.env` file:

   ```env
   ECRASPAY_API_KEY="your_api_key"
   ECRASPAY_ENVIRONMENT="sandbox"  # Use "live" for production
   ```

2. **Direct Initialization**:
   Pass the API key and environment directly during class instantiation.

   ```python
   from ecraspay import Checkout

   api = Checkout(api_key="your_api_key", environment="sandbox")
   ```

---

## Usage

### 1. **Checkout Payments**

```python
from ecraspay import Checkout

# Initialize the Checkout API
api = Checkout(api_key="your_api_key", environment="sandbox")

# Initiate a checkout transaction
response = api.initiate_transaction(
    amount=1000,
    payment_reference="txn_12345",
    customer_name="John Doe",
    customer_email="johndoe@example.com",
    redirect_url="https://example.com/redirect"
)

print("Checkout URL:", response["responseBody"]["checkoutUrl"])

# Verify a checkout transaction
verification = api.verify_transaction("txn_12345")
print("Verification Response:", verification)
```

### 2. **Card Payments**

```python
from ecraspay import Card
from ecraspay.utilities import card

payload =card.encrypt_card(pan="", cvv="", expiration="", pin="")

# Initialize the Card API
api = Card(api_key="your_api_key", environment="sandbox")

# Initiate a card payment
response = api.initiate_payment(
    card_payload=payload,
    transaction_ref="txn_12345",
    device_details={"device_id": "device_001", "ip_address": "192.168.1.1"}
)
print("Card Payment Response:", response)

# Submit OTP for the payment
otp_response = api.submit_otp(otp="123456", gateway_ref="gateway_001")
print("OTP Submission Response:", otp_response)

# Resend OTP
resend_response = api.resend_otp(gateway_ref="gateway_001")
print("OTP Resend Response:", resend_response)

# Verify card payment
verification = api.verify_card_payment(transaction_ref="txn_12345")
print("Card Payment Verification:", verification)

# Get card transaction details
details = api.get_card_details(transaction_ref="txn_12345")
print("Card Transaction Details:", details)
```

### 3. **USSD Payments**

```python
from ecraspay import USSD

# Initialize the USSD API
api = USSD(api_key="your_api_key", environment="sandbox")

# Initiate a USSD payment
response = api.initiate_ussd_payment(bank_name="Bank ABC", transaction_ref="txn_12345")
print("USSD Payment Response:", response)

# Get supported banks
banks = api.get_bank_list()
print("Supported Banks:", banks)
```

### 4. **Bank Transfers**

```python
from ecraspay import BankTransfer

# Initialize the Bank Transfer API
api = BankTransfer(api_key="your_api_key", environment="sandbox")

# Initialize a bank transfer transaction
response = api.initialize_bank_transfer(transaction_ref="txn_12345")
print("Bank Transfer Response:", response)
```

### 5. **Transaction Management**

```python
from ecraspay import Transaction

# Initialize the Transaction API
api = Transaction(api_key="your_api_key", environment="sandbox")

# Fetch transaction details
details = api.get_transaction_details(transaction_ref="txn_12345")
print("Transaction Details:", details)

# Verify a transaction
verification = api.verify_transaction(transaction_ref="txn_12345")
print("Transaction Verified:", verification)

# Fetch transaction status
status = api.get_transaction_status(transaction_ref="txn_12345")
print("Transaction Status:", status)

# Cancel a transaction
cancel_response = api.cancel_transaction(transaction_ref="txn_12345")
print("Transaction Canceled:", cancel_response)
```

### 6. **Utility Functions**

Utility functions are available for:
- **Storing Payments**: Custom implementation for storing transaction data.
- **Updating Payment Status**: Modify transaction status dynamically in your application.

Example:

```python
# Storing a payment record
service._store_payment(reference="txn_12345", amount=1000, status="initialized", metadata={})

# Updating a payment status
service._update_payment_status(reference="txn_12345", status="verified")
```

---

## Switching Environments

You can switch between `sandbox` and `live` environments easily by passing the environment parameter:

```python
api = Checkout(api_key="your_api_key", environment="live")
```

---

## Error Handling

`ecraspay-py` raises exceptions for any HTTP errors. Wrap your calls in try-except blocks to handle errors gracefully:

```python
from requests.exceptions import HTTPError
from ecraspay import Checkout

try:
    api = Checkout(api_key="your_api_key", environment="sandbox")
    response = api.initiate_transaction(
        amount=1000,
        payment_reference="txn_12345",
        customer_name="John Doe",
        customer_email="johndoe@example.com",
    )
    print(response)
except HTTPError as e:
    print(f"HTTP Error: {e.response.status_code} - {e.response.json()}")
```

---

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Clone your forked repository.
3. Create a new branch for your feature or fix.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run tests to ensure everything works:
   ```bash
   pytest
   ```
6. Push your changes and create a pull request.

---

## Running Tests

To run tests locally:

```bash
pytest tests/
```

---

## Support

For support or inquiries, contact [support@ecraspay.com](mailto:support@ecraspay.com).

---

## License

`ecraspay-py` is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Resources

- **ECRASPAY Documentation**: [API Docs](https://ecraspay.com/docs)
- **ECRASPAY Website**: [https://ecraspay.com](https://ecraspay.com)

---

## Version

**Latest Release**: 0.1.0

---

## Summary

`ecraspay-py` simplifies payment processing for Python developers, offering an intuitive interface for managing transactions, card payments, USSD payments, and bank transfers.

## Contributing

We welcome contributions to the ECRASPAY Python SDK! Whether you're fixing bugs, adding new features, or improving documentation, your contributions are highly appreciated.

### How to Contribute

1. **Fork the Repository**:
   - Navigate to the repository's GitHub page and click the **Fork** button.

2. **Clone Your Fork**:
   - Clone your fork to your local machine:
     ```bash
     git clone https://github.com/thelimeskies/ecraspay-sdk.git
     ```

3. **Create a Branch**:
   - Create a new branch for your feature or bugfix:
     ```bash
     git checkout -b feature-or-bugfix-name
     ```

4. **Make Your Changes**:
   - Implement your changes in the appropriate files.
   - Follow the project's coding standards and ensure your changes align with the rest of the codebase.

5. **Write Tests**:
   - Add tests for your changes to ensure functionality is maintained.
   - Use `pytest` to run the test suite:
     ```bash
     pytest
     ```

6. **Commit Your Changes**:
   - Commit your changes with a descriptive commit message:
     ```bash
     git commit -m "Add <feature-or-bugfix-name>"
     ```

7. **Push Your Branch**:
   - Push your branch to your forked repository:
     ```bash
     git push origin feature-or-bugfix-name
     ```

8. **Create a Pull Request**:
   - Go to the original repository on GitHub.
   - Click the **Pull Requests** tab, then click **New Pull Request**.
   - Select your branch and provide a detailed description of your changes.

---

### Contribution Guidelines

- Ensure your code follows the [PEP 8](https://pep8.org/) Python style guide.
- Write meaningful commit messages.
- Add or update documentation when necessary.
- Run all tests to verify your changes don't break existing functionality.

---

### Reporting Issues

If you encounter any issues or bugs, please create an issue on the [GitHub Issues](https://github.com/thelimeskies/ecraspay-sdk/issues) page with the following details:
- A clear and descriptive title.
- Steps to reproduce the issue.
- Expected and actual behavior.
- Any relevant logs or screenshots.

---

Thank you for contributing to ECRASPAY Python SDK!


## TODO

- [-] Finish Documentation
- [ ] Add examples
- [ ] Finish Tests
- [ ] Write and Document all Utility functions for the SDK(Django, Flask, FastAPI, Pure Python) - e.g. `get_device_details`, `encrypt_card`, `clean_phone_number`, `clean_amount`, `clean_email`, `clean_name`, `clean_transaction_id`.
