#! /usr/bin/env python

# This module contains the API for the Scryfall REST API.
# It is used to search for cards by name or id.

from .api import (
    search_card_by_id,
    search_cards_by_name,
    search_card_by_name_exact,
    search_card_by_name_fuzzy,
    search_cards_by_name_all,
    get_random_card,
    autocomplete_card_name,
    get_card_rulings,
)
from .schemas import (
    ImageUris,
    Prices,
    PreviewInfo,
    RelatedUris,
    PurchaseUris,
    ScryfallRelatedCard,
    CardFace,
    ScryfallCard,
    ScryfallCardList,
    ScryfallCatalog,
    ScryfallRuling,
    ScryfallRulingList,
)
from .exceptions import ScryfallApiError, ScryfallErrorBody

__all__ = [
    "search_card_by_id",
    "search_cards_by_name",
    "search_card_by_name_exact",
    "search_card_by_name_fuzzy",
    "search_cards_by_name_all",
    "get_random_card",
    "autocomplete_card_name",
    "get_card_rulings",
    "ScryfallApiError",
    "ScryfallErrorBody",
    "ScryfallCard",
    "ScryfallCardList",
    "ScryfallCatalog",
    "ScryfallRuling",
    "ScryfallRulingList",
    "ImageUris",
    "Prices",
    "PreviewInfo",
    "RelatedUris",
    "PurchaseUris",
    "ScryfallRelatedCard",
    "CardFace",
]