import pytest
import requests
from unittest.mock import patch, MagicMock
from ecraspay.modules.checkout import Checkout


class TestCheckout:
    @pytest.fixture
    def checkout_instance(self):
        """Fixture to initialize the Checkout class."""

        class MockCheckout(Checkout):
            def __init__(self):
                self.base_url = "https://sandbox.api.example.com"
                self.api_key = "test_key"

            def _get_headers(self):
                return {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }

        return MockCheckout()

    @patch("requests.request")
    def test_initiate_transaction(self, mock_request, checkout_instance):
        """Test the initiate_transaction method with required fields."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "transaction_id": "12345",
        }
        mock_request.return_value = mock_response

        # Call the method
        response = checkout_instance.initiate_transaction(
            amount=1000,
            payment_reference="unique_ref_123",
            customer_name="John Doe",
            customer_email="johndoe@example.com",
            metadata={"order_id": "12345"},
        )

        # Assertions
        assert response == {"status": "success", "transaction_id": "12345"}

        # Verify the correct call to requests
        expected_payload = {
            "amount": 1000,
            "payment_reference": "unique_ref_123",
            "customer_name": "John Doe",
            "customer_email": "johndoe@example.com",
            "metadata": {"order_id": "12345"},
        }

        mock_request.assert_called_once_with(
            "POST",
            "https://sandbox.api.example.com/checkout/initiate",
            headers={
                "Authorization": "Bearer test_key",
                "Content-Type": "application/json",
            },
            json=expected_payload,
            params=None,
            timeout=10,
        )

        # Assertions
        assert response == {"status": "success", "transaction_id": "12345"}

        # Verify that the correct request was made
        mock_request.assert_called_once_with(
            "POST",
            "https://sandbox.api.example.com/checkout/initiate",
            headers={
                "Authorization": "Bearer test_key",
                "Content-Type": "application/json",
            },
            json={
                "amount": 1000,
                "payment_reference": "unique_ref_123",
                "customer_name": "John Doe",
                "customer_email": "johndoe@example.com",
                "metadata": {"order_id": "12345"},
            },
            params=None,
            timeout=10,
        )

    @patch("requests.request")
    def test_initiate_transaction_with_optional_fields(
        self, mock_request, checkout_instance
    ):
        """Test the initiate_transaction method with optional fields."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "transaction_id": "67890",
        }
        mock_request.return_value = mock_response

        # Call the method with optional fields
        response = checkout_instance.initiate_transaction(
            amount=2000,
            payment_reference="unique_ref_456",
            customer_name="Jane Doe",
            customer_email="janedoe@example.com",
            redirect_url="https://example.com/redirect",
            description="Test transaction",
            metadata={"order_id": "67890"},
        )

        # Assertions
        assert response == {"status": "success", "transaction_id": "67890"}

        # Verify that the correct request was made
        mock_request.assert_called_once_with(
            "POST",
            "https://sandbox.api.example.com/checkout/initiate",
            headers={
                "Authorization": "Bearer test_key",
                "Content-Type": "application/json",
            },
            json={
                "amount": 2000,
                "payment_reference": "unique_ref_456",
                "customer_name": "Jane Doe",
                "customer_email": "janedoe@example.com",
                "redirect_url": "https://example.com/redirect",
                "description": "Test transaction",
                "metadata": {"order_id": "67890"},
            },
            params=None,
            timeout=10,
        )

    @patch("requests.request")
    def test_initiate_transaction_http_error(self, mock_request, checkout_instance):
        """Test the initiate_transaction method when an HTTP error occurs."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Bad Request"
        )
        mock_request.return_value = mock_response

        with pytest.raises(requests.exceptions.HTTPError):
            checkout_instance.initiate_transaction(
                amount=1000,
                payment_reference="unique_ref_123",
                customer_name="John Doe",
                customer_email="johndoe@example.com",
            )

    @patch("requests.request")
    def test_initiate_transaction_invalid_json(self, mock_request, checkout_instance):
        """Test the initiate_transaction method with invalid JSON response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Not JSON"
        mock_response.json.side_effect = ValueError
        mock_request.return_value = mock_response

        with pytest.raises(ValueError, match="Failed to parse response as JSON."):
            checkout_instance.initiate_transaction(
                amount=1000,
                payment_reference="unique_ref_123",
                customer_name="John Doe",
                customer_email="johndoe@example.com",
            )
