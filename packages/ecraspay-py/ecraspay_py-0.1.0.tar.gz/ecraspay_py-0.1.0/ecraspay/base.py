import os
import requests
import logging


class BaseAPI:
    def __init__(self, api_key=None, webhook_url=None, environment="sandbox"):
        """
        Initialize the API client.

        Args:
            api_key (str): API key for authentication.
            webhook_url (str): Webhook URL for notifications.
            environment (str): The environment to use ('sandbox' or 'live').
        """
        self.api_key = api_key or os.getenv("API_KEY")
        self.webhook_url = webhook_url or os.getenv("WEBHOOK_URL")

        # Set the environment (default: sandbox)
        self.environment = environment or os.getenv("API_ENV", "sandbox")

        # Define base URLs
        self.base_urls = {
            "sandbox": "https://api.merchant.staging.ercaspay.com/api/v1",
            "live": "https://api.ercaspay.com/api/v1",
        }

        # Select the base URL based on the environment
        self.base_url = self.base_urls.get(self.environment)
        if not self.base_url:
            raise ValueError(
                f"Invalid environment '{self.environment}'. Use 'sandbox' or 'live'."
            )

        if not self.api_key:
            raise ValueError("API key is required")

    def _get_headers(self):
        """Prepare headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _make_request(self, method, endpoint, data=None, params=None, timeout=10):
        """
        Make an HTTP request to the API.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE).
            endpoint (str): API endpoint (relative to the base URL).
            data (dict): JSON payload for the request.
            params (dict): Query parameters for the request.
            timeout (int): Timeout for the request in seconds. Defaults to 10.

        Returns:
            dict: JSON response from the API.

        Raises:
            ValueError: If the response cannot be parsed as JSON.
            requests.exceptions.RequestException: For any request-related errors.
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        try:
            # Make the HTTP request
            response = requests.request(
                method, url, headers=headers, json=data, params=params, timeout=timeout
            )

            # Raise HTTP errors if status_code indicates an issue
            response.raise_for_status()

        except requests.exceptions.Timeout:
            logging.error(f"Request to {url} timed out.")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Request to {url} failed: {str(e)}")
            raise

        try:
            # Parse and return JSON response
            return response.json()
        except ValueError:
            logging.error(f"Failed to parse JSON from response: {response.text}")
            raise ValueError("Failed to parse response as JSON.") from None
