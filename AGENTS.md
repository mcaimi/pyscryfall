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

Installable package under **`src/pyscryfall/`**; import as **`pyscryfall`** after `uv sync` or `pip install`.

```
src/pyscryfall/
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

All modules live in **`src/pyscryfall/`** (Python package **`pyscryfall`**).

- **`api.py`** — Eight public functions for Scryfall API endpoints:
  - **Search**: `search_cards_by_name()`, `search_card_by_id()`
  - **Named search**: `search_card_by_name_exact()`, `search_card_by_name_fuzzy()`
  - **Pagination**: `search_cards_by_name_all()` (generator)
  - **Other**: `get_random_card()`, `autocomplete_card_name()`, `get_card_rulings()`
  - Each validates JSON, checks `object` field ("card" | "list" | "error" | "catalog"), raises `ScryfallApiError` on failure.
  - **Rate limiting**: Module-level `_enforce_rate_limit()` enforces 10 req/sec (configurable via `SCRYFALL_RATE_LIMIT_DELAY` env var).
  - **User-Agent**: All requests include `User-Agent: pyscryfall/<version>` via `_prepare_session()` helper.

- **`schemas.py`** — Dataclasses with `slots=True`. Every model has `from_dict()` / `to_dict()` / `to_json()` / `from_json_string()`. 
  - **Card models**: `ScryfallCard`, `ScryfallCardList`, `CardFace`, `ScryfallRelatedCard`
  - **Nested models**: `ImageUris`, `Prices`, `PreviewInfo`, `RelatedUris`, `PurchaseUris`
  - **Catalog**: `ScryfallCatalog` (for autocomplete)
  - **Rulings**: `ScryfallRuling`, `ScryfallRulingList`
  - All inherit from `_SerializableMixin` for serialization methods.

- **`exceptions.py`** — `ScryfallApiError(Exception)` carries `http_status` and optional `ScryfallErrorBody`.

- **`helpers.py`** — Private functions for optional/nested list parsing; not in `__all__`.

Base URL defaults to `https://api.scryfall.com`, overridable via `SCRYFALL_BASE_URL` env var.

## Conventions

- All dataclasses use `@dataclass(slots=True)`.
- Optional fields default to `None` and use `data.get(key)` in `from_dict` factories.
- List/string/int conversion helpers (`_str_list`, `_int_list`) wrap `None` checks.
- Public API surface controlled via `__all__` in each module and `src/pyscryfall/__init__.py`.
- Tests call the **real** Scryfall API (integration tests, no mocks). Need network access.
- **Rate limiting** is automatic and transparent - all API functions call `_enforce_rate_limit()` before HTTP requests.
- **User-Agent header** is automatically added via `_prepare_session()` unless user provides custom session with non-default User-Agent.
- All API functions follow this pattern:
  1. `_prepare_session(session)` — ensure User-Agent header
  2. `_enforce_rate_limit()` — sleep if needed for rate limiting
  3. `session.get(...)` — make HTTP request
  4. `_parse_json(response)` — validate and parse JSON
  5. `_raise_for_scryfall_error(payload, ...)` — check for error objects
  6. Return typed schema object

## Adding a New Endpoint

1. **Add HTTP function to `src/pyscryfall/api.py`** following the established pattern:
   - Use `_prepare_session(session)` for session handling (ensures User-Agent header)
   - Call `_enforce_rate_limit()` before making the HTTP request
   - Use `_parse_json(response)` for response parsing
   - Use `_raise_for_scryfall_error(payload, http_status=...)` for error validation
   - Follow existing docstring format with Args, Returns, Raises, Example sections
   - Add type hints for all parameters and return values

2. **Extend or add dataclasses in `src/pyscryfall/schemas.py`** if needed:
   - Use `@dataclass(slots=True)` decorator
   - Inherit from `_SerializableMixin` for serialization methods
   - Use `data.get()` for optional fields, cast required fields with `str()`, `int()`, etc.
   - Implement `from_dict()` class method following existing patterns
   - Use helper functions from `helpers.py` for list fields: `_str_list()`, `_int_list()`, `_list_of()`

3. **Export in both locations**:
   - Add to `__all__` list in `src/pyscryfall/api.py`
   - Import and re-export in `src/pyscryfall/__init__.py` `__all__`
   - Import new schemas in `api.py` if needed

4. **Add integration test in `tests/scryfall_api_test.py`**:
   - Test basic functionality with real API call
   - Test error cases if applicable
   - Test with known cards/data for predictable assertions
   - Use descriptive test names: `test_<function_name>_<scenario>`

5. **Update documentation**:
   - Add usage example to `README.md`
   - Update `AGENTS.md` if architectural changes

### Example Pattern for New Function

```python
def new_endpoint_function(
    param: str,
    *,
    optional_param: str | None = None,
    session: requests.Session | None = None,
    timeout: float = 30.0,
    base_url: str = BASE_URL,
) -> ReturnType:
    """
    Brief description of what this endpoint does.
    
    Uses Scryfall's ``GET /path/to/endpoint`` endpoint.
    More details about behavior.
    
    Args:
        param: Description of required parameter
        optional_param: Description of optional parameter
        session: Optional requests.Session
        timeout: Request timeout in seconds
        base_url: Override Scryfall API base URL
        
    Returns:
        ReturnType: Description of return value
        
    Raises:
        ScryfallApiError: Description of error conditions
        
    Example:
        >>> result = new_endpoint_function("example")
        >>> print(result.field)
    """
    scryfall_session = _prepare_session(session)
    
    params: dict[str, str] = {"param": param}
    if optional_param is not None:
        params["optional"] = optional_param
    
    _enforce_rate_limit()
    response = scryfall_session.get(
        f"{base_url}/path/to/endpoint",
        params=params,
        timeout=timeout,
    )
    
    if not response.ok:
        raise ScryfallApiError(
            f"Request failed (HTTP {response.status_code})",
            http_status=response.status_code,
        )
    
    payload = _parse_json(response)
    _raise_for_scryfall_error(payload, http_status=response.status_code)
    
    return ReturnType.from_dict(payload)  # type: ignore
```

## Dependencies

- **Runtime:** `requests >= 2.33.1`
- **Dev:** `pytest >= 8, < 9`