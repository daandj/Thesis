import algorithms.ISMCTS as ISMCTS
from games.klaverjas.ISMCTSplayer import ISMCTSPlayer
import pytest

from games.klaverjas.klaverjas import Card, Suit, Trick, Value

# Boilerplate

@pytest.fixture
def new_hand() -> list[Card]:
    return [Card(Suit.HEARTS, Value.SEVEN),
            Card(Suit.HEARTS, Value.JACK),
            Card(Suit.CLUBS, Value.EIGHT),
            Card(Suit.CLUBS, Value.NINE),
            Card(Suit.DIAMONDS, Value.SEVEN),
            Card(Suit.DIAMONDS, Value.JACK),
            Card(Suit.DIAMONDS, Value.KING),
            Card(Suit.SPADES, Value.QUEEN)]

@pytest.fixture
def new_player() -> ISMCTSPlayer:
    return ISMCTSPlayer(0)

@pytest.fixture
def new_player_with_hand(new_player: ISMCTSPlayer,
                         new_hand: list[Card]) -> ISMCTSPlayer:
    new_player.deal(new_hand)
    return new_player

@pytest.fixture
def determinization() -> ISMCTS.Determinization:
    pass

# Test the ISMCTS class

def test__get_cards(new_player_with_hand: ISMCTSPlayer):

    assert new_player_with_hand.iset[1] == new_player_with_hand.iset[2]
    assert new_player_with_hand.iset[1] == new_player_with_hand.iset[3]

    assert Card(Suit.DIAMONDS, Value.SEVEN) not in new_player_with_hand.iset[1]
    assert Card(Suit.SPADES, Value.SEVEN) in new_player_with_hand.iset[1]

    # Make sure that the iset are in fact different object and that updating one,
    # does not change the other:
    new_player_with_hand.iset[1].remove(Card(Suit.SPADES, Value.SEVEN))
    assert Card(Suit.SPADES, Value.SEVEN) in new_player_with_hand.iset[2]

# 'We' are the first player and played a trump jack, the next player plays an
# ten of clubs, so their iset may not contain a trump card anymore.
def test_update_iset(new_player_with_hand: ISMCTSPlayer):
    player = new_player_with_hand
    trick = Trick(Card(Suit.HEARTS, Value.JACK))
    trump = Suit.HEARTS

    player.update_iset(
        trump,
        trick,
        Card(Suit.CLUBS, Value.TEN),
        1
    )

    for iset in player.iset:
        assert Card(Suit.CLUBS, Value.TEN) not in iset
    
    for card in player.iset[1]:
        assert card.suit != trump

def test_determinize():
    # Ideas to test the determinization function:
    # - Test that it doesn't give an IndexError, to prove that it doesn't 
    #   take more items from the info_set than there are items in it.
    # - Test that the info_set item is not changed in the function i.e.
    #   that internally it uses a copy.
    assert True

def test_simulate(determinization: ISMCTS.Determinization):
    #TODO: Write the determinization fixture and then this should work.
    assert True
    # determinization_old = copy.deepcopy(determinization)
    # results: list[int] = ISMCTS.ISMCTS.simulate(determinization)
    # assert len(results) == 2

    # # Check that the determinization is exactly as it was
    # assert determinization_old == determinization