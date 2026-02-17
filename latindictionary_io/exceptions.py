"""Custom exceptions for the latindictionary-io client."""

from __future__ import annotations


class LatinDictionaryError(Exception):
    """Base exception for all latindictionary-io errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class APIError(LatinDictionaryError):
    """Raised when the API returns a non-success HTTP status code."""

    def __init__(self, status_code: int, body: str) -> None:
        self.status_code = status_code
        self.body = body
        super().__init__(f"API error {status_code}: {body}")


class ConnectionError(LatinDictionaryError):
    """Raised when a connection to the API cannot be established."""


class TimeoutError(LatinDictionaryError):
    """Raised when a request to the API times out."""


class RateLimitError(APIError):
    """Raised when the API returns HTTP 429 (Too Many Requests)."""

    def __init__(self, status_code: int = 429, body: str = "Rate limited") -> None:
        super().__init__(status_code, body)


class InputValidationError(LatinDictionaryError):
    """Raised when input parameters fail local validation."""
