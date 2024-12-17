[![Test and Deploy Python Wrapper](https://github.com/thelimeskies/ecraspay-sdk/actions/workflows/test-and-deploy-python.yml/badge.svg)](https://github.com/thelimeskies/ecraspay-sdk/actions/workflows/test-and-deploy-python.yml)



# ECRASPAY Python SDK [Alpha]

ECRASPAY SDK provides a convenient and Pythonic way to interact with the ECRASPAY API for managing payments and transactions. This package simplifies initiating and managing payments, such as card payments, USSD, bank transfers, and transaction verification.

---

## Features
- **Direct integration with the ECRASPAY API:**
  - **Transaction Management**:
    - Fetch transaction details and status.
    - Cancel transactions.
    - Verify transactions.

  - **Card Payments**:
    - Initiate card payments.
    - Submit and resend OTPs.
    - Fetch card transaction details.
    - Verify card payments.

  - **USSD Payments**:
    - Initiate USSD payments.
    - Retrieve a list of supported banks for USSD payments.

  - **Bank Transfers**:
    - Initialize bank transfers by requesting bank account details.

- **Checkout Payments**:
  - Initiate checkout transactions.
  - Verify checkout transactions.


---

## Installation

### Prerequisites

- Python 3.6 or later.

### Installation via pip

```bash
pip install ecraspay-py
```

---

## Usage

### Initialize the EcrasPay client

#### - Checkouts Payments

```python
```

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

- [ ] Finish Documentation
- [ ] Add examples
- [ ] Finish Tests
- [ ] Write and Document all Utility functions for the SDK(Django, Flask, FastAPI, Pure Python) - e.g. `get_device_details`, `encrypt_card`, `clean_phone_number`, `clean_amount`, `clean_email`, `clean_name`, `clean_transaction_id`.
