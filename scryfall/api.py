#!/usr/bin/env python
"""HTTP helpers for the Scryfall REST API (typed with ``schemas``)."""

# This module contains the API for the Scryfall REST API.
# It is used to search for cards by name or id.

import json
import os
from typing import Any, Mapping

try:
    import requests
    from .schemas import (
        ScryfallCard,
        ScryfallCardList,
    )
    from .exceptions import ScryfallApiError, ScryfallErrorBody
except ImportError as e:
    raise ImportError(f"Error importing: {e}")

# Default production API; override with SCRYFALL_BASE_URL for tests or alternate hosts.
BASE_URL = os.getenv("SCRYFALL_BASE_URL", "https://api.scryfall.com")


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
# if the object is not in the allowed list, raise a ScryfallApiError exception
def _raise_for_scryfall_error(payload: Mapping[str, Any], *, http_status: int) -> None:
    """Raise ``ScryfallApiError`` if ``payload`` ``object`` is not in the allowed list."""
    _allowed_objects = ["card", "list", "error"]

    # look in the payload for the object type
    if payload.get("object") not in _allowed_objects: 
        body = ScryfallErrorBody.from_dict(payload)
        # raise a ScryfallApiError exception with the details of the error
        raise ScryfallApiError(
            body.details or body.code or "Scryfall API error",
            http_status=http_status,
            body=body,
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
    scryfall_session = session or requests.Session()

    # create the parameters for the search
    params: dict[str, str] = {
        "q": _name_search_query(name),
        "unique": unique
    }

    # add the order parameter if it is provided
    if order is not None:
        params["order"] = order

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
    scryfall_session = session or requests.Session() # type: ignore

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

# export the API functions
__all__ = ["search_card_by_id", "search_cards_by_name"]