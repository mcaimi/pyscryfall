#!/usr/bin/env python
"""Small parsers for optional nested objects and list fields in Scryfall JSON."""

from typing import Any, Mapping

# parse an optional nested object from a dictionary
def _optional_model[T](
    cls: type[T],
    data: Mapping[str, Any] | None,
    key: str,
    *,
    from_dict: str = "from_dict",
) -> T | None:
    raw = data.get(key) if data is not None else None
    if raw is None:
        return None
    factory = getattr(cls, from_dict)
    return factory(raw)


# parse a list of objects from a dictionary
def _list_of[T](
    cls: type[T],
    items: Any,
    *,
    from_dict: str = "from_dict",
) -> list[T] | None:
    if items is None:
        return None
    if not isinstance(items, list):
        return None
    factory = getattr(cls, from_dict)
    return [factory(x) for x in items]


# parse a list of strings from a dictionary
def _str_list(v: Any) -> list[str] | None:
    if v is None:
        return None
    return [str(x) for x in v]


# parse a list of integers from a dictionary
def _int_list(v: Any) -> list[int] | None:
    if v is None:
        return None
    return [int(x) for x in v]
