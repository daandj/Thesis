from enum import IntEnum
from functools import reduce
from operator import add
import random
from algorithms.CBT1 import CBT1
from algorithms.MCTS import MCTS
from game import Game
from player import Player

class Move(IntEnum):
    empty = -1
    X = 0
    O = 1

    def __str__(self):
        if self.value == -1:
            return " "
        return ["X", "O"][self.value]
    
class TicTacToeBoard():
    board: list[list[int]]
    size: int
    winner: int
    prev_player: int

    def __init__(self, size: int):
        self.size = size
        self.board = [[Move.empty for _ in range(size)] for _ in range(size)]
        self.prev_player = 1
        self.winner = Move.empty.value

    def print(self) -> None:
        print("+"+"-+"*len(self.board))
        for row in self.board:
            print("|",end="")
            for item in row:
                if item == Move.empty:
                    print(" ", end="")
                else:
                    print(str(item), end="")
                print("|",end="")
            print("\n+"+"-+"*len(self.board))

    @property
    def moves(self) -> list[int]:
        board_list: list[int] = reduce(add, self.board)
        empties = list(map(lambda x: x == Move.empty, board_list))
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
    
        if all([Move.empty not in row for row in self.board]):
            self.winner = -1
            return True
        return False
    
    def update(self, place: int) -> bool:
        if self.board[place // self.size][place % self.size] != Move.empty:
            return False
        
        if place < 0 or place > self.size*self.size-1:
            return False
        
        self.board[place // self.size][place % self.size] = self.prev_player

        self.prev_player = (self.prev_player + 1) % 2

        return True
    
    @property
    def points(self) -> int:
        if not self.finished:
            raise RuntimeError("No points before finishing the game")
        
        points = 0

        if self.winner == Move.O:
            points = 1
        elif self.winner == Move.X:
            points = -1
        else:
            points = 0

        return points
    
    def undo(self, place: int) -> None:
        if (self.board[place // self.size][place % self.size] == Move.empty):
            raise RuntimeError("Cannot undo an empty move")
        
        self.board[place // self.size][place % self.size] = Move.empty
        self.prev_player = (self.prev_player + 1) % 2

class RandomPlayer(Player):
    def make_move(self, board: TicTacToeBoard) -> int:
        return random.choice(board.moves)
    
class HumanPlayer(Player):
    
    def make_move(self, board: TicTacToeBoard) -> int:
        print("\n\nHet bord is:")

        board.print

        print("")
        print("Kies uit een van de volgende vakjes:")
        TicTacToe.print_empty_board(board.size)
        print("")
        while (True):
            input_str: str = input("Kies een vakje "
                                    f"(0-{board.size*board.size-1}): ")
            if (not input_str.isdigit()
                or int(input_str) >= board.size*board.size
                or int(input_str) < 0):
                
                print("Dat is niet een geldige keuze... Probeer het opnieuw.")
                continue

            return int(input_str)
        
class MCTSPlayer(Player):
    def make_move(self, board: TicTacToeBoard) -> int:
        move = MCTS.run(board)
        return move
    
class CBT1Player(Player):
    def make_move(self, board: TicTacToeBoard) -> int:
        alg = CBT1(board)
        
        move = alg.run()
        return move 


class TicTacToe(Game):
    board: TicTacToeBoard

    def __init__(self, *players):
        super().__init__(*players)
        self.set_board_size()

    def setup(self, *args) -> None:
        pass

    def set_board_size(self, size: int = 3) -> None:
        self.board = TicTacToeBoard(size)
    
    # Play one round of the game and then return the player whose turn it is next
    def play_round(self, starting_player: int) -> int:
        tries = 10
        while (True):
            if tries <= 0:
                raise RuntimeError("To many illegal moves tried")
            tries -= 1

            move = self.players[starting_player].make_move(self.board)
            if self.board.update(move):
                break
    
        self.board.print()

        return 1-starting_player

    @property
    def points(self) -> int:
        return self.board.points
    
    @property
    def name(self) -> str:
        return "TicTacToe"
    
    @property
    def num_players(self) -> int:
        return 2

    @classmethod
    def print_empty_board(self, size: int = 3) -> None:
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
