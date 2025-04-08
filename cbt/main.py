import sys

from cbt.gamemanager import GameManager
import cbt.games.tictactoe as ttt
from cbt.algorithms import CBT2

    # return 0

def minimal() -> int:
    game = ttt.TicTacToe(print_flag=False)
    cbt2player = CBT2.CBT2Player(0, print_flag=False)
    cbt2player.iterations = 10000
    cbt2player.set_parameters(10.0, 1.0)
    cbt2player2 = CBT2.CBT2Player(0, print_flag=False)
    cbt2player2.iterations = 10000
    cbt2player2.set_parameters(10.0, 1.0)
    gm = GameManager(game, cbt2player, cbt2player2,
                     print_flag=True, data_flag=False)
    winner = gm.play()

    print(f"The outcome is {gm.points} and winner is player {winner}")
    return 0

if __name__ == '__main__':
    sys.exit(minimal())
