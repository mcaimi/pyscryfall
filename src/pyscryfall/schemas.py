#!/usr/bin/env python
"""Scryfall API JSON: list responses, errors, and card objects (all documented layouts)."""

# This module contains the schemas for the Scryfall REST API.
# It is used to define the data structures for the Scryfall REST API.
# Wraps the JSON responses from the Scryfall REST API into Python objects.

import json
from dataclasses import asdict, dataclass, fields
from typing import Any, Mapping

try:
    from .helpers import _optional_model, _list_of, _str_list, _int_list
except ImportError as e:
    raise ImportError(f"Error importing: {e}")

# Wrap the JSON responses from the Scryfall REST API into Python dataclasses


# Mixin class for serialization methods
class _SerializableMixin:
    # serialize the _SerializableMixin object to a dictionary
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    # serialize the _SerializableMixin object as a json document
    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)

    # load a _SerializableMixin object from a serialized string
    @classmethod
    def from_json_string(cls, s: str):
        return cls.from_dict(json.loads(s))


# define the dataclass for the ImageUris schema
@dataclass(slots=True)
class ImageUris(_SerializableMixin):
    small: str | None = None
    normal: str | None = None
    large: str | None = None
    png: str | None = None
    art_crop: str | None = None
    border_crop: str | None = None

    # create a new ImageUris object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        return cls(
            small=data.get("small"),
            normal=data.get("normal"),
            large=data.get("large"),
            png=data.get("png"),
            art_crop=data.get("art_crop"),
            border_crop=data.get("border_crop"),
        )


# define the dataclass for the Prices schema
@dataclass(slots=True)
class Prices(_SerializableMixin):
    usd: str | None = None
    usd_foil: str | None = None
    usd_etched: str | None = None
    eur: str | None = None
    eur_foil: str | None = None
    eur_etched: str | None = None
    tix: str | None = None

    # create a new Prices object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None):
        if not data:
            return cls()
        return cls(
            usd=data.get("usd"),
            usd_foil=data.get("usd_foil"),
            usd_etched=data.get("usd_etched"),
            eur=data.get("eur"),
            eur_foil=data.get("eur_foil"),
            eur_etched=data.get("eur_etched"),
            tix=data.get("tix"),
        )


# define the dataclass for the PreviewInfo schema
@dataclass(slots=True)
class PreviewInfo(_SerializableMixin):
    previewed_at: str | None = None
    source_uri: str | None = None
    source: str | None = None

    # create a new PreviewInfo object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        return cls(
            previewed_at=data.get("previewed_at"),
            source_uri=data.get("source_uri"),
            source=data.get("source"),
        )


# define the dataclass for the RelatedUris schema
@dataclass(slots=True)
class RelatedUris(_SerializableMixin):
    gatherer: str | None = None
    tcgplayer_infinite_articles: str | None = None
    tcgplayer_infinite_decks: str | None = None
    edhrec: str | None = None

    # create a new RelatedUris object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None):
        if not data:
            return cls()
        kwargs = {f.name: data.get(f.name) for f in fields(cls)}
        return cls(**kwargs)


# define the dataclass for the PurchaseUris schema
@dataclass(slots=True)
class PurchaseUris(_SerializableMixin):
    tcgplayer: str | None = None
    cardmarket: str | None = None
    cardhoarder: str | None = None

    # create a new PurchaseUris object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None):
        if not data:
            return None
        kwargs = {f.name: data.get(f.name) for f in fields(cls)}
        if all(v is None for v in kwargs.values()):
            return None
        return cls(**kwargs)


# define the dataclass for the ScryfallRelatedCard schema
@dataclass(slots=True)
class ScryfallRelatedCard(_SerializableMixin):
    object: str
    id: str
    component: str
    name: str
    type_line: str
    uri: str

    # create a new ScryfallRelatedCard object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        return cls(
            object=str(data["object"]),
            id=str(data["id"]),
            component=str(data["component"]),
            name=str(data["name"]),
            type_line=str(data["type_line"]),
            uri=str(data["uri"]),
        )


