"""
This module provides the CheckoutAPI class for interacting with the checkout API endpoints.

Example:
    from ecraspay.checkout import Checkout

    api = Checkout(api_key="your_api_key", environment="sandbox")
    response = api.initiate_transaction(
        amount=1000,
        payment_reference="unique_ref_123",
        customer_name="John Doe",
        customer_email="johndoe@example.com",
        metadata={"order_id": "12345"}
    )
    print(response)
"""

from ecraspay.base import BaseAPI


class Checkout(BaseAPI):
    """
    A class for interacting with the Checkout API.
    """

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

    def verify_transaction(self, transaction_id: str) -> dict:
        """
        Verify a transaction.

        Args:
            transaction_id (str): Transaction ID.

        Returns:
            dict: API response.
        """
        return self._make_request(
            "GET", f"/payment/transaction/verify/{transaction_id}"
        )
