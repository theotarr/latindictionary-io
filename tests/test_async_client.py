"""Tests for the asynchronous AsyncClient."""

from __future__ import annotations

import pytest
import respx

from latindictionary_io import AsyncClient
from latindictionary_io.exceptions import APIError, RateLimitError

MOCK_BASE = "https://mock.test/api/v1"


@pytest.fixture()
async def client() -> AsyncClient:
    c = AsyncClient(base_url=MOCK_BASE, max_retries=0)
    yield c
    await c.close()


class TestAsyncLatinToEnglish:
    @respx.mock(base_url=MOCK_BASE)
    @pytest.mark.asyncio
    async def test_lookup(self, client: AsyncClient) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/la-to-en/canis").respond(
            200, json={"word": "canis", "definitions": ["dog"]}
        )
        result = await client.latin_to_english("canis")
        assert result["word"] == "canis"


class TestAsyncEnglishToLatin:
    @respx.mock(base_url=MOCK_BASE)
    @pytest.mark.asyncio
    async def test_lookup(self, client: AsyncClient) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/en-to-la/dog").respond(
            200, json={"word": "dog", "translations": ["canis"]}
        )
        result = await client.english_to_latin("dog")
        assert result["word"] == "dog"


class TestAsyncAutoDetect:
    @respx.mock(base_url=MOCK_BASE)
    @pytest.mark.asyncio
    async def test_auto_detect(self, client: AsyncClient) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/auto-detect/amor").respond(
            200, json={"language": "latin", "data": []}
        )
        result = await client.auto_detect("amor")
        assert result["language"] == "latin"


class TestAsyncLatinParse:
    @respx.mock(base_url=MOCK_BASE)
    @pytest.mark.asyncio
    async def test_parse(self, client: AsyncClient) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/latin-parse").respond(
            200, json={"tokens": []}
        )
        result = await client.latin_parse("Gallia est omnis divisa")
        assert isinstance(result, dict)


class TestAsyncInflectionTable:
    @respx.mock(base_url=MOCK_BASE)
    @pytest.mark.asyncio
    async def test_inflection(self, client: AsyncClient) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/inflection-table").respond(
            200, json={"entries": []}
        )
        result = await client.inflection_table("amo")
        assert isinstance(result, dict)


class TestAsyncErrorHandling:
    @respx.mock(base_url=MOCK_BASE)
    @pytest.mark.asyncio
    async def test_api_error(self, client: AsyncClient) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/la-to-en/").respond(500, text="Error")
        with pytest.raises(APIError):
            await client.latin_to_english("canis")

    @respx.mock(base_url=MOCK_BASE)
    @pytest.mark.asyncio
    async def test_rate_limit(self, client: AsyncClient) -> None:
        respx.get(url__startswith=f"{MOCK_BASE}/la-to-en/").respond(429, text="Too Many")
        with pytest.raises(RateLimitError):
            await client.latin_to_english("canis")


class TestAsyncContextManager:
    @pytest.mark.asyncio
    async def test_async_context(self) -> None:
        async with AsyncClient(base_url=MOCK_BASE) as client:
            assert isinstance(client, AsyncClient)
