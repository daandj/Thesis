"""
This module defines the GameManager class.
"""

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
                 data_flag: bool = False
                 ):
        """
        Initialize the game manager with a game, players and flags.

        Args:
            game (Game): An implementation of the rules of some game.
            players (tuple[Player]): The player algorithms, using a strategy pattern.
            print_flag (bool): Flag to control printing of game state.
            data_flag (bool): Flag to control printing of data later analysis.
        """
        self.game = game
        self.set_players(players)
        self.print_flag = print_flag
        self.data_flag = data_flag

    def __str__(self) -> str:
        """
        Return a string representation naming the game and containing the player algorithms.
        """
        ret_str = f"{self.game.name} game with {self.game.num_players} players"
        ret_str += ", ".join([str(player) for player in self.players])
        return ret_str

    def set_players(
            self,
            players: tuple[Player, ...]
        ) -> None:
        """
        Set the players for the game.

        Raises:
            ValueError: If the number of players does not match the game's requirements.
        """
        if len(players) != self.game.num_players:
            raise ValueError(f'A game of {self.game.name} must'
                             f' have exactly {self.game.num_players} players')

        self.players = players

    @final
    def set_player(self, player: Player, position: int) -> None:
        """
        Set a specific player at a given position.

        Raises:
            ValueError: If the position is invalid.
        """
        if position < 0 or position > self.game.num_players:
            raise ValueError(f'Invalid place number for a player '
                             f'(must be between 0 and {self.game.num_players})')
        tmp_list = list(self.players)
        tmp_list[position] = player
        self.players = tuple(tmp_list)

    def play(self) -> int:
        """
        Run the game until it finishes.

        Ask the next players algorithm to choose a move and then update the
        game state, and repeat this until the game is finished.

        Returns:
            int: The index of the winning player.
        """
        next_player = 0
        self.game.reset()

        while not self.game.finished:
            #TODO: replace the [5,5] on the next line with something.
            new_move = self.players[next_player].make_move([5,5])

            if self.print_flag:
                print(f"Player {next_player} chose arm {new_move}")

            next_player = self.game.do(new_move)

        return self.game.winner

    @property
    def points(self) -> float:
        """
        Get the current points of the game.

        Returns:
            float: The points scored in the game.
        """
        return self.game.points