from enum import IntEnum
from functools import reduce
from operator import add
import random
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

class RandomPlayer(Player):
    
    def make_move(self, board: list[list[int]]) -> int:
        board_list: list[int] = reduce(add, board)
        empties = list(map(lambda x: x == Move.empty, board_list))
        available_idx = [idx for idx, x in enumerate(empties) if x]

        return random.choice(available_idx)
    
class HumanPlayer(Player):
    
    def make_move(self, board: list[list[Move]]) -> int:
        print("Het bord is:")

        TicTacToe.print_board(board)

        print("")
        print("Kies uit een van de volgende vakjes:")
        TicTacToe.print_empty_board()
        print("")
        while (True):
            input_str: str = input("Kies een kaart om te spelen "
                                    f"(0-{len(board)*len(board)-1}): ")
            if (not input_str.isdigit()
                or int(input_str) >= len(board)*len(board)
                or int(input_str) < 0):
                
                print("Dat is niet een geldige keuze... Probeer het opnieuw.")
                continue

            return int(input_str)


class TicTacToe(Game):
    board: list[list[Move]]
    size: int
    winner: int

    def __init__(self, *players):
        super().__init__(*players)
        self.set_board_size()
        self.winner = Move.empty.value

    def setup(self, *args) -> None:
        pass

    def set_board_size(self, size: int = 3) -> None:
        self.size = size
        self.board = [[Move.empty for _ in range(size)] for _ in range(size)]
    
    # Play one round of the game and then return the player whose turn it is next
    def play_round(self, starting_player: int) -> int:
        tries = 10
        while (True):
            if tries <= 0:
                raise RuntimeError("To many illegal moves tried")
            tries -= 1

            move = self.players[starting_player].make_move(self.board)
            if self.update_board(move, Move(starting_player)):
                break
    
        TicTacToe.print_board(self.board)

        return 1-starting_player

    @property
    def points(self) -> list[int]:
        points: list[int] = [0] * len(self.players)
        for player in [Move.O, Move.X]:
            points[player.value] = 1 if self.winner == player.value else 0

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
    
        return False
    
    def update_board(self, place: int, move: Move) -> bool:
        if self.board[place // self.size][place % self.size] != Move.empty:
            return False
        
        if place < 0 or place > self.size*self.size-1:
            return False
        
        self.board[place // self.size][place % self.size] = move

        return True
    
    @classmethod
    def print_board(self, board: list[list[Move]]) -> None:
        print("+-+-+-+")
        for row in board:
            print("|",end="")
            for item in row:
                if item == Move.empty:
                    print(" ", end="")
                else:
                    print(str(item), end="")
                print("|",end="")
            print("\n+-+-+-+")


    @classmethod
    def print_empty_board(self, size: int = 3) -> None:
        print("+-+-+-+")
        for i in range(size):
            print("|",end="")
            for j in range(size):
                print(str(i*size+j), end="")
                print("|",end="")
            print("\n+-+-+-+")
