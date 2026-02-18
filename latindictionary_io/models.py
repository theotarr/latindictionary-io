"""Pydantic v2 response models for the latindictionary.io REST API.

All models use ``extra="allow"`` so every field returned by the API is
captured even when the schema here does not list it explicitly.
"""



from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# GET /la-to-en/{word}  &  GET /en-to-la/{word}
# ---------------------------------------------------------------------------


class TranslationResponse(BaseModel):
    """Top-level response from the translation endpoints."""

    model_config = ConfigDict(extra="allow")


# ---------------------------------------------------------------------------
# GET /auto-detect/{text}
# ---------------------------------------------------------------------------


class AutoDetectResponse(BaseModel):
    """Response from the auto-detect endpoint."""

    model_config = ConfigDict(extra="allow")

    language: Optional[str] = None
    data: Optional[Any] = None


# ---------------------------------------------------------------------------
# GET /latin-parse
# ---------------------------------------------------------------------------


class LatinParseResponse(BaseModel):
    """Response from the AI Latin parsing endpoint."""

    model_config = ConfigDict(extra="allow")


# ---------------------------------------------------------------------------
# GET /inflection-table
# ---------------------------------------------------------------------------


class InflectionTableResponse(BaseModel):
    """Response from the inflection table endpoint."""

    model_config = ConfigDict(extra="allow")
