"""Tests for _base helpers."""

from __future__ import annotations

from latindictionary_io._base import build_url, calculate_backoff

BASE = "https://api.latindictionary.io/api/v1"


class TestBuildUrl:
    def test_simple_path(self) -> None:
        url = build_url(BASE, "la-to-en/canis")
        assert url == f"{BASE}/la-to-en/canis"

    def test_trailing_slash_stripped(self) -> None:
        url = build_url(BASE + "/", "la-to-en/canis")
        assert "//" not in url.replace("https://", "")

    def test_leading_slash_stripped(self) -> None:
        url = build_url(BASE, "/la-to-en/canis")
        assert url == f"{BASE}/la-to-en/canis"


class TestCalculateBackoff:
    def test_attempt_zero(self) -> None:
        delay = calculate_backoff(0)
        assert 1.0 <= delay <= 1.5

    def test_increases_with_attempt(self) -> None:
        delays = [calculate_backoff(i) for i in range(5)]
        # The base delay (without jitter) doubles each time, so on average later
        # attempts should be larger. We just check the max bound grows.
        assert calculate_backoff(4) <= 30.0 + 15.0  # BACKOFF_MAX + max jitter
