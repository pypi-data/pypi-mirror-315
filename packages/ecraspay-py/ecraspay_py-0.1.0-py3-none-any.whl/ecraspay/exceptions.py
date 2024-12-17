class ApiWrapperError(Exception):
    """Base exception for the API wrapper."""


class ApiWrapperAuthError(ApiWrapperError):
    """Exception raised for authentication errors."""


class ApiWrapperRequestError(ApiWrapperError):
    """Exception raised for invalid requests."""
