from __future__ import annotations

import numpy as np
from game import Game
from player import Player

class HumanPlayer(Player):
    def make_move(self, board: MinimalBoard) -> int:
        while (True):
            input_str: str = input(f"Kies een getal tussen 0 en {len(board.moves)}: ")
            if (not input_str.isdigit()
                or int(input_str) not in board.moves
                or int(input_str) < 0):
                
                print("Dat is niet een geldige keuze... Probeer het opnieuw.")
                continue

            return int(input_str)
        
class MinimalBoard:
    means: np.ndarray
    winner: int | None
    choices: list[int | None]
    player: int
    rng: np.random.Generator = np.random.default_rng()

    def __init__(self, shape: tuple[int, int] = (5, 5)):
        self.winner = 0
        self.means = np.random.random_sample(shape)
        self.player = 0
        self.choices = [None, None]

    @property
    def moves(self) -> list[int]:
        return list(range(self.means.shape[self.player]))
    
    @property
    def finished(self) -> bool:
        if any(move == None for move in self.choices):
            return False
        # TODO: Test that is only done once
        self.outcome = self.rng.binomial(1, self.means[tuple(self.choices)]) # type: ignore
        return True
    
    def update(self, place: int) -> bool:
        if self.choices[self.player] != None:
            return False
        if place not in self.moves:
            return False
        
        self.choices[self.player] = place

        self.player = 1 - self.player

        return True
    
    @property
    def points(self) -> float:
        if not self.finished or self.winner == None:
            raise RuntimeError("No points before finishing the game")

        return float(self.winner)
    
    def undo(self, place: int) -> None:
        self.winner = None
        self.player = 1 - self.player
        self.choices[self.player] = None

    def print(self) -> None:
        for idx, move in enumerate(self.moves):
            if move:
                print(f"Player {idx} chose arm {move}")
        
        print("")

    def print_means(self) -> None:
        with np.printoptions(precision=2, suppress=True):
            print(self.means)

class Minimal(Game):
    board: MinimalBoard

    def __init__(self, *players: Player, print = False, shape: tuple[int, int] = (5,5)):
        super().__init__(*players, print=print)
        self.board = MinimalBoard(shape)
        if print:
            self.board.print_means()

    def setup(self, *args) -> None:
        pass

    def reshape(self, shape: tuple[int, int]) -> None:
        self.board = MinimalBoard(shape)
    
    # Play one round of the game and then return the player whose turn it is next
    def play_round(self, player: int, print_flag: bool = False) -> int:
        tries = 10
        while (True):
            if tries <= 0:
                raise RuntimeError("To many illegal moves tried")
            tries -= 1

            move = self.players[player].make_move(self.board)
            if self.board.update(move):
                break
    
        if print_flag:
            self.board.print()

        return 1-player

    @property
    def points(self) -> float:
        return self.board.points
    
    @property
    def name(self) -> str:
        return "Minimal Game"
    
    @property
    def num_players(self) -> int:
        return 2
    
    @property
    def finished(self) -> bool:
        return self.board.finished
        
    @property
    def winner(self) -> int:
        return int(self.board.points)