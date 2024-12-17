import pytest
from unittest.mock import patch, MagicMock
from ecraspay.base import BaseAPI
import requests


class TestBaseAPI:
    @pytest.fixture
    def base_api_instance(self):
        """Fixture to initialize the BaseAPI class."""

        class MockBaseAPI(BaseAPI):
            def __init__(self):
                self.base_url = "https://sandbox.api.example.com"
                self.api_key = "test_key"

            def _get_headers(self):
                return {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }

        return MockBaseAPI()

    @patch("requests.request")
    def test_make_request_success(self, mock_request, base_api_instance):
        """Test a successful API request."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_request.return_value = mock_response

        # Call the method
        response = base_api_instance._make_request(
            "GET", "test-endpoint", params={"key": "value"}
        )

        # Assertions
        assert response == {"status": "success"}
        mock_request.assert_called_once_with(
            "GET",
            "https://sandbox.api.example.com/test-endpoint",
            headers={
                "Authorization": "Bearer test_key",
                "Content-Type": "application/json",
            },
            json=None,
            params={"key": "value"},
            timeout=10,
        )

    @patch("requests.request")
    def test_make_request_timeout(self, mock_request, base_api_instance):
        """Test a request that times out."""
        mock_request.side_effect = requests.exceptions.Timeout

        with pytest.raises(requests.exceptions.Timeout):
            base_api_instance._make_request("GET", "test-endpoint")

    @patch("requests.request")
    def test_make_request_http_error(self, mock_request, base_api_instance):
        """Test a request that raises an HTTP error."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Bad Request"
        )
        mock_request.return_value = mock_response

        with pytest.raises(requests.exceptions.HTTPError):
            base_api_instance._make_request("GET", "test-endpoint")

    @patch("requests.request")
    def test_make_request_invalid_json(self, mock_request, base_api_instance):
        """Test a response with invalid JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Not JSON"
        mock_response.json.side_effect = ValueError
        mock_request.return_value = mock_response

        with pytest.raises(ValueError, match="Failed to parse response as JSON."):
            base_api_instance._make_request("GET", "test-endpoint")

    def test_make_request_logging(self, mock_request, base_api_instance, caplog):
        """Test logging during a request failure."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Bad Request"
        )
        mock_request.return_value = mock_response

        with caplog.at_level("ERROR"):
            with pytest.raises(requests.exceptions.HTTPError):
                base_api_instance._make_request("GET", "test-endpoint")

        # Check that the logging contains the expected substring
        assert any(
            "Request to https://sandbox.api.example.com/test-endpoint failed"
            in record.message
            for record in caplog.records
        )
