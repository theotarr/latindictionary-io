"""Tests for custom exceptions."""

from __future__ import annotations

from latindictionary_io.exceptions import (
    APIError,
    ConnectionError,
    InputValidationError,
    LatinDictionaryError,
    RateLimitError,
    TimeoutError,
)


def test_base_exception() -> None:
    err = LatinDictionaryError("something went wrong")
    assert str(err) == "something went wrong"
    assert err.message == "something went wrong"


def test_api_error() -> None:
    err = APIError(404, "Not Found")
    assert err.status_code == 404
    assert err.body == "Not Found"
    assert "404" in str(err)


def test_rate_limit_error_is_api_error() -> None:
    err = RateLimitError()
    assert isinstance(err, APIError)
    assert err.status_code == 429


def test_connection_error() -> None:
    err = ConnectionError("refused")
    assert isinstance(err, LatinDictionaryError)


def test_timeout_error() -> None:
    err = TimeoutError("timed out")
    assert isinstance(err, LatinDictionaryError)


def test_input_validation_error() -> None:
    err = InputValidationError("bad input")
    assert isinstance(err, LatinDictionaryError)
    assert "bad input" in str(err)
