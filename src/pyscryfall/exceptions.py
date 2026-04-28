#! /usr/bin/env python

# This module contains the exceptions for the Scryfall REST API.
# It is used to define the exceptions for the Scryfall REST API.

from dataclasses import dataclass
from typing import Any, Mapping

# define the dataclass for the ScryfallErrorBody schema
@dataclass(slots=True)
class ScryfallErrorBody:
    object: str | None = None
    code: str | None = None
    status: int | None = None
    details: str | None = None

    # create a new ScryfallErrorBody object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        return cls(
            object=str(data.get("object", "error")),
            code=str(data.get("code", "")),
            status=int(data.get("status", 0)),
            details=str(data.get("details", "")),
        )


# raise an error if the response is not a valid Scryfall response
class ScryfallApiError(Exception):
    """Raised when Scryfall returns ``object: error`` or a non-success HTTP status."""

    def __init__(self, message: str, *, http_status: int | None = None, body: ScryfallErrorBody | None = None):
        super().__init__(message)
        self.http_status = http_status
        self.body = body

# export the exceptions
__all__ = ["ScryfallErrorBody", "ScryfallApiError"]