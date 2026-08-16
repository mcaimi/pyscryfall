import json
from pyscryfall.api import (
    search_card_by_id,
    search_cards_by_name,
    search_card_by_name_exact,
    search_card_by_name_fuzzy,
    search_cards_by_name_all,
    get_random_card,
    autocomplete_card_name,
    get_card_rulings,
)
from pyscryfall.schemas import (
    ScryfallCard,
    ScryfallCardList,
    ScryfallCatalog,
    ScryfallRuling,
    ScryfallRulingList,
)

JSON_DUMP: str = "tests/card-example.json"


# test search card by name
# use a card that is known to exist: "Sengir Vampire"
def test_search_card_by_name():
    card = search_cards_by_name("Sengir Vampire")

    # card should be found
    assert card is not None and isinstance(card, ScryfallCardList)

    # should be a list of cards (Sengir Vampire is a print of a card)
    assert len(card.data) > 0

    # Name should be Sengir Vampire
    assert card.data[0].name == "Sengir Vampire"


# test search card by id
# use a card that is known to exist: "Sengir Vampire"
def test_search_card_by_id():
    # use Sengir Vampire's id
    card = search_card_by_id("de652420-eacf-4f9d-9f13-c6bc02b0fa72")

    # card should be found
    assert card is not None

    # should be only one card
    assert isinstance(card, ScryfallCard)

    # Name should be Sengir Vampire
    assert card.name == "Sengir Vampire"


# test search card by name and convert to json
# use a card that is known to exist: "Sengir Vampire"
def test_search_card_by_name_to_json():
    card = search_cards_by_name("Sengir Vampire")

    # card should be found
    assert card is not None and isinstance(card, ScryfallCardList)

    # should be a list of cards (Sengir Vampire is a print of a card)
    assert len(card.data) > 0

    # Name should be Sengir Vampire
    assert card.data[0].name == "Sengir Vampire"

    # Convert to json
    assert card.to_json() is not None
    assert isinstance(card.to_json(), str)
    # json should be valid
    assert len(card.to_json()) > 0
    assert json.loads(card.to_json()) is not None


# test search card by id and convert to json
# use a card that is known to exist: "Sengir Vampire"
def test_search_card_by_id_to_json():
    card = search_card_by_id("de652420-eacf-4f9d-9f13-c6bc02b0fa72")

    # card should be found
    assert card is not None and isinstance(card, ScryfallCard)

    # Name should be Sengir Vampire
    assert card.name == "Sengir Vampire"

    # Convert to json
    assert card.to_json() is not None
    assert isinstance(card.to_json(), str)
    # json should be valid
    assert len(card.to_json()) > 0
    assert json.loads(card.to_json()) is not None


# test search card by name and convert to dictionary
# use a card that is known to exist: "Sengir Vampire"
def test_search_card_by_name_to_dictionary():
    card = search_cards_by_name("Sengir Vampire")

    # card should be found
    assert card is not None and isinstance(card, ScryfallCardList)

    # should be a list of cards (Sengir Vampire is a print of a card)
    assert len(card.data) > 0

    # Name should be Sengir Vampire
    assert card.data[0].name == "Sengir Vampire"

    # Convert to dictionary
    assert card.to_dict() is not None
    assert isinstance(card.to_dict(), dict)

    # dictionary should be valid
    assert len(card.to_dict()) > 0


# test search card by id and convert to dictionary
# use a card that is known to exist: "Sengir Vampire"
def test_search_card_by_id_to_dictionary():
    card = search_card_by_id("de652420-eacf-4f9d-9f13-c6bc02b0fa72")

    # card should be found
    assert card is not None and isinstance(card, ScryfallCard)

    # Name should be Sengir Vampire
    assert card.name == "Sengir Vampire"

    # Convert to dictionary
    assert card.to_dict() is not None
    assert isinstance(card.to_dict(), dict)

    # dictionary should be valid
    assert len(card.to_dict()) > 0


# test create card object by loading a json string dump
# use the dump of "Sengir Vampire" card from scryfall
# outputs ScryfallCardList
def test_load_card_from_json_string():
    # load example card from file
    with open(JSON_DUMP, "r") as j:
        dump_str: str = j.read()

    # make sure input is a string
    assert isinstance(dump_str, str)

    # make sure dump_str is not empty
    assert len(dump_str) > 0
    # json should be valid
    assert json.loads(dump_str) is not None

    # create card object
    card = ScryfallCardList.from_json_string(dump_str)

    # verify
    assert isinstance(card, ScryfallCardList) and card is not None
    assert len(card.data) > 0
    assert card.data[0].name == "Sengir Vampire"


# test create card object by loading a serialized dictionary
# use the dump of "Sengir Vampire" card from scryfall
# outputs ScryfallCardList
def test_load_card_from_serialized_dictionary():
    # load example card from file
    with open(JSON_DUMP, "r") as j:
        dump_dict: dict = json.loads(j.read())

    # make sure dump_dict is a dictionary
    assert isinstance(dump_dict, dict)

    # create card object
    card = ScryfallCardList.from_dict(dump_dict)

    # verify
    assert isinstance(card, ScryfallCardList) and card is not None
    assert len(card.data) > 0
    assert card.data[0].name == "Sengir Vampire"


# test exact name search
def test_search_card_by_name_exact():
    card = search_card_by_name_exact("Lightning Bolt")

    # card should be found
    assert card is not None and isinstance(card, ScryfallCard)

    # Name should be exactly Lightning Bolt
    assert card.name == "Lightning Bolt"


# test fuzzy name search
def test_search_card_by_name_fuzzy():
    # Use a partial/misspelled name (missing 'i' and 'g')
    card = search_card_by_name_fuzzy("Lightn Bolt")

    # card should be found
    assert card is not None and isinstance(card, ScryfallCard)

    # Should find Lightning Bolt
    assert card.name == "Lightning Bolt"


# test random card
def test_get_random_card():
    card = get_random_card()

    # card should be found
    assert card is not None and isinstance(card, ScryfallCard)

    # Should have basic fields
    assert card.id is not None
    assert card.name is not None


# test random card with query filter
def test_get_random_card_with_filter():
    card = get_random_card(q="t:creature")

    # card should be found
    assert card is not None and isinstance(card, ScryfallCard)

    # Should be a creature
    assert card.type_line is not None
    assert "Creature" in card.type_line


# test autocomplete
def test_autocomplete_card_name():
    catalog = autocomplete_card_name("Lightning")

    # should return a catalog
    assert catalog is not None and isinstance(catalog, ScryfallCatalog)

    # should have suggestions
    assert len(catalog.data) > 0

    # should include Lightning Bolt
    assert any("Lightning Bolt" in name for name in catalog.data)


# test card rulings
def test_get_card_rulings():
    # Use a card known to have rulings
    card = search_card_by_name_exact("Humility")
    rulings = get_card_rulings(card.id)

    # should return a ruling list
    assert rulings is not None and isinstance(rulings, ScryfallRulingList)

    # should have object type
    assert rulings.object == "list"

    # data should be a list (may be empty for some cards)
    assert isinstance(rulings.data, list)


# test pagination with generator
def test_search_cards_by_name_all_pagination():
    # Island has many printings, should span multiple pages
    # Use unique="prints" to get all printings, not just unique cards
    cards = list(search_cards_by_name_all("Island", unique="prints"))

    # should have many cards (Island has hundreds of printings)
    assert len(cards) > 175  # More than one page worth

    # all should be cards
    assert all(isinstance(c, ScryfallCard) for c in cards)

    # verify all are unique by ID
    ids = [c.id for c in cards]
    assert len(ids) == len(set(ids))