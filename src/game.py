from functools import reduce
from operator import add
import random
from klaverjas import Card, GameStateReader, Trick, GameState, Value
from player import Player

class Game:
    players: tuple[Player, ...]
    state: GameState

    # Public methods

    def __init__(self, *players: Player):
        self.state = GameState()
        self.state_reader = GameStateReader(self.state)
        self.set_players(players)

    # For pretty printing using the std library print function
    def __str__(self):
        pass

    def set_players(
            self, 
            players: tuple[Player, ...]
        ) -> None:
        if len(players) != 4:
            raise ValueError('A game of Klaverjas must have exactly 4 players')
        
        self.players = players

    def set_player(self, player: Player, position: int) -> None:
        if position < 0 or position > 3:
            raise ValueError('Invalid place number for a player (must be between 0 and 3)')
        tmp_list = list(self.players)
        tmp_list[position] = player
        self.players = tuple(tmp_list)
    
    def play(self) -> int:
        self.deal()
        starting_player = 0
        self.state.trump_card = self.players[starting_player].pick_trump(self.state_reader)

        for _ in range(8):
            trick = Trick()
            for j in range(4):
                self.players[(starting_player + j) % 4].make_move(self.state_reader, trick)

            normalized_trick = Trick.rotate(trick, starting_player)
            self.state.update(normalized_trick)

            starting_player = (starting_player + self.state.winner(trick)) % 4

        totals = list(map(lambda points, roem: points + roem,
                     self.state.points, self.state.roem))
        max_points = max(totals)
        winner = totals.index(max_points)

        return winner
        
    # Give everyone their random cards
    def deal(self) -> None:
        card_nrs = list(range(0, 32))
        random.shuffle(card_nrs)

        for idx, player in enumerate(self.players):
            # Sanity check, so we don't deal out cards to play that already 
            # have them.
            if len(player.get_hand()) > 0:
                raise RuntimeWarning("Dealing out new cards when a player "
                                     "already has them should never happen")
            
            player.deal([Card.from_number(j) for j in card_nrs[8*idx:8*idx+8]])

    @property
    def points(self) -> list[int]:
        return self.state.points
    
    @property
    def roem(self) -> list[int]:
        return self.state.roem