"""
This module provides the BankTransfer class for interacting with the bank transfer
API endpoints.

Example:
    from ecraspay.bank_transfer import BankTransfer

    api = BankTransfer(api_key="your_api_key", environment="sandbox")

    # Initialize a bank transfer
    response = api.initialize_bank_transfer(
        transaction_ref="txn_12345"
    )
    print(response)
"""

from ecraspay.base import BaseAPI


class BankTransfer(BaseAPI):
    """
    A class for managing bank transfer operations through the API.

    This class provides a method to initialize bank transfers by requesting
    bank account details for a given transaction reference.
    """

    def initialize_bank_transfer(self, transaction_ref: str) -> dict:
        """
        Initialize a bank transfer by requesting bank account details.

        Args:
            transaction_ref (str): Unique reference for the transaction.

        Returns:
            dict: The API response containing the bank account details
            for the transfer.

        Example:
            response = api.initialize_bank_transfer(
                transaction_ref="txn_12345"
            )
            print(response)
        """
        return self._make_request(
            method="GET",
            endpoint=(
                f"/payment/bank-transfer/request-bank-account/" f"{transaction_ref}"
            ),
        )
