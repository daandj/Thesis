from __future__ import annotations

import numpy as np
from algorithms.minimal_CBT import CBTMinimal
from game import Game
from player import Player

class HumanPlayer(Player):
    def make_move(self, game: Game) -> int:
        while True:
            input_str: str = input(f"Kies een getal tussen 0 en {len(game.moves)}: ")
            if (not input_str.isdigit()
                or int(input_str) > len(game.moves)
                or int(input_str) < 0):

                print("Dat is niet een geldige keuze... Probeer het opnieuw.")
                continue

            return int(input_str)

class CBTMinimalPlayer(Player):
    def __init__(self, location, data_flag: bool = False):
        super().__init__(location, data_flag=data_flag)
        if location != 0:
            raise ValueError("CBTMinimalPlayer can only be used for player 0")

    def make_move(self, game: Game, data_flag: bool = False) -> int:
        alg = CBTMinimal(game, data_flag=data_flag)
        move = alg.run()
        return move

class Minimal(Game):
    means: np.ndarray
    rng: np.random.Generator = np.random.default_rng()
    choices: list[int | None]
    score: int | None

    def __init__(self, means: np.ndarray, print_flag = False):
        super().__init__(print_flag)
        self.means = means
        self.choices = [None, None]
        self.score = None
        self.player = 0

        if self.print_flag:
            self.print_means()

    def setup(self, *args) -> None:
        pass

    def do(self, move: int) -> int:
        """
        Play the next move.

        Validate the move, update the game state, and set the
        `player` instance variable to index of the next player.

        Args:
            move (int): The move to be played.

        Returns:
            int: The index of the next player.

        Raises:
            ValueError: If the move is invalid, the game is finished or the
                current player has already made a move.
        """
        if self.player >= len(self.choices):
            raise ValueError("Game is already finished")
        if self.choices[self.player] is not None:
            raise ValueError("Player has already made a move")
        if move not in self.moves:
            raise ValueError(f"Invalid move: {move} for player {self.player}")

        self.choices[self.player] = move
        self.player += 1
        return self.player

    def undo(self) -> int:
        self.player -= 1
        if self.player < 0:
            raise ValueError("No moves to undo")

        self.choices[self.player] = None
        return self.player

    def reset(self) -> None:
        self.choices = [None, None]
        self.player = 0
        self.score = None

    @property
    def points(self) -> float:
        # Ensure points are calculated only after the game is finished
        if not self.finished:
            raise RuntimeError("No points before finishing the game")

        if self.score is None:
            # Safely calculate the score using the means array
            try:
                self.score = int(
                    self.rng.binomial(1, self.means[tuple(self.choices)])
                )
            except IndexError as exc:
                raise ValueError(f"Invalid choices for score calculation: {self.choices}") from exc

        return self.score

    @property
    def moves(self) -> list[int]:
        return list(range(self.means.shape[self.player]))

    @property
    def name(self) -> str:
        return "Minimal Game"

    @property
    def num_players(self) -> int:
        return 2

    @property
    def finished(self) -> bool:
        return all(move is not None for move in self.choices)

    @property
    def winner(self) -> int:
        return 1-int(self.points)

    def print_means(self) -> None:
        with np.printoptions(precision=2, suppress=True):
            print(self.means)
