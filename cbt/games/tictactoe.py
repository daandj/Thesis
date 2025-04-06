from enum import IntEnum
from functools import reduce
from operator import add
import random
from cbt.algorithms.MCTS import MCTS
from cbt.algorithms.cbt_alg import CBT
from cbt.game import Game
from cbt.player import Player

class Move(IntEnum):
    EMPTY = -1
    X = 0
    O = 1

    def __str__(self):
        if self.value == Move.EMPTY:
            return " "
        return ["X", "O"][self.value]

class RandomPlayer(Player):
    def make_move(self, game: Game) -> int:
        return random.choice(game.moves)

class HumanPlayer(Player):
    def make_move(self, game: Game) -> int:
        if not isinstance(game, TicTacToe):
            raise RuntimeError("This player is only for TicTacToe")

        print("\n\nHet bord is:")

        game.print_board()

        print("")
        print("Kies uit een van de volgende vakjes:")
        TicTacToe.print_empty_board(game.size)
        print("")
        while True:
            input_str: str = input("Kies een vakje "
                                    f"(0-{game.size * game.size-1}): ")
            if (not input_str.isdigit()
                or int(input_str) > game.size * game.size-1
                or int(input_str) < 0):

                print("Dat is niet een geldige keuze... Probeer het opnieuw.")
                continue

            return int(input_str)

class MCTSPlayer(Player):
    def make_move(self, game: Game) -> int:
        if not isinstance(game, TicTacToe):
            raise RuntimeError("This player is only for TicTacToe")

        alg = MCTS(game)

        move = alg.run()
        return move

class CBTPlayer(Player):
    def make_move(self, game: Game) -> int:
        if not isinstance(game, TicTacToe):
            raise RuntimeError("This player is only for TicTacToe")

        alg = CBT(game)

        move = alg.run()
        return move

class TicTacToe(Game):
    """
    TicTacToe is a class representing the game of Tic Tac Toe.
    """
    board: list[list[int]]
    history: list[int]
    size: int
    _winner: Move

    def __init__(self, size: int = 3, print_flag: bool = False):
        super().__init__(print_flag=print_flag)
        self.set_board_size(size)
        self.player = 0
        self.history = []
        self._winner = Move.EMPTY

    def setup(self, *args) -> None:
        pass

    def set_board_size(self, size: int = 3) -> None:
        self.board = [[Move.EMPTY for _ in range(size)] for _ in range(size)]
        self.size = size

    def do(self, move: int) -> int:
        if self.board[move // self.size][move % self.size] != Move.EMPTY:
            return False

        if move < 0 or move > self.size*self.size-1:
            return False

        self.board[move // self.size][move % self.size] = self.player

        if self.print_flag:
            self.print_board()

        self.history.append(move)

        self.player = 1-self.player
        return self.player

    def undo(self) -> int:
        place = self.history.pop()

        if self.board[place // self.size][place % self.size] == Move.EMPTY:
            raise RuntimeError("Cannot undo an empty move")

        self.board[place // self.size][place % self.size] = Move.EMPTY

        self.player = 1-self.player
        return self.player

    @property
    def moves(self) -> list[int]:
        board_list: list[int] = reduce(add, self.board)
        empties = list(map(lambda x: x == Move.EMPTY, board_list))
        return [idx for idx, x in enumerate(empties) if x]

    @property
    def points(self) -> float:
        if not self.finished:
            raise RuntimeError("No points before finishing the game")

        points: float = 0.0

        if self._winner == Move.O:
            points = 0
        elif self._winner == Move.X:
            points = 1
        elif self._winner == Move.EMPTY:
            # Draw
            points = 0.5
        else:
            raise RuntimeError("Invalid winner")

        return points

    @property
    def name(self) -> str:
        return "TicTacToe"

    @property
    def num_players(self) -> int:
        return 2

    @property
    def finished(self) -> bool:
        # With thanks to Diapolo10
        # (https://gist.github.com/Diapolo10/0af07b0f4c3036ad8353fbc41e1c31b1)
        for player in [Move.X, Move.O]:

            # Check rows
            for row in self.board:
                if all(cell == player for cell in row):
                    self._winner = player
                    return True

            # Check columns
            for col in zip(*self.board):
                if all(cell == player for cell in col):
                    self._winner = player
                    return True

            # Check crosses (assumes 3x3 board)
            diag0 = [self.board[i][i] for i in range(self.size)]
            diag1 = [self.board[i][self.size - i - 1] for i in range(self.size)]
            if all(cell == player for cell in diag0):
                self._winner = player
                return True
            if all(cell == player for cell in diag1):
                self._winner = player
                return True

        if all(Move.EMPTY not in row for row in self.board):
            self._winner = Move.EMPTY
            return True
        return False

    @property
    def winner(self) -> int:
        """
        Return the winner of the game.
        """
        return self._winner.value

    def reset(self) -> None:
        """
        Reset the game state to its initial state.
        """
        self.set_board_size(self.size)
        self.history = []
        self.player = 0

    @classmethod
    def print_empty_board(cls, size: int = 3) -> None:
        print("+"+"--+"*size)
        for i in range(size):
            print("|",end="")
            for j in range(size):
                print(f"{(i*size+j):2d}", end="")
                print("|",end="")
            print("\n+"+"--+"*size)

    def print_board(self) -> None:
        print("+"+"-+"*len(self.board))
        for row in self.board:
            print("|",end="")
            for item in row:
                print(str(Move(item)), end="")
                print("|",end="")
            print("\n+"+"-+"*len(self.board))

        print("")
