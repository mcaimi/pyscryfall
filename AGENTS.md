# PyScryfall — Agent Development Guide

## Project Overview

Python 3.12+ library wrapping the [Scryfall](https://scryfall.com/) REST API for searching Magic: The Gathering cards. Uses `dataclasses` for typed JSON payloads.

**Tech stack:** Python 3.12+, `requests`, `pytest`, [`uv`](https://docs.astral.sh/uv/).

## Commands

```bash
uv sync                                  # setup venv + install deps (prod + dev)
uv run pytest                            # run integration tests (requires network)
uv run pytest -v                         # verbose output
```

## Layout

```
scryfall/
    __init__.py       ← re-exports public API: search functions, schemas, exceptions
    api.py            ← HTTP layer: search_cards_by_name, search_card_by_id, helpers
    schemas.py        ← dataclasses mirroring Scryfall JSON (from_dict / to_dict)
    exceptions.py     ← ScryfallApiError, ScryfallErrorBody
    helpers.py        ← internal parsers (_optional_model, _list_of, _str_list, _int_list)
tests/
    scryfall_api_test.py   ← integration tests against live Scryfall API
pyproject.toml         ← project config (uv + pytest)
```

## Architecture

- **api.py** — two public functions: `search_cards_by_name()` and `search_card_by_id()`. Each validates JSON, checks `object` field ("card" | "list" | "error"), raises `ScryfallApiError` on failure.
- **schemas.py** — dataclasses with `slots=True`. Every model has `from_dict()` / `to_dict()`. Nested models (`ImageUris`, `Prices`, `PreviewInfo`, `RelatedUris`, `PurchaseUris`, `CardFace`, `ScryfallRelatedCard`) composed inside `ScryfallCard`.
- **exceptions.py** — `ScryfallApiError(Exception)` carries `http_status` and optional `ScryfallErrorBody`.
- **helpers.py** — private functions for optional/nested list parsing; not in `__all__`.

Base URL defaults to `https://api.scryfall.com`, overridable via `SCRYFALL_BASE_URL` env var.

## Conventions

- All dataclasses use `@dataclass(slots=True)`.
- Optional fields default to `None` and use `data.get(key)` in `from_dict` factories.
- List/string/int conversion helpers (`_str_list`, `_int_list`) wrap `None` checks.
- Public API surface controlled via `__all__` in each module and the package `__init__.py`.
- Tests call the **real** Scryfall API (integration tests, no mocks). Need network access.

## Adding a New Endpoint

1. Add HTTP function to `scryfall/api.py` following the pattern in `search_cards_by_name`.
2. Extend or add dataclasses in `scryfall/schemas.py` (use `data.get()` for new optional fields).
3. Add `__all__` exports to `scryfall/__init__.py`.
4. Add an integration test in `tests/scryfall_api_test.py`.

## Dependencies

- **Runtime:** `requests >= 2.33.1`
- **Dev:** `pytest >= 8, < 9`