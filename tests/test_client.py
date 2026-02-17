"""Tests for the synchronous Client."""

from __future__ import annotations

import pytest
import respx

from latindictionary_io import Client
from latindictionary_io.exceptions import APIError, RateLimitError

MOCK_BASE = "https://mock.test/api/v1"


@pytest.fixture()
def client() -> Client:
    c = Client(base_url=MOCK_BASE, max_retries=0)
    yield c
    c.close()


class TestLatinToEnglish:
    @respx.mock(base_url=MOCK_BASE)
    def test_lookup(self, client: Client) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/la-to-en/canis").respond(
            200, json={"word": "canis", "definitions": ["dog"]}
        )
        result = client.latin_to_english("canis")
        assert result["word"] == "canis"


class TestEnglishToLatin:
    @respx.mock(base_url=MOCK_BASE)
    def test_lookup(self, client: Client) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/en-to-la/dog").respond(
            200, json={"word": "dog", "translations": ["canis"]}
        )
        result = client.english_to_latin("dog")
        assert result["word"] == "dog"


class TestAutoDetect:
    @respx.mock(base_url=MOCK_BASE)
    def test_auto_detect(self, client: Client) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/auto-detect/amor").respond(
            200, json={"language": "latin", "data": []}
        )
        result = client.auto_detect("amor")
        assert result["language"] == "latin"


class TestLatinParse:
    @respx.mock(base_url=MOCK_BASE)
    def test_parse(self, client: Client) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/latin-parse").respond(
            200, json={"tokens": []}
        )
        result = client.latin_parse("Gallia est omnis divisa")
        assert isinstance(result, dict)

    @respx.mock(base_url=MOCK_BASE)
    def test_parse_with_options(self, client: Client) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/latin-parse").respond(
            200, json={"tokens": []}
        )
        result = client.latin_parse(
            "Gallia", model="default", max_candidates_per_token=3, allow_fallback=True
        )
        assert isinstance(result, dict)


class TestInflectionTable:
    @respx.mock(base_url=MOCK_BASE)
    def test_inflection(self, client: Client) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/inflection-table").respond(
            200, json={"entries": []}
        )
        result = client.inflection_table("amo")
        assert isinstance(result, dict)


class TestErrorHandling:
    @respx.mock(base_url=MOCK_BASE)
    def test_api_error(self, client: Client) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/la-to-en/").respond(
            500, text="Internal Error"
        )
        with pytest.raises(APIError) as exc_info:
            client.latin_to_english("canis")
        assert exc_info.value.status_code == 500

    @respx.mock(base_url=MOCK_BASE)
    def test_rate_limit(self, client: Client) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/la-to-en/").respond(
            429, text="Too Many"
        )
        with pytest.raises(RateLimitError):
            client.latin_to_english("canis")


class TestContextManager:
    def test_sync_context(self) -> None:
        with Client(base_url=MOCK_BASE) as client:
            assert isinstance(client, Client)
