from typing import final
from game import Game
from player import Player

class GameManager:
    """
    Class for running a game. It takes the player algorithms and a game, and
    handles the communication between each part.
    """
    players: tuple[Player, ...]
    game: Game

    # Public methods
    def __init__(self, game: Game,
                 *players: Player,
                 print_flag: bool = False,
                 ):
        self.game = game
        self.set_players(players)
        self.print_flag = print_flag

    # For pretty printing using the std library print function
    def __str__(self) -> str:
        ret_str = f"{self.game.name} game with {self.game.num_players} players"
        ret_str += ", ".join([str(player) for player in self.players])
        return ret_str

    def set_players(
            self,
            players: tuple[Player, ...]
        ) -> None:
        if len(players) != self.game.num_players:
            raise ValueError(f'A game of {self.game.name} must'
                             f' have exactly {self.game.num_players} players')

        self.players = players

    @final
    def set_player(self, player: Player, position: int) -> None:
        if position < 0 or position > self.game.num_players:
            raise ValueError(f'Invalid place number for a player '
                             f'(must be between 0 and {self.game.num_players})')
        tmp_list = list(self.players)
        tmp_list[position] = player
        self.players = tuple(tmp_list)

    def play(self) -> int:
        next_player = 0
        self.game.reset()

        while not self.game.finished:
            new_move = self.players[next_player].make_move(self.game)
            next_player = self.game.do(new_move)

        return self.game.winner

    @property
    def points(self) -> float:
        return self.game.points