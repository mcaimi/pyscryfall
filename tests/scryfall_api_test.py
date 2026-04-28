from pyscryfall.api import search_card_by_id, search_cards_by_name
from pyscryfall.schemas import ScryfallCard, ScryfallCardList


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
