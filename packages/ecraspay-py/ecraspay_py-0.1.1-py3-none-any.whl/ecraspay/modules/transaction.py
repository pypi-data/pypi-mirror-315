"""
This module provides the Transaction class for interacting with
transaction-related API endpoints.

Example:
    from ecraspay.transaction import Transaction

    api = Transaction(api_key="your_api_key", environment="sandbox")
    # Fetch transaction details
    response = api.get_transaction_details(transaction_ref="txn_12345")
    print(response)

    # Initiate a new transaction
    response = api.initiate_transaction(
        amount=1000,
        payment_reference="txn_67890",
        customer_name="John Doe",
        customer_email="johndoe@example.com",
        metadata={"order_id": "67890"}
    )
    print(response)
"""

from ecraspay.base import BaseAPI


class Transaction(BaseAPI):
    """
    A class for managing transactions through the API.

    This class provides methods for fetching transaction details, verifying
    transactions, checking transaction status, canceling transactions, and
    initiating new transactions.
    """

    def get_transaction_details(self, transaction_ref: str) -> dict:
        """
        Fetch the details of a transaction.

        Args:
            transaction_ref (str): Unique reference for the transaction.

        Returns:
            dict: API response containing transaction details.
        """
        return self._make_request(
            method="GET", endpoint=f"/payment/details/{transaction_ref}"
        )

    def verify_transaction(self, transaction_ref: str) -> dict:
        """
        Verify the status of a transaction.

        Args:
            transaction_ref (str): Unique reference for the transaction.

        Returns:
            dict: API response confirming the transaction status.
        """
        return self._make_request(
            method="GET", endpoint=f"/payment/verify/{transaction_ref}"
        )

    def get_transaction_status(self, transaction_ref: str) -> dict:
        """
        Fetch the status of a transaction.

        Args:
            transaction_ref (str): Unique reference for the transaction.

        Returns:
            dict: API response containing the transaction status.
        """
        return self._make_request(
            method="GET", endpoint=f"/payment/status/{transaction_ref}"
        )

    def cancel_transaction(self, transaction_ref: str) -> dict:
        """
        Cancel a transaction.

        Args:
            transaction_ref (str): Unique reference for the transaction.

        Returns:
            dict: API response confirming the transaction cancellation.
        """
        return self._make_request(
            method="GET", endpoint=f"/payment/cancel/{transaction_ref}"
        )

    def initiate_transaction(
        self,
        amount: int,
        payment_reference: str,
        customer_name: str,
        customer_email: str,
        redirect_url: str = None,
        description: str = None,
        fee_bearer: str = None,
        currency: str = "usd",
        payment_method: str = "card",
        customer_phone: str = None,
        metadata: dict = None,
        **kwargs,
    ) -> dict:
        """
        Initiate a new transaction.

        Args:
            amount (int): Amount to be paid (smallest currency unit, e.g., usd for USD).
            payment_reference (str): Unique reference for the transaction.
            customer_name (str): Customer's name.
            customer_email (str): Customer's email.
            redirect_url (str, optional): URL to redirect the customer after payment.
            description (str, optional): Description of the transaction.
            fee_bearer (str, optional): Fee bearer ('customer' or 'merchant').
            currency (str, optional): Transaction currency (default: 'usd').
            payment_method (str, optional): Payment method (e.g., 'card').
            customer_phone (str, optional): Customer's phone number.
            metadata (dict, optional): Additional metadata for the transaction.
            **kwargs: Extra parameters to include in the transaction.

        Returns:
            dict: API response.
        """
        payload = {
            key: value
            for key, value in {
                "amount": amount,
                "paymentReference": payment_reference,
                "customerName": customer_name,
                "customerEmail": customer_email,
                "redirectUrl": redirect_url,
                "description": description,
                "feeBearer": fee_bearer,
                "currency": currency,
                "paymentMethods": payment_method,
                "customerPhoneNumber": customer_phone,
                "metadata": metadata,
            }.items()
            if value is not None
        }
        payload.update(kwargs)

        return self._make_request("POST", "/payment/initiate", data=payload)
