import json
from pyscryfall.api import search_card_by_id, search_cards_by_name
from pyscryfall.schemas import ScryfallCard, ScryfallCardList

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