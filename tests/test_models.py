"""Tests for Pydantic response models."""

from __future__ import annotations

from latindictionary_io.models import (
    AutoDetectResponse,
    InflectionTableResponse,
    LatinParseResponse,
    TranslationResponse,
)


class TestTranslationResponse:
    def test_extra_fields(self) -> None:
        resp = TranslationResponse.model_validate({"word": "canis", "definitions": ["dog"]})
        assert resp.word == "canis"  # type: ignore[attr-defined]
        assert resp.definitions == ["dog"]  # type: ignore[attr-defined]


class TestAutoDetectResponse:
    def test_basic(self) -> None:
        result = AutoDetectResponse(language="latin", data=[{"word": "canis"}])
        assert result.language == "latin"
        assert isinstance(result.data, list)

    def test_extra_fields(self) -> None:
        result = AutoDetectResponse.model_validate(
            {"language": "latin", "data": [], "confidence": 0.95}
        )
        assert result.confidence == 0.95  # type: ignore[attr-defined]


class TestLatinParseResponse:
    def test_extra_fields(self) -> None:
        resp = LatinParseResponse.model_validate({"tokens": [{"text": "Gallia"}]})
        assert resp.tokens == [{"text": "Gallia"}]  # type: ignore[attr-defined]


class TestInflectionTableResponse:
    def test_extra_fields(self) -> None:
        resp = InflectionTableResponse.model_validate({"entries": [], "lemma": "amo"})
        assert resp.lemma == "amo"  # type: ignore[attr-defined]
