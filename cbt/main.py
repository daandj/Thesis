import sys

from cbt.gamemanager import GameManager
import cbt.games.tictactoe as ttt
from cbt.algorithms import CBT2

    # return 0

def minimal() -> int:
    game = ttt.TicTacToe(print_flag=False)
    cbt2player = CBT2.CBT2Player(0, print_flag=False)
    cbt2player.iterations = 10000
    cbt2player.set_parameters(10000.0, 1000.0)
    gm = GameManager(game, cbt2player, ttt.HumanPlayer(1),
                     print_flag=False, data_flag=True)
    winner = gm.play()

    print(f"The outcome is {gm.points} and winner is player {winner}")
    return 0

if __name__ == '__main__':
    sys.exit(minimal())
