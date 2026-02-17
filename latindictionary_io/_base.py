"""Shared helpers for the sync and async clients."""



import random

DEFAULT_BASE_URL = "https://api.latindictionary.io/api/v1"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3
BACKOFF_BASE = 1.0
BACKOFF_MAX = 30.0


def build_url(base_url: str, path: str) -> str:
    """Build a REST URL by joining *base_url* and *path*."""
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def calculate_backoff(attempt: int) -> float:
    """Return a delay in seconds using exponential backoff with jitter."""
    delay = min(BACKOFF_BASE * (2**attempt), BACKOFF_MAX)
    jitter = random.uniform(0, delay * 0.5)
    return delay + jitter
