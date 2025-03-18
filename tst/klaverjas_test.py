import pytest

from games.klaverjas.definitions import Card, Suit, Trick, Value
from games.klaverjas.gamestate import GameState

@pytest.fixture
def spades_ten() -> Card:
    return Card(Suit.SPADES, Value.TEN)

@pytest.fixture
def full_trick() -> Trick:
    return Trick(Card(Suit.SPADES, Value.TEN),
                 Card(Suit.CLUBS, Value.EIGHT),
                 Card(Suit.DIAMONDS, Value.ACE),
                 Card(Suit.HEARTS, Value.KING))

@pytest.fixture
def game_state() -> GameState:
    game_state = GameState()
    game_state.trump_card = Suit.HEARTS
    return game_state

def test_card_init_values(spades_ten: Card):
    assert spades_ten.suit == Suit.SPADES
    assert spades_ten.value == Value.TEN
    assert spades_ten.number == 8*Suit.SPADES.value+Value.TEN.value

def test_card_str(spades_ten: Card):
    assert str(spades_ten) == "♠10"

def test_card_hash(spades_ten: Card):
    assert hash(spades_ten) == hash(Card(Suit.SPADES, Value.TEN))
    assert hash(spades_ten) != hash(Card(Suit.CLUBS, Value.ACE))

def test_trick_neq(spades_ten: Card):
    assert Trick(spades_ten) != Trick()
    assert Trick() != Trick(spades_ten)

    assert Trick(spades_ten) != Trick(Card(Suit.CLUBS, Value.EIGHT))

def test_trick_eq(spades_ten: Card):
    assert Trick() == Trick()
    assert Trick(spades_ten) == Trick(spades_ten)
    assert Trick(spades_ten) == Trick(Card(Suit.SPADES, Value.TEN))
    
    card1 = Trick(Card(Suit.CLUBS, Value.JACK), Card(Suit.CLUBS, Value.NINE))
    card2 = Trick(Card(Suit.CLUBS, Value.JACK), Card(Suit.CLUBS, Value.NINE))
    assert card1 == card2
    assert card1 == card1


def test_trick_rotate(full_trick: Trick):
    test_trick = Trick(Card(Suit.HEARTS, Value.KING),
          Card(Suit.SPADES, Value.TEN),
          Card(Suit.CLUBS, Value.EIGHT),
          Card(Suit.DIAMONDS, Value.ACE))
    test_trick._Trick__starting_player = 1
    assert Trick.rotate(full_trick,1) == test_trick
    assert Trick.rotate(full_trick, 4).starting_player == 0
    assert Trick.rotate(full_trick,4) == full_trick
    test_trick = Trick(Card(Suit.CLUBS, Value.EIGHT),
          Card(Suit.DIAMONDS, Value.ACE),
          Card(Suit.HEARTS, Value.KING),
          Card(Suit.SPADES, Value.TEN))
    test_trick._Trick__starting_player = 3

    assert Trick.rotate(full_trick,3) == test_trick

def test_winner(game_state: GameState):
    test_trick = Trick(Card(Suit.CLUBS, Value.EIGHT),
                       Card(Suit.DIAMONDS, Value.ACE),
                       Card(Suit.HEARTS, Value.KING),
                       Card(Suit.SPADES, Value.TEN))
    test_trick._Trick__starting_player = 3
    game_state.trump_card = Suit.SPADES

    assert game_state.winner(test_trick) == 3

    game_state.trump_card = Suit.CLUBS
    assert game_state.winner(test_trick) == 0

    test_trick = Trick(Card(Suit.CLUBS, Value.JACK),
                       Card(Suit.CLUBS, Value.ACE),
                       Card(Suit.HEARTS, Value.KING),
                       Card(Suit.SPADES, Value.TEN))
    game_state.trump_card = Suit.DIAMONDS

    assert game_state.winner(test_trick) == 1

    game_state.trump_card = Suit.CLUBS
    assert game_state.winner(test_trick) == 0

def test_gamestate_update():
    assert True
    #TODO: Write this test and more

def test_gamestate__roem_trick1(game_state: GameState):
    assert 40 == game_state._GameState__roem_trick(Trick(
        Card(Suit.HEARTS, Value.ACE),
        Card(Suit.HEARTS, Value.KING),
        Card(Suit.HEARTS, Value.QUEEN),
        Card(Suit.HEARTS, Value.SEVEN)
    ))

def test_gamestate__roem_trick2(game_state: GameState):
    assert 70 == game_state._GameState__roem_trick(Trick(
        Card(Suit.HEARTS, Value.ACE),
        Card(Suit.HEARTS, Value.KING),
        Card(Suit.HEARTS, Value.QUEEN),
        Card(Suit.HEARTS, Value.JACK)
    ))
    assert 20 == game_state._GameState__roem_trick(Trick(
        Card(Suit.HEARTS, Value.QUEEN),
        Card(Suit.HEARTS, Value.JACK),
        Card(Suit.HEARTS, Value.TEN),
        Card(Suit.DIAMONDS, Value.KING)
    ))

def test_gamestate__roem_trick_four_jacks(game_state: GameState):
    assert 200 == game_state._GameState__roem_trick(Trick(
        Card(Suit.HEARTS, Value.JACK),
        Card(Suit.CLUBS, Value.JACK),
        Card(Suit.DIAMONDS, Value.JACK),
        Card(Suit.SPADES, Value.JACK)
    ))
    assert True

def test_gamestate__roem_trick_four_nines(game_state: GameState):
    assert 0 == game_state._GameState__roem_trick(Trick(
        Card(Suit.HEARTS, Value.NINE),
        Card(Suit.CLUBS, Value.NINE),
        Card(Suit.DIAMONDS, Value.NINE),
        Card(Suit.SPADES, Value.NINE)
    ))
    assert True