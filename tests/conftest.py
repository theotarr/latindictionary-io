"""Shared fixtures for latindictionary-io tests."""

from __future__ import annotations

import pytest
import respx

from latindictionary_io import AsyncClient, Client

MOCK_BASE = "https://mock.test/api/v1"


@pytest.fixture()
def client() -> Client:
    c = Client(base_url=MOCK_BASE, max_retries=0)
    yield c
    c.close()


@pytest.fixture()
async def async_client() -> AsyncClient:
    c = AsyncClient(base_url=MOCK_BASE, max_retries=0)
    yield c
    await c.close()


@pytest.fixture()
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url=MOCK_BASE) as router:
        yield router
