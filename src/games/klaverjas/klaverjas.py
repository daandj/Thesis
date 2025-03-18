import random
from game import Game
from games.klaverjas.gamestate import GameState, GameStateReader
from player import Player
from games.klaverjas.definitions import Card, Trick

class KlaverjasGame(Game):
    state: GameState
    state_reader: GameStateReader

    def __init__(self, *players: Player):
        super().__init__(*players)
        self.state = GameState()
        self.state_reader = GameStateReader(self.state)

    @property
    def num_players(self) -> int:
        return 4
    
    @property
    def name(self) -> str:
        return "Klaverjas"
    
    @property
    def points(self) -> list[int]:
        return list(map(lambda points, roem: points + roem,
                     self.state.points, self.state.roem))
    
    @property
    def finished(self) -> int:
        return 8 == len(self.state_reader.tricks)
    
    def setup(self, starting_player: int = 0) -> None:
        card_nrs = list(range(0, 32))
        random.shuffle(card_nrs)

        for idx, player in enumerate(self.players):
            # Sanity check, so we don't deal out cards to play that already 
            # have them.
            if len(player.get_hand()) > 0:
                raise RuntimeWarning("Dealing out new cards when a player "
                                     "already has them should never happen")
            
            player.deal([Card.from_number(j) for j in card_nrs[8*idx:8*idx+8]])
        
        self.state.trump_card = self.players[starting_player].pick_trump(self.state_reader)

    def play_round(self, starting_player: int) -> int:
        trick = Trick()
        for j in range(4):
            self.players[(starting_player + j) % 4].make_move(self.state_reader, trick)

        normalized_trick = Trick.rotate(trick, starting_player)
        self.state.update(normalized_trick)

        starting_player = (starting_player + self.state.winner(trick)) % 4
        return starting_player