import sys

from cbt.gamemanager import GameManager
import cbt.games.tictactoe as ttt
from cbt.algorithms import CBT2

    # return 0

def minimal() -> int:
    game = ttt.TicTacToe(print_flag=False)
    cbt2player = CBT2.CBT2Player(1, print_flag=False)
    cbt2player.iterations = 10000
    gm = GameManager(game, ttt.MCTSPlayer(0), cbt2player,
                     print_flag=False, data_flag=True)
    winner = gm.play()

    print(f"The outcome is {gm.points} and winner is player {winner}")
    return 0

if __name__ == '__main__':
    sys.exit(minimal())
