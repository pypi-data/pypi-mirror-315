"""
This module provides the USSD class for interacting with USSD payment-related 
API endpoints.

Example:
    from ecraspay.ussd import USSD

    api = USSD(api_key="your_api_key", environment="sandbox")
    
    # Initiate a USSD payment
    response = api.initiate_ussd_payment(bank_name="Bank ABC", transaction_ref="txn_12345")
    print(response)

    # Get the list of supported banks
    response = api.get_bank_list()
    print(response)
"""

from ecraspay.base import BaseAPI


class USSD(BaseAPI):
    """
    A class for managing USSD payment operations through the API.

    This class provides methods for initiating USSD payments and retrieving the list of supported banks.
    """

    def initiate_ussd_payment(self, bank_name: str, transaction_ref: str) -> dict:
        """
        Initiate a USSD payment by requesting a USSD code for a specific bank.

        Args:
            bank_name (str): Name of the bank to process the USSD payment.
            transaction_ref (str): Unique reference for the transaction.

        Returns:
            dict: The API response containing the USSD code and payment instructions.

        Example:
            response = api.initiate_ussd_payment(bank_name="Bank ABC", transaction_ref="txn_12345")
            print(response)
        """
        payload = {
            "bank_name": bank_name,
        }

        return self._make_request(
            method="POST",
            endpoint=f"/payment/ussd/request-ussd-code/{transaction_ref}",
            data=payload,
        )

    def get_bank_list(self) -> dict:
        """
        Retrieve the list of banks that support USSD payments.

        Returns:
            dict: The API response containing the list of supported banks.

        Example:
            response = api.get_bank_list()
            print(response)
        """
        return self._make_request(
            method="GET",
            endpoint="/payment/ussd/supported-banks",
        )
