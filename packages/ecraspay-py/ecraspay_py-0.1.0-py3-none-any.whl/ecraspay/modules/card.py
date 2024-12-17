"""
This module provides the Card class for interacting with card payment-related API 
endpoints.

Example:
    from ecraspay.card import Card

    api = Card(api_key="your_api_key", environment="sandbox")
    # Initiate a card payment
    response = api.initiate_payment(
        card_payload="encrypted_card_data",
        transaction_ref="txn_12345",
        device_details={"device_id": "device_001", "ip_address": "192.168.1.1"}
    )
    print(response)
"""

from ecraspay.base import BaseAPI


class Card(BaseAPI):
    """
    A class for managing card payment operations through the API.

    This class provides methods for initializing card payments, submitting OTPs,
    resending OTPs, fetching card details, and verifying payments.
    """

    def initiate_payment(
        self, card_payload: str, transaction_ref: str, device_details: dict
    ) -> dict:
        """
        Initiates a card payment.

        Args:
            card_payload (str): Encrypted card details payload.
            transaction_ref (str): Unique reference for the transaction.
            device_details (dict): Details of the device initiating the transaction.

        Returns:
            dict: The API response containing transaction initialization details.

        Example:
            response = api.initiate_payment(
                card_payload="encrypted_card_data",
                transaction_ref="txn_12345",
                device_details={"device_id": "device_001", "ip_address": "192.168.1.1"}
            )
            print(response)
        """
        payload = {
            "payload": card_payload,
            "transactionReference": transaction_ref,
            "deviceDetails": device_details,
        }

        return self._make_request(
            method="POST",
            endpoint="/payment/cards/initialize",
            data=payload,
        )

    def submit_otp(self, otp: str, gateway_ref: str) -> dict:
        """
        Submits an OTP for a card payment.

        Args:
            otp (str): The One-Time Password (OTP) provided by the user.
            gateway_ref (str): Reference to the payment gateway.

        Returns:
            dict: The API response confirming OTP submission.

        Example:
            response = api.submit_otp(otp="123456", gateway_ref="gateway_001")
            print(response)
        """
        payload = {
            "otp": otp,
            "gatewayReference": gateway_ref,
        }

        return self._make_request(
            method="POST",
            endpoint="/payment/cards/otp/submit/",
            data=payload,
        )

    def resend_otp(self, gateway_ref: str) -> dict:
        """
        Resends the OTP for a card payment.

        Args:
            gateway_ref (str): Reference to the payment gateway.

        Returns:
            dict: The API response confirming the OTP resend request.

        Example:
            response = api.resend_otp(gateway_ref="gateway_001")
            print(response)
        """
        payload = {
            "gatewayReference": gateway_ref,
        }

        return self._make_request(
            method="POST",
            endpoint="/payment/cards/otp/resend/",
            data=payload,
        )

    def get_card_details(self, transaction_ref: str) -> dict:
        """
        Retrieves details of a card transaction.

        Args:
            transaction_ref (str): Unique reference for the transaction.

        Returns:
            dict: The API response containing card transaction details.

        Example:
            response = api.get_card_details(transaction_ref="txn_12345")
            print(response)
        """
        return self._make_request(
            method="GET",
            endpoint=f"/payment/cards/details/{transaction_ref}",
        )

    def verify_card_payment(self, transaction_ref: str) -> dict:
        """
        Verifies the status of a card payment.

        Args:
            transaction_ref (str): Unique reference for the transaction.

        Returns:
            dict: The API response confirming the payment status.

        Example:
            response = api.verify_card_payment(transaction_ref="txn_12345")
            print(response)
        """
        payload = {
            "transactionReference": transaction_ref,
        }

        return self._make_request(
            method="POST",
            endpoint="/payment/cards/verify/",
            data=payload,
        )
