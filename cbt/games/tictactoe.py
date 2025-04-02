from enum import IntEnum
from functools import reduce
from operator import add
import random
from cbt.algorithms.cbt_alg import CBT
from cbt.algorithms.MCTS import MCTS
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

class TicTacToeBoard():
    board: list[list[int]]
    size: int
    winner: int
    prev_player: int

    def __init__(self, size: int):
        self.size = size
        self.board = [[Move.EMPTY for _ in range(size)] for _ in range(size)]
        self.prev_player = 0
        self.winner = Move.EMPTY.value

    def print(self) -> None:
        print("+"+"-+"*len(self.board))
        for row in self.board:
            print("|",end="")
            for item in row:
                print(str(Move(item)), end="")
                print("|",end="")
            print("\n+"+"-+"*len(self.board))

        print("")

    @property
    def moves(self) -> list[int]:
        board_list: list[int] = reduce(add, self.board)
        empties = list(map(lambda x: x == Move.EMPTY, board_list))
        return [idx for idx, x in enumerate(empties) if x]

    @property
    def finished(self) -> bool:
        # With thanks to Diapolo10
        # (https://gist.github.com/Diapolo10/0af07b0f4c3036ad8353fbc41e1c31b1)
        for player in [Move.X, Move.O]:

            # Check rows
            for row in self.board:
                if all(cell == player for cell in row):
                    self.winner = player.value
                    return True

            # Check columns
            for col in zip(*self.board):
                if all(cell == player for cell in col):
                    self.winner = player.value
                    return True

            # Check crosses (assumes 3x3 board)
            diag0 = [self.board[i][i] for i in range(self.size)]
            diag1 = [self.board[i][self.size - i - 1] for i in range(self.size)]
            if all(cell == player for cell in diag0):
                self.winner = player.value
                return True
            if all(cell == player for cell in diag1):
                self.winner = player.value
                return True

        if all(Move.EMPTY not in row for row in self.board):
            self.winner = -1
            return True
        return False

    def update(self, place: int) -> bool:
        if self.board[place // self.size][place % self.size] != Move.EMPTY:
            return False

        if place < 0 or place > self.size*self.size-1:
            return False

        self.board[place // self.size][place % self.size] = self.prev_player

        self.prev_player = (self.prev_player + 1) % 2

        return True

    @property
    def points(self) -> float:
        if not self.finished:
            raise RuntimeError("No points before finishing the game")

        points: float = 0.0

        if self.winner == Move.O:
            points = -1
        elif self.winner == Move.X:
            points = 1
        else:
            points = 0.0

        return points

    def undo(self, place: int) -> None:
        if self.board[place // self.size][place % self.size] == Move.EMPTY:
            raise RuntimeError("Cannot undo an empty move")

        self.board[place // self.size][place % self.size] = Move.EMPTY
        self.prev_player = (self.prev_player + 1) % 2

class RandomPlayer(Player):
    def make_move(self, game: Game) -> int:
        return random.choice(game.moves)

class HumanPlayer(Player):
    def make_move(self, game: Game) -> int:
        if not isinstance(game, TicTacToe):
            raise RuntimeError("This player is only for TicTacToe")

        print("\n\nHet bord is:")

        game.board.print()

        print("")
        print("Kies uit een van de volgende vakjes:")
        TicTacToe.print_empty_board(game.board.size)
        print("")
        while True:
            input_str: str = input("Kies een vakje "
                                    f"(0-{len(game.moves)-1}): ")
            if (not input_str.isdigit()
                or int(input_str) >= len(game.moves)
                or int(input_str) < 0):

                print("Dat is niet een geldige keuze... Probeer het opnieuw.")
                continue

            return int(input_str)

class MCTSPlayer(Player):
    def make_move(self, game: Game) -> int:
        if not isinstance(game, TicTacToe):
            raise RuntimeError("This player is only for TicTacToe")

        alg = MCTS(game.board)

        move = alg.run()
        return move

class CBTPlayer(Player):
    def make_move(self, game: Game) -> int:
        if not isinstance(game, TicTacToe):
            raise RuntimeError("This player is only for TicTacToe")

        alg = CBT(game.board)

        move = alg.run()
        return move


class TicTacToe(Game):
    """
    TicTacToe is a class representing the game of Tic Tac Toe.
    """
    board: TicTacToeBoard

    def __init__(self, print_flag: bool = False):
        super().__init__(print_flag=print_flag)
        self.set_board_size()
        self.player = 0

    def setup(self, *args) -> None:
        pass

    def set_board_size(self, size: int = 3) -> None:
        self.board = TicTacToeBoard(size)

    def do(self, move: int) -> int:
        if not self.board.update(move):
            raise RuntimeError("Illegal move")

        if self.print_flag:
            self.board.print()

        self.player = 1-self.player
        return self.player

    def undo(self) -> int:
        #TODO: Somehow find out what the previous move was
        # and undo that one.
        self.board.undo(self.board.moves[-1])
        self.player = 1-self.player
        return self.player

    @property
    def points(self) -> float:
        return self.board.points

    @property
    def name(self) -> str:
        return "TicTacToe"

    @property
    def num_players(self) -> int:
        return 2

    @classmethod
    def print_empty_board(cls, size: int = 3) -> None:
        print("+"+"--+"*size)
        for i in range(size):
            print("|",end="")
            for j in range(size):
                print(f"{(i*size+j):2d}", end="")
                print("|",end="")
            print("\n+"+"--+"*size)

    @property
    def finished(self) -> bool:
        return self.board.finished

    @property
    def winner(self) -> int:
        return 1 if self.points < 0 else 0
