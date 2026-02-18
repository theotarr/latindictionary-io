from __future__ import annotations
"""Synchronous client for the latindictionary.io REST API."""



import time
from typing import Any
from urllib.parse import quote

import httpx

from . import exceptions
from ._base import (
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    build_url,
    calculate_backoff,
)


class Client:
    """Synchronous client for latindictionary.io.

    Usage::

        with Client() as client:
            result = client.latin_to_english("canis")
    """

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._client = httpx.Client(timeout=timeout)

    # -- context manager -----------------------------------------------------

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    # -- internal request layer ----------------------------------------------

    def _request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        url = build_url(self._base_url, path)
        last_exc: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.get(url, params=params)
            except httpx.TimeoutException as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    time.sleep(calculate_backoff(attempt))
                    continue
                raise exceptions.TimeoutError(str(exc)) from exc
            except httpx.ConnectError as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    time.sleep(calculate_backoff(attempt))
                    continue
                raise exceptions.ConnectionError(str(exc)) from exc

            if response.status_code == 429:
                last_exc = exceptions.RateLimitError()
                if attempt < self._max_retries:
                    time.sleep(calculate_backoff(attempt))
                    continue
                raise last_exc

            if response.status_code >= 400:
                raise exceptions.APIError(response.status_code, response.text)

            return response.json()

        raise last_exc  # type: ignore[misc]  # pragma: no cover

    # -- translation endpoints -----------------------------------------------

    def latin_to_english(self, word: str) -> Any:
        """Look up a Latin word and get English definitions.

        Args:
            word: The Latin word to look up.

        Returns:
            The translation data from the API.
        """
        return self._request(f"la-to-en/{quote(word, safe='')}")

    def english_to_latin(self, word: str) -> Any:
        """Look up an English word and get Latin equivalents.

        Args:
            word: The English word to look up.

        Returns:
            The translation data from the API.
        """
        return self._request(f"en-to-la/{quote(word, safe='')}")

    def auto_detect(self, text: str) -> Any:
        """Auto-detect the language and translate.

        Args:
            text: The text to translate.

        Returns:
            The auto-detect result from the API.
        """
        return self._request(f"auto-detect/{quote(text, safe='')}")

    # -- parsing endpoints ---------------------------------------------------

    def latin_parse(
        self,
        text: str,
        *,
        model: str | None = None,
        max_candidates_per_token: int | None = None,
        max_alternates: int | None = None,
        allow_fallback: bool | None = None,
    ) -> Any:
        """AI-powered Latin text parsing.

        Args:
            text: The Latin text to parse.
            model: Optional model identifier.
            max_candidates_per_token: Max candidates per token.
            max_alternates: Max alternate parses.
            allow_fallback: Allow fallback parsing.

        Returns:
            The parsed result from the API.
        """
        params: dict[str, Any] = {"q": text}
        if model is not None:
            params["model"] = model
        if max_candidates_per_token is not None:
            params["max_candidates_per_token"] = max_candidates_per_token
        if max_alternates is not None:
            params["max_alternates"] = max_alternates
        if allow_fallback is not None:
            params["allow_fallback"] = allow_fallback
        return self._request("latin-parse", params)

    def inflection_table(
        self,
        lemma: str,
        *,
        entry_id: str | None = None,
        max_entries: int | None = None,
        include_periphrastic: bool | None = None,
    ) -> Any:
        """Get the inflection table for a Latin word.

        Args:
            lemma: The dictionary form of the word.
            entry_id: Optional entry ID for disambiguation.
            max_entries: Maximum number of entries to return.
            include_periphrastic: Include periphrastic forms.

        Returns:
            The inflection table data from the API.
        """
        params: dict[str, Any] = {"lemma": lemma}
        if entry_id is not None:
            params["entry_id"] = entry_id
        if max_entries is not None:
            params["max_entries"] = max_entries
        if include_periphrastic is not None:
            params["include_periphrastic"] = include_periphrastic
        return self._request("inflection-table", params)
