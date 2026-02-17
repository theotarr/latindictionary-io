"""Examples for the latindictionary-io Python client."""

import asyncio

from latindictionary_io import AsyncClient, Client

# ---------------------------------------------------------------------------
# Synchronous usage
# ---------------------------------------------------------------------------


def sync_examples() -> None:
    with Client() as client:
        # Latin to English
        result = client.latin_to_english("canis")
        print(f"  Latin->English: {result}")

        # English to Latin
        result = client.english_to_latin("dog")
        print(f"  English->Latin: {result}")

        # Auto-detect language and translate
        result = client.auto_detect("amor")
        print(f"  Auto-detect: {result}")

        # AI-powered Latin parsing
        result = client.latin_parse("Gallia est omnis divisa in partes tres")
        print(f"  Parse result: {result}")

        # Inflection table
        result = client.inflection_table("amo")
        print(f"  Inflection table: {result}")


# ---------------------------------------------------------------------------
# Asynchronous usage
# ---------------------------------------------------------------------------


async def async_examples() -> None:
    async with AsyncClient() as client:
        # All methods mirror the sync client, but are awaited
        result = await client.latin_to_english("canis")
        print(f"  Latin->English: {result}")

        result = await client.auto_detect("amor")
        print(f"  Auto-detect: {result}")

        result = await client.latin_parse("Gallia est omnis divisa in partes tres")
        print(f"  Parse result: {result}")


if __name__ == "__main__":
    print("=== Sync Examples ===")
    sync_examples()

    print("\n=== Async Examples ===")
    asyncio.run(async_examples())
