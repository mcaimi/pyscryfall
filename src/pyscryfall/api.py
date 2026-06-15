#!/usr/bin/env python
"""HTTP helpers for the Scryfall REST API (typed with ``schemas``)."""

# This module contains the API for the Scryfall REST API.
# It is used to search for cards by name or id.

import importlib.metadata
import json
import os
import time
from typing import Any, Generator, Mapping

try:
    import requests
    from .schemas import (
        ScryfallCard,
        ScryfallCardList,
        ScryfallCatalog,
        ScryfallRulingList,
    )
    from .exceptions import ScryfallApiError, ScryfallErrorBody
except ImportError as e:
    raise ImportError(f"Error importing: {e}")

# Default production API; override with SCRYFALL_BASE_URL for tests or alternate hosts.
BASE_URL = os.getenv("SCRYFALL_BASE_URL", "https://api.scryfall.com")

# Get package version for User-Agent header
try:
    _VERSION = importlib.metadata.version("pyscryfall")
except Exception:
    _VERSION = "0.1.2"


def _get_default_headers() -> dict[str, str]:
    """Return headers required by Scryfall API."""
    return {"User-Agent": f"pyscryfall/{_VERSION}"}


def _prepare_session(session: requests.Session | None) -> requests.Session:
    """Return session with required headers, respecting user's existing headers."""
    sess = session or requests.Session()
    # Always set our User-Agent if it's the default requests library value
    # or if no custom User-Agent was provided
    current_ua = sess.headers.get("User-Agent", "")
    if not current_ua or current_ua.startswith("python-requests/"):
        sess.headers.update(_get_default_headers())
    return sess


# Rate limiting: Scryfall allows ~10 req/sec
_last_request_time: float = 0.0
_rate_limit_delay: float = float(os.getenv("SCRYFALL_RATE_LIMIT_DELAY", "0.1"))


def _enforce_rate_limit() -> None:
    """
    Sleep if needed to maintain 10 requests/second limit.

    Scryfall API allows bursts, but we conservatively enforce 100ms between requests.
    Override with SCRYFALL_RATE_LIMIT_DELAY env var (in seconds).
    """
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < _rate_limit_delay:
        time.sleep(_rate_limit_delay - elapsed)
    _last_request_time = time.time()


# parse payload from the response from scryfall APIs
# response payload is expected to be a json object. this needs to be deserialized into a dictionary.
# if the response is not a valid json object, raise a ScryfallApiError exception
# if the response is not a dictionary, raise a ScryfallApiError exception
def _parse_json(response: requests.Response) -> dict[str, Any]:
    # try to parse the response as a json object
    try:
        payload = response.json()
    except json.JSONDecodeError as exc:
        raise ScryfallApiError(
            f"Invalid JSON from Scryfall (HTTP {response.status_code})",
            http_status=response.status_code,
        ) from exc

    # check if the deserialized payload is a dictionary
    if not isinstance(payload, dict):
        raise ScryfallApiError(
            f"Unexpected Scryfall payload type: {type(payload).__name__}",
            http_status=response.status_code,
        )

    # return the deserialized payload
    return payload

# raise an error if the response is not a valid Scryfall response
# managed object types are "card", "list", and "error"
# if the object is "error", raise a ScryfallApiError exception
def _raise_for_scryfall_error(payload: Mapping[str, Any], *, http_status: int) -> None:
    """Raise ``ScryfallApiError`` if ``payload`` ``object`` is "error"."""

    # Check if Scryfall returned an error object
    if payload.get("object") == "error":
        body = ScryfallErrorBody.from_dict(payload)
        # raise a ScryfallApiError exception with the details of the error
        raise ScryfallApiError(
            body.details or body.code or "Scryfall API error",
            http_status=http_status,
            body=body,
        )

    # Validate that object type is expected (card or list)
    obj_type = payload.get("object")
    if obj_type not in ["card", "list"]:
        raise ScryfallApiError(
            f"Unexpected object type from Scryfall: {obj_type}",
            http_status=http_status,
        )


# properly escape the name parameter for the search query
# double quotes are escaped by replacing them with a backslash and a double quote
# the result is returned as a string with the name:"..." clause 
def _name_search_query(name: str) -> str:
    # escape the double quotes in the name
    escaped = name.replace('"', '\\"')
    # return the name:"..." clause
    return f'name:"{escaped}"'


