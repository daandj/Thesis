from typing import Tuple
import pytest

from games.klaverjas.definitions import Card, Suit, Trick, Value
from games.klaverjas.gamestate import GameState, GameStateReader
from player import Player, RandomPlayer

@pytest.fixture
# Returns a player with  a dealt hand
def player_with_hand() -> Player:
    p = RandomPlayer(0)
    p.deal([Card(Suit.HEARTS, Value.SEVEN),
            Card(Suit.HEARTS, Value.JACK),
            Card(Suit.CLUBS, Value.EIGHT),
            Card(Suit.CLUBS, Value.NINE),
            Card(Suit.DIAMONDS, Value.SEVEN),
            Card(Suit.DIAMONDS, Value.JACK),
            Card(Suit.DIAMONDS, Value.KING),
            Card(Suit.SPADES, Value.QUEEN)]
    )
    return p    

@pytest.fixture
# Returns an empty trick, state and accompanying reader
def empty_trick() -> Tuple[Trick, GameState, GameStateReader]:
    test = Trick()
    state = GameState()
    reader = GameStateReader(state)

    return test, state, reader

def test_first_legal_move(player_with_hand: Player,
                    empty_trick: Tuple[Trick, GameState, GameStateReader]):
    p = player_with_hand
    test, state, reader = empty_trick
    state.trump_card = Suit.CLUBS

    assert p.legal_moves(reader, test) == p.get_hand()

# A non trump card has been played, so the legal move should be to match
def test_second_legal_move_no_trump(player_with_hand: Player,
                    empty_trick: Tuple[Trick, GameState, GameStateReader]):
    p = player_with_hand
    test, state, reader = empty_trick

    state.trump_card = Suit.CLUBS
    test.play(Card(Suit.SPADES, Value.TEN))

    assert p.legal_moves(reader, test) == [Card(Suit.SPADES, Value.QUEEN)]

# The first move was a trump card, higher than one that the player has, but not
# the other, so they have to play of any trump cards in their hand.
def test_second_legal_move_trump_middle(player_with_hand: Player,
                    empty_trick: Tuple[Trick, GameState, GameStateReader]):
    p = player_with_hand
    test, state, reader = empty_trick

    state.trump_card = Suit.CLUBS
    test.play(Card(Suit.CLUBS, Value.ACE))

    legal_moves = p.legal_moves(state.trump_card, test)
    assert legal_moves == [Card(Suit.CLUBS, Value.NINE)]

# The first move was a trump card, higher than any that the player has, so 
# they have to play of any trump cards in their hand.
def test_second_legal_move_trump_lower(player_with_hand: Player, 
                    empty_trick: Tuple[Trick, GameState, GameStateReader]):
    p = player_with_hand
    test, state, reader = empty_trick

    state.trump_card = Suit.CLUBS
    test.play(Card(Suit.CLUBS, Value.SEVEN))

    legal_moves = p.legal_moves(reader.trump, test)
    assert len(legal_moves) == 2
    assert Card(Suit.CLUBS, Value.NINE) in legal_moves
    assert Card(Suit.CLUBS, Value.EIGHT) in legal_moves
    
def test_second_legal_move_trump_higher(player_with_hand: Player, 
                    empty_trick: Tuple[Trick, GameState, GameStateReader]):
    p = player_with_hand
    test, state, reader = empty_trick

    state.trump_card = Suit.CLUBS
    test.play(Card(Suit.CLUBS, Value.JACK))

    legal_moves = p.legal_moves(reader, test)
    assert len(legal_moves) == 2
    assert Card(Suit.CLUBS, Value.NINE) in legal_moves
    assert Card(Suit.CLUBS, Value.EIGHT) in legal_moves

def test_placeholder(player_with_hand: Player,
                    empty_trick: Tuple[Trick, GameState, GameStateReader]):
    p = player_with_hand
    test, state, reader = empty_trick

    state.trump_card = Suit.CLUBS
    test.play(Card(Suit.SPADES, Value.TEN))
    p.make_move(reader, test)

    expected_trick = Trick(Card(Suit.SPADES, Value.TEN),
                           Card(Suit.SPADES, Value.QUEEN))

    # Check that the played card is correctly in the trick object and the 
    # correct card is played (the only trump that is higher)
    assert test == expected_trick

    # Check that the hand is now seven cards and has no king of spaces left.
    assert len(p.get_hand()) == 7
    assert Card(Suit.SPADES, Value.QUEEN) not in p.get_hand()

    # Play a trump card, now the player can only play their trump, and it must
    # be higher
    test.play(Card(Suit.CLUBS, Value.ACE))

    expected_trick = Trick(Card(Suit.SPADES, Value.TEN),
                           Card(Suit.SPADES, Value.QUEEN),
                           Card(Suit.CLUBS, Value.ACE))
    assert test == expected_trick

    assert p.legal_moves(state.trump_card, test) == [Card(Suit.CLUBS, Value.NINE)]

def test_legal_moves_no_trumps_played():
    #TODO: Implement this
    assert True