# define the dataclass for the CardFace schema
@dataclass(slots=True)
class CardFace(_SerializableMixin):
    object: str | None = None
    name: str | None = None
    mana_cost: str | None = None
    type_line: str | None = None
    oracle_text: str | None = None
    colors: list[str] | None = None
    color_indicator: list[str] | None = None
    power: str | None = None
    toughness: str | None = None
    loyalty: str | None = None
    defense: str | None = None
    artist: str | None = None
    artist_id: str | None = None
    artist_ids: list[str] | None = None
    illustration_id: str | None = None
    image_uris: ImageUris | None = None
    flavor_text: str | None = None
    flavor_name: str | None = None
    printed_name: str | None = None
    printed_text: str | None = None
    printed_type_line: str | None = None
    watermark: str | None = None
    layout: str | None = None
    oracle_id: str | None = None
    cmc: float | None = None

    # create a new CardFace object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        return cls(
            object=data.get("object"),
            name=data.get("name"),
            mana_cost=data.get("mana_cost"),
            type_line=data.get("type_line"),
            oracle_text=data.get("oracle_text"),
            colors=_str_list(data.get("colors")),
            color_indicator=_str_list(data.get("color_indicator")),
            power=data.get("power"),
            toughness=data.get("toughness"),
            loyalty=data.get("loyalty"),
            defense=data.get("defense"),
            artist=data.get("artist"),
            artist_id=data.get("artist_id"),
            artist_ids=_str_list(data.get("artist_ids")),
            illustration_id=data.get("illustration_id"),
            image_uris=_optional_model(ImageUris, data, "image_uris"),
            flavor_text=data.get("flavor_text"),
            flavor_name=data.get("flavor_name"),
            printed_name=data.get("printed_name"),
            printed_text=data.get("printed_text"),
            printed_type_line=data.get("printed_type_line"),
            watermark=data.get("watermark"),
            layout=data.get("layout"),
            oracle_id=data.get("oracle_id"),
            cmc=float(data["cmc"]) if data.get("cmc") is not None else None,
        )