# search a card by using its name. it searches for all prints of a card.
# search is done by using the Scryfall API's /cards/search endpoint, and returns all cards that match the name.
# card matches even for partial string content (e.g. "Sengir" will match "Sengir Vampire")
def search_cards_by_name(
    name: str,
    *,
    unique: str = "cards",
    order: str | None = None,
    session: requests.Session | None = None,
    timeout: float = 30.0,
    base_url: str = BASE_URL,
) -> ScryfallCardList:
    """
        Search prints whose name matches ``name`` (Scryfall ``name:"…"`` syntax).
        See `<https://scryfall.com/docs/api/cards/search>`_ for ``unique`` and ``order``.
    """

    # create the session object with requests library if one is not provided
    scryfall_session = _prepare_session(session)

    # create the parameters for the search
    params: dict[str, str] = {
        "q": _name_search_query(name),
        "unique": unique
    }

    # add the order parameter if it is provided
    if order is not None:
        params["order"] = order

    # enforce rate limiting before sending request
    _enforce_rate_limit()

    # send the request to the Scryfall API
    response = scryfall_session.get(f"{base_url}/cards/search", params=params, timeout=timeout)

    # check if the response is ok
    if not response.ok:
        raise ScryfallApiError(
            f"Scryfall request failed (HTTP {response.status_code})",
            http_status=response.status_code,
        )

    # parse the response
    payload = _parse_json(response)

    # raise an error if the response is not a valid Scryfall response
    _raise_for_scryfall_error(payload, http_status=response.status_code)

    # return the list of cards
    return ScryfallCardList.from_dict(payload) # type: ignore   

# search a card by using its id. it returns the card details.
# since the card id is a UUID, it is unique and the result is expected to be a single card.
def search_card_by_id(
    card_id: str,
    *,
    session: requests.Session | None = None,
    timeout: float = 30.0,
    base_url: str = BASE_URL,
) -> ScryfallCard:

    # create the session object with requests library if one is not provided
    scryfall_session = _prepare_session(session)

    # enforce rate limiting before sending request
    _enforce_rate_limit()

    # send the request to the Scryfall API
    response = scryfall_session.get(f"{base_url}/cards/{card_id}", timeout=timeout)

    # check if the response is ok
    if not response.ok:
        raise ScryfallApiError(
            f"Scryfall request failed (HTTP {response.status_code})",
            http_status=response.status_code,
        )

    # parse the response
    payload = _parse_json(response)

    # raise an error if the response is not a valid Scryfall response
    _raise_for_scryfall_error(payload, http_status=response.status_code)

    # return the card details
    return ScryfallCard.from_dict(payload) # type: ignore   

def search_card_by_name_exact(
    name: str,
    *,
    set_code: str | None = None,
    session: requests.Session | None = None,
    timeout: float = 30.0,
    base_url: str = BASE_URL,
) -> ScryfallCard:
    """
    Find a single card by exact name match.

    Uses Scryfall's ``GET /cards/named?exact=<name>`` endpoint.
    Returns the first match found (prefers the most recent printing).

    Args:
        name: Exact card name (case-insensitive)
        set_code: Optional set code to restrict search (e.g., "m21")
        session: Optional requests.Session
        timeout: Request timeout in seconds
        base_url: Override Scryfall API base URL

    Returns:
        ScryfallCard: The matching card

    Raises:
        ScryfallApiError: If card not found or API error

    Example:
        >>> card = search_card_by_name_exact("Lightning Bolt")
        >>> print(card.oracle_text)
    """
    scryfall_session = _prepare_session(session)

    params: dict[str, str] = {"exact": name}
    if set_code is not None:
        params["set"] = set_code

    _enforce_rate_limit()
    response = scryfall_session.get(
        f"{base_url}/cards/named",
        params=params,
        timeout=timeout,
    )

    if not response.ok:
        raise ScryfallApiError(
            f"Card not found: {name}",
            http_status=response.status_code,
        )

    payload = _parse_json(response)
    _raise_for_scryfall_error(payload, http_status=response.status_code)

    return ScryfallCard.from_dict(payload)  # type: ignore


