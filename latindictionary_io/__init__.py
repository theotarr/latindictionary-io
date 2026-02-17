"""latindictionary-io — Python client for the latindictionary.io API."""

from .async_client import AsyncClient
from .client import Client
from .exceptions import (
    APIError,
    ConnectionError,
    InputValidationError,
    LatinDictionaryError,
    RateLimitError,
    TimeoutError,
)
from .models import (
    AutoDetectResponse,
    InflectionTableResponse,
    LatinParseResponse,
    TranslationResponse,
)

__all__ = [
    # Clients
    "Client",
    "AsyncClient",
    # Exceptions
    "LatinDictionaryError",
    "APIError",
    "ConnectionError",
    "InputValidationError",
    "RateLimitError",
    "TimeoutError",
    # Models
    "AutoDetectResponse",
    "InflectionTableResponse",
    "LatinParseResponse",
    "TranslationResponse",
]

__version__ = "1.0.0"