# define the dataclass for the ScryfallCard schema
@dataclass(slots=True)
class ScryfallCard(_SerializableMixin):
    """
    Any Scryfall card layout.

    Single-faced cards populate root-level gameplay/print fields. Multi-faced
    layouts use ``card_faces``; root may omit ``image_uris``, ``mana_cost``, etc.
    Reversible cards omit root ``oracle_id`` (per-face ``oracle_id`` instead).
    """

    object: str
    id: str
    oracle_id: str | None = None
    multiverse_ids: list[int] | None = None
    mtgo_id: int | None = None
    mtgo_foil_id: int | None = None
    arena_id: int | None = None
    tcgplayer_id: int | None = None
    tcgplayer_etched_id: int | None = None
    cardmarket_id: int | None = None
    name: str | None = None
    lang: str | None = None
    released_at: str | None = None
    uri: str | None = None
    scryfall_uri: str | None = None
    layout: str | None = None
    highres_image: bool | None = None
    image_status: str | None = None
    image_uris: ImageUris | None = None
    mana_cost: str | None = None
    cmc: float | None = None
    type_line: str | None = None
    oracle_text: str | None = None
    power: str | None = None
    toughness: str | None = None
    loyalty: str | None = None
    defense: str | None = None
    colors: list[str] | None = None
    color_identity: list[str] | None = None
    color_indicator: list[str] | None = None
    keywords: list[str] | None = None
    all_parts: list[ScryfallRelatedCard] | None = None
    card_faces: list[CardFace] | None = None
    legalities: dict[str, str] | None = None
    games: list[str] | None = None
    reserved: bool | None = None
    game_changer: bool | None = None
    foil: bool | None = None
    nonfoil: bool | None = None
    finishes: list[str] | None = None
    oversized: bool | None = None
    promo: bool | None = None
    promo_types: list[str] | None = None
    reprint: bool | None = None
    variation: bool | None = None
    variation_of: str | None = None
    set_id: str | None = None
    set: str | None = None
    set_name: str | None = None
    set_type: str | None = None
    set_uri: str | None = None
    set_search_uri: str | None = None
    scryfall_set_uri: str | None = None
    rulings_uri: str | None = None
    prints_search_uri: str | None = None
    collector_number: str | None = None
    digital: bool | None = None
    rarity: str | None = None
    flavor_text: str | None = None
    flavor_name: str | None = None
    printed_name: str | None = None
    printed_text: str | None = None
    printed_type_line: str | None = None
    card_back_id: str | None = None
    artist: str | None = None
    artist_ids: list[str] | None = None
    illustration_id: str | None = None
    border_color: str | None = None
    frame: str | None = None
    frame_effects: list[str] | None = None
    security_stamp: str | None = None
    full_art: bool | None = None
    textless: bool | None = None
    booster: bool | None = None
    story_spotlight: bool | None = None
    watermark: str | None = None
    attraction_lights: list[int] | None = None
    edhrec_rank: int | None = None
    penny_rank: int | None = None
    preview: PreviewInfo | None = None
    prices: Prices | None = None
    related_uris: RelatedUris | None = None
    purchase_uris: PurchaseUris | None = None
    produced_mana: list[str] | None = None
    hand_modifier: str | None = None
    life_modifier: str | None = None
    content_warning: bool | None = None

    # create a new ScryfallCard object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        return cls(
            object=str(data["object"]),
            id=str(data["id"]),
            oracle_id=data.get("oracle_id"),
            multiverse_ids=_int_list(data.get("multiverse_ids")),
            mtgo_id=data.get("mtgo_id"),
            mtgo_foil_id=data.get("mtgo_foil_id"),
            arena_id=data.get("arena_id"),
            tcgplayer_id=data.get("tcgplayer_id"),
            tcgplayer_etched_id=data.get("tcgplayer_etched_id"),
            cardmarket_id=data.get("cardmarket_id"),
            name=data.get("name"),
            lang=data.get("lang"),
            released_at=data.get("released_at"),
            uri=data.get("uri"),
            scryfall_uri=data.get("scryfall_uri"),
            layout=data.get("layout"),
            highres_image=data.get("highres_image"),
            image_status=data.get("image_status"),
            image_uris=_optional_model(ImageUris, data, "image_uris"),
            mana_cost=data.get("mana_cost"),
            cmc=float(data["cmc"]) if data.get("cmc") is not None else None,
            type_line=data.get("type_line"),
            oracle_text=data.get("oracle_text"),
            power=data.get("power"),
            toughness=data.get("toughness"),
            loyalty=data.get("loyalty"),
            defense=data.get("defense"),
            colors=_str_list(data.get("colors")),
            color_identity=_str_list(data.get("color_identity")),
            color_indicator=_str_list(data.get("color_indicator")),
            keywords=_str_list(data.get("keywords")),
            all_parts=_list_of(ScryfallRelatedCard, data.get("all_parts")),
            card_faces=_list_of(CardFace, data.get("card_faces")),
            legalities=dict(data["legalities"])
            if data.get("legalities") is not None
            else None,
            games=_str_list(data.get("games")),
            reserved=data.get("reserved"),
            game_changer=data.get("game_changer"),
            foil=data.get("foil"),
            nonfoil=data.get("nonfoil"),
            finishes=_str_list(data.get("finishes")),
            oversized=data.get("oversized"),
            promo=data.get("promo"),
            promo_types=_str_list(data.get("promo_types")),
            reprint=data.get("reprint"),
            variation=data.get("variation"),
            variation_of=data.get("variation_of"),
            set_id=data.get("set_id"),
            set=data.get("set"),
            set_name=data.get("set_name"),
            set_type=data.get("set_type"),
            set_uri=data.get("set_uri"),
            set_search_uri=data.get("set_search_uri"),
            scryfall_set_uri=data.get("scryfall_set_uri"),
            rulings_uri=data.get("rulings_uri"),
            prints_search_uri=data.get("prints_search_uri"),
            collector_number=data.get("collector_number"),
            digital=data.get("digital"),
            rarity=data.get("rarity"),
            flavor_text=data.get("flavor_text"),
            flavor_name=data.get("flavor_name"),
            printed_name=data.get("printed_name"),
            printed_text=data.get("printed_text"),
            printed_type_line=data.get("printed_type_line"),
            card_back_id=data.get("card_back_id"),
            artist=data.get("artist"),
            artist_ids=_str_list(data.get("artist_ids")),
            illustration_id=data.get("illustration_id"),
            border_color=data.get("border_color"),
            frame=data.get("frame"),
            frame_effects=_str_list(data.get("frame_effects")),
            security_stamp=data.get("security_stamp"),
            full_art=data.get("full_art"),
            textless=data.get("textless"),
            booster=data.get("booster"),
            story_spotlight=data.get("story_spotlight"),
            watermark=data.get("watermark"),
            attraction_lights=_int_list(data.get("attraction_lights")),
            edhrec_rank=data.get("edhrec_rank"),
            penny_rank=data.get("penny_rank"),
            preview=_optional_model(PreviewInfo, data, "preview"),
            prices=Prices.from_dict(data.get("prices")),
            related_uris=RelatedUris.from_dict(data.get("related_uris")),
            purchase_uris=PurchaseUris.from_dict(data.get("purchase_uris")),
            produced_mana=_str_list(data.get("produced_mana")),
            hand_modifier=data.get("hand_modifier"),
            life_modifier=data.get("life_modifier"),
            content_warning=data.get("content_warning"),
        )


