import sys

from cbt.gamemanager import GameManager
import cbt.games.tictactoe as ttt

    # return 0

def minimal() -> int:
    game = ttt.TicTacToe(print_flag=True)
    gm = GameManager(game, ttt.HumanPlayer(0), ttt.HumanPlayer(1),
                     print_flag=True, data_flag=True)
    winner = gm.play()

    print(f"The outcome is {gm.points} and winner is player {winner}")
    return 0

if __name__ == '__main__':
    sys.exit(minimal())
