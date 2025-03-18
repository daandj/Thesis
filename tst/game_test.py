import pytest

from games.klaverjas.klaverjas import KlaverjasGame
from games.klaverjas.klaverjasplayer import RandomPlayer

@pytest.fixture
def random_players_game() -> KlaverjasGame:
    [player1, player2, player3, player4] = [RandomPlayer(i) for i in range(0,4)]

    game = KlaverjasGame(player1, player2, player3, player4)
    return game

# Deal out random cards and check that every player has received enough
# and different cards
def test_deal(random_players_game: KlaverjasGame):
    random_players_game.setup()

    all_cards = []

    for player in random_players_game.players:
        all_cards.append(player.get_hand())
        assert len(player.get_hand()) == 8

    assert not any(all_cards.count(x) > 1 for x in all_cards)