# define the dataclass for the ScryfallCardList schema
# collection of ScryfallCard objects
@dataclass(slots=True)
class ScryfallCardList(_SerializableMixin):
    object: str
    total_cards: int
    has_more: bool
    data: list[ScryfallCard]
    next_page: str | None = None

    # create a new ScryfallCardList object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        return cls(
            object=str(data["object"]),
            total_cards=int(data["total_cards"]),
            has_more=bool(data["has_more"]),
            data=[ScryfallCard.from_dict(item) for item in data["data"]],
            next_page=data.get("next_page"),
        )


# define the dataclass for the ScryfallCatalog schema
@dataclass(slots=True)
class ScryfallCatalog(_SerializableMixin):
    """
    Catalog response from Scryfall autocomplete and other catalog endpoints.

    Contains a list of string values (e.g., card names, artist names).
    """
    object: str
    total_values: int
    data: list[str]

    # create a new ScryfallCatalog object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        return cls(
            object=str(data["object"]),
            total_values=int(data["total_values"]),
            data=[str(item) for item in data["data"]],
        )


# define the dataclass for the ScryfallRuling schema
@dataclass(slots=True)
class ScryfallRuling(_SerializableMixin):
    """
    A single ruling or clarification about a Magic card.

    Rulings come from Gatherer or other official sources.
    """
    object: str
    oracle_id: str
    source: str
    published_at: str
    comment: str

    # create a new ScryfallRuling object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        return cls(
            object=str(data["object"]),
            oracle_id=str(data["oracle_id"]),
            source=str(data["source"]),
            published_at=str(data["published_at"]),
            comment=str(data["comment"]),
        )


# define the dataclass for the ScryfallRulingList schema
@dataclass(slots=True)
class ScryfallRulingList(_SerializableMixin):
    """
    List of rulings for a card.
    """
    object: str
    has_more: bool
    data: list[ScryfallRuling]

    # create a new ScryfallRulingList object from a dictionary
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        return cls(
            object=str(data["object"]),
            has_more=bool(data["has_more"]),
            data=[ScryfallRuling.from_dict(item) for item in data["data"]],
        )


# export the schemas
__all__ = [
    "ImageUris",
    "Prices",
    "PreviewInfo",
    "RelatedUris",
    "PurchaseUris",
    "ScryfallRelatedCard",
    "CardFace",
    "ScryfallCard",
    "ScryfallCardList",
    "ScryfallCatalog",
    "ScryfallRuling",
    "ScryfallRulingList",
]