def search_card_by_name_fuzzy(
    name: str,
    *,
    set_code: str | None = None,
    session: requests.Session | None = None,
    timeout: float = 30.0,
    base_url: str = BASE_URL,
) -> ScryfallCard:
    """
    Find a single card by fuzzy name match.

    Uses Scryfall's ``GET /cards/named?fuzzy=<name>`` endpoint.
    Scryfall's fuzzy matching handles typos, partial names, and abbreviations.

    Args:
        name: Fuzzy card name to search
        set_code: Optional set code to restrict search (e.g., "m21")
        session: Optional requests.Session
        timeout: Request timeout in seconds
        base_url: Override Scryfall API base URL

    Returns:
        ScryfallCard: The best matching card

    Raises:
        ScryfallApiError: If no match found or API error

    Example:
        >>> card = search_card_by_name_fuzzy("Lig Bolt")  # finds Lightning Bolt
        >>> print(card.name)
    """
    scryfall_session = _prepare_session(session)

    params: dict[str, str] = {"fuzzy": name}
    if set_code is not None:
        params["set"] = set_code

    _enforce_rate_limit()
    response = scryfall_session.get(
        f"{base_url}/cards/named",
        params=params,
        timeout=timeout,
    )

    if not response.ok:
        raise ScryfallApiError(
            f"No fuzzy match found for: {name}",
            http_status=response.status_code,
        )

    payload = _parse_json(response)
    _raise_for_scryfall_error(payload, http_status=response.status_code)

    return ScryfallCard.from_dict(payload)  # type: ignore


def get_random_card(
    *,
    q: str | None = None,
    session: requests.Session | None = None,
    timeout: float = 30.0,
    base_url: str = BASE_URL,
) -> ScryfallCard:
    """
    Fetch a random card from Scryfall.

    Uses Scryfall's ``GET /cards/random`` endpoint.
    Optionally filter with a full-text search query.

    Args:
        q: Optional search query to filter random results (e.g., "t:creature")
        session: Optional requests.Session
        timeout: Request timeout in seconds
        base_url: Override Scryfall API base URL

    Returns:
        ScryfallCard: A random card

    Raises:
        ScryfallApiError: On API error

    Example:
        >>> card = get_random_card()
        >>> print(card.name)
        >>>
        >>> creature = get_random_card(q="t:creature")
        >>> print(creature.type_line)
    """
    scryfall_session = _prepare_session(session)

    params: dict[str, str] = {}
    if q is not None:
        params["q"] = q

    _enforce_rate_limit()
    response = scryfall_session.get(
        f"{base_url}/cards/random",
        params=params if params else None,
        timeout=timeout,
    )

    if not response.ok:
        raise ScryfallApiError(
            f"Random card request failed (HTTP {response.status_code})",
            http_status=response.status_code,
        )

    payload = _parse_json(response)
    _raise_for_scryfall_error(payload, http_status=response.status_code)

    return ScryfallCard.from_dict(payload)  # type: ignore


def autocomplete_card_name(
    q: str,
    *,
    include_extras: bool = False,
    session: requests.Session | None = None,
    timeout: float = 30.0,
    base_url: str = BASE_URL,
) -> ScryfallCatalog:
    """
    Get autocomplete suggestions for a partial card name.

    Uses Scryfall's ``GET /cards/autocomplete`` endpoint.
    Returns up to 25 card name suggestions.

    Args:
        q: Partial card name to autocomplete (minimum 2 characters)
        include_extras: Include extra cards (tokens, schemes, etc.)
        session: Optional requests.Session
        timeout: Request timeout in seconds
        base_url: Override Scryfall API base URL

    Returns:
        ScryfallCatalog: Catalog with suggested card names in data field

    Raises:
        ScryfallApiError: On API error or invalid query

    Example:
        >>> suggestions = autocomplete_card_name("Lig")
        >>> print(suggestions.data)
        ['Light', 'Lightning Bolt', 'Lightning Strike', ...]
    """
    if len(q) < 2:
        raise ScryfallApiError(
            "Autocomplete query must be at least 2 characters",
            http_status=None,
        )

    scryfall_session = _prepare_session(session)

    params: dict[str, str] = {"q": q}
    if include_extras:
        params["include_extras"] = "true"

    _enforce_rate_limit()
    response = scryfall_session.get(
        f"{base_url}/cards/autocomplete",
        params=params,
        timeout=timeout,
    )

    if not response.ok:
        raise ScryfallApiError(
            f"Autocomplete request failed (HTTP {response.status_code})",
            http_status=response.status_code,
        )

    payload = _parse_json(response)

    # Note: autocomplete returns object="catalog", not "error"
    # So we need special handling here
    if payload.get("object") == "error":
        body = ScryfallErrorBody.from_dict(payload)
        raise ScryfallApiError(
            body.details or body.code or "Scryfall API error",
            http_status=response.status_code,
            body=body,
        )

    return ScryfallCatalog.from_dict(payload)  # type: ignore


