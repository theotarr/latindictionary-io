# latindictionary-io

Python client for the [latindictionary.io](https://www.latindictionary.io) REST API — Latin-English translation, auto-detection, AI parsing, and inflection tables.

- **Sync + async** — `Client` (httpx) and `AsyncClient` (httpx.AsyncClient)
- **Typed** — full type hints, Pydantic v2 response models, `py.typed`
- **Resilient** — automatic retries with exponential backoff + jitter
- **Python 3.10+**

## Installation

```sh
pip install latindictionary-io
```

## Quick start

```python
from latindictionary_io import Client

with Client() as client:
    # Latin → English
    result = client.latin_to_english("canis")
    print(result)

    # English → Latin
    result = client.english_to_latin("dog")
    print(result)
```

### Async

```python
import asyncio
from latindictionary_io import AsyncClient

async def main():
    async with AsyncClient() as client:
        result = await client.latin_to_english("canis")
        print(result)

asyncio.run(main())
```

## API reference

Both `Client` and `AsyncClient` expose the same methods (async versions are awaited).

### Constructor

```python
Client(
    base_url="https://api.latindictionary.io/api/v1",
    timeout=30.0,
    max_retries=3,
)
```

| Parameter | Default | Description |
|---|---|---|
| `base_url` | `https://api.latindictionary.io/api/v1` | REST API base URL |
| `timeout` | `30.0` | Request timeout in seconds |
| `max_retries` | `3` | Max retry attempts (with exponential backoff) |

### Translation endpoints

#### `latin_to_english(word)`

Look up a Latin word and get English definitions.

```python
result = client.latin_to_english("canis")
```

| Parameter | Type | Description |
|---|---|---|
| `word` | `str` | The Latin word to look up |

#### `english_to_latin(word)`

Look up an English word and get Latin equivalents.

```python
result = client.english_to_latin("dog")
```

| Parameter | Type | Description |
|---|---|---|
| `word` | `str` | The English word to look up |

#### `auto_detect(text)`

Auto-detect the language and translate.

```python
result = client.auto_detect("amor")
```

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | The text to translate |

### Parsing endpoints

#### `latin_parse(text, *, model=None, max_candidates_per_token=None, max_alternates=None, allow_fallback=None)`

AI-powered Latin text parsing.

```python
result = client.latin_parse("Gallia est omnis divisa in partes tres")
```

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | The Latin text to parse |
| `model` | `str \| None` | Optional model identifier |
| `max_candidates_per_token` | `int \| None` | Max candidates per token |
| `max_alternates` | `int \| None` | Max alternate parses |
| `allow_fallback` | `bool \| None` | Allow fallback parsing |

#### `inflection_table(lemma, *, entry_id=None, max_entries=None, include_periphrastic=None)`

Get the inflection table for a Latin word.

```python
table = client.inflection_table("amo")
```

| Parameter | Type | Description |
|---|---|---|
| `lemma` | `str` | The dictionary form of the word |
| `entry_id` | `str \| None` | Optional entry ID for disambiguation |
| `max_entries` | `int \| None` | Maximum number of entries |
| `include_periphrastic` | `bool \| None` | Include periphrastic forms |

## Response models

Pydantic v2 models are available for response validation. All use `extra="allow"` so additional API fields are preserved.

| Model | Used by |
|---|---|
| `TranslationResponse` | `latin_to_english()`, `english_to_latin()` |
| `AutoDetectResponse` | `auto_detect()` |
| `LatinParseResponse` | `latin_parse()` |
| `InflectionTableResponse` | `inflection_table()` |

## Exceptions

All exceptions inherit from `LatinDictionaryError`.

| Exception | Description |
|---|---|
| `LatinDictionaryError` | Base exception |
| `APIError` | Non-success HTTP status (has `.status_code`, `.body`) |
| `RateLimitError` | HTTP 429 — extends `APIError` |
| `ConnectionError` | Cannot connect to API |
| `TimeoutError` | Request timed out |
| `InputValidationError` | Local input validation failed |

## Development

```sh
pip install -e ".[dev]"
pytest
```

## License

MIT
