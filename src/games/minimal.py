from __future__ import annotations

import numpy as np
from game import Game
from player import Player

class HumanPlayer(Player):
    def make_move(self, moves: list[int]) -> int:
        while (True):
            input_str: str = input(f"Kies een getal tussen 0 en {len(moves)}: ")
            if (not input_str.isdigit()
                or int(input_str) not in moves
                or int(input_str) < 0):
                
                print("Dat is niet een geldige keuze... Probeer het opnieuw.")
                continue

            return int(input_str)
        
class CBTPlayer(Player):
    def make_move(self, moves: list[int]) -> int:
        # Placeholder for the actual CBT algorithm
        # In a real implementation, this would use the CBT algorithm to select a move
        return moves[0]
    

class Minimal(Game):
    means: np.ndarray
    rng: np.random.Generator = np.random.default_rng()
    choices: list[int | None]
    score: int | None

    def __init__(self, *players: Player, print = False, means: np.ndarray):
        super().__init__(*players, print=print)
        self.means = means
        self.choices = [None, None]
        self.score = None

        if print:
            self.print_means()

    def setup(self, *args) -> None:
        pass
    
    # Play one round of the game and then return the player whose turn it is next
    def play_round(self, player: int, print_flag: bool = False) -> int:
        # Ensure both players make valid moves
        move0 = self.players[0].make_move(self.moves(0))
        if not self.update(0, move0):
            raise ValueError(f"Player 0 made an invalid move: {move0}")
        
        if print_flag:
            self.print_moves()
        
        move1 = self.players[1].make_move(self.moves(1))
        if not self.update(1, move1):
            raise ValueError(f"Player 1 made an invalid move: {move1}")
    
        if print_flag:
            self.print_moves()

        return player
    
    def update(self, player: int, place: int) -> bool:
        # Ensure the move is valid and update the state
        if self.choices[player] is not None:
            return False
        if place not in self.moves(player):
            return False
        
        self.choices[player] = place
        return True
    
    def undo(self, player: int) -> None:
        self.choices[player] = None

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
            except IndexError:
                raise ValueError(f"Invalid choices for score calculation: {self.choices}")

        return self.score

    def moves(self, player: int) -> list[int]:
        return list(range(self.means.shape[player]))
    
    @property
    def name(self) -> str:
        return "Minimal Game"
    
    @property
    def num_players(self) -> int:
        return 2
    
    @property
    def finished(self) -> bool:
        return all(move != None for move in self.choices)
        
    @property
    def winner(self) -> int:
        return 1-int(self.points)

    def print_moves(self) -> None:
        for idx, move in enumerate(self.choices):
            if move != None:
                print(f"Player {idx} chose arm {move}")
        
        print("")
    
    def print_means(self) -> None:
        with np.printoptions(precision=2, suppress=True):
            print(self.means)