def search_cards_by_name_all(
    name: str,
    *,
    unique: str = "cards",
    order: str | None = None,
    session: requests.Session | None = None,
    timeout: float = 30.0,
    base_url: str = BASE_URL,
) -> Generator[ScryfallCard, None, None]:
    """
    Yield all cards matching ``name`` across all pages.

    Automatically follows ``next_page`` URLs from Scryfall's paginated responses.
    Rate limiting is enforced between page requests.

    Args:
        name: Card name to search (same semantics as search_cards_by_name)
        unique: Unique mode ("cards" | "art" | "prints")
        order: Sort order (e.g., "released", "name")
        session: Optional requests.Session for connection pooling
        timeout: Request timeout in seconds
        base_url: Override Scryfall API base URL

    Yields:
        ScryfallCard: Individual cards from all pages

    Raises:
        ScryfallApiError: On HTTP or API errors

    Example:
        >>> for card in search_cards_by_name_all("Island"):
        ...     print(card.set_name, card.collector_number)
    """
    scryfall_session = _prepare_session(session)

    # Fetch first page using existing function
    first_page = search_cards_by_name(
        name,
        unique=unique,
        order=order,
        session=scryfall_session,
        timeout=timeout,
        base_url=base_url,
    )

    # Yield cards from first page
    for card in first_page.data:
        yield card

    # Follow next_page if available
    next_url = first_page.next_page
    while next_url:
        _enforce_rate_limit()
        response = scryfall_session.get(next_url, timeout=timeout)

        if not response.ok:
            raise ScryfallApiError(
                f"Scryfall pagination request failed (HTTP {response.status_code})",
                http_status=response.status_code,
            )

        payload = _parse_json(response)
        _raise_for_scryfall_error(payload, http_status=response.status_code)

        page = ScryfallCardList.from_dict(payload)  # type: ignore
        for card in page.data:
            yield card

        next_url = page.next_page


def get_card_rulings(
    card_id: str,
    *,
    session: requests.Session | None = None,
    timeout: float = 30.0,
    base_url: str = BASE_URL,
) -> ScryfallRulingList:
    """
    Fetch rulings for a card by Scryfall ID.

    Uses Scryfall's ``GET /cards/:id/rulings`` endpoint.
    Returns clarifications and judge rulings about a specific card.

    Args:
        card_id: Scryfall UUID for the card
        session: Optional requests.Session
        timeout: Request timeout in seconds
        base_url: Override Scryfall API base URL

    Returns:
        ScryfallRulingList: List of rulings for the card

    Raises:
        ScryfallApiError: If card not found or API error

    Example:
        >>> card = search_card_by_name_exact("Humility")
        >>> rulings = get_card_rulings(card.id)
        >>> for ruling in rulings.data:
        ...     print(ruling.published_at, ruling.comment)
    """
    scryfall_session = _prepare_session(session)

    _enforce_rate_limit()
    response = scryfall_session.get(
        f"{base_url}/cards/{card_id}/rulings",
        timeout=timeout,
    )

    if not response.ok:
        raise ScryfallApiError(
            f"Rulings request failed for card {card_id} (HTTP {response.status_code})",
            http_status=response.status_code,
        )

    payload = _parse_json(response)

    # Check for error object
    if payload.get("object") == "error":
        body = ScryfallErrorBody.from_dict(payload)
        raise ScryfallApiError(
            body.details or body.code or "Scryfall API error",
            http_status=response.status_code,
            body=body,
        )

    return ScryfallRulingList.from_dict(payload)  # type: ignore


# export the API functions
__all__ = [
    "search_card_by_id",
    "search_cards_by_name",
    "search_card_by_name_exact",
    "search_card_by_name_fuzzy",
    "search_cards_by_name_all",
    "get_random_card",
    "autocomplete_card_name",
    "get_card_rulings",
]