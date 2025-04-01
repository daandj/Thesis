import sys

import numpy as np
from gamemanager import GameManager
import games.minimal as mg
# import games.tictactoe as ttt

def main() -> int:
    raise NotImplementedError("This function is not implemented yet.")
    # game = ttt.TicTacToe(ttt.CBTPlayer(0),ttt.MCTSPlayer(1), print_flag=True)
    # game.set_board_size(5)
    # winner = game.play()

    # if game.points == 0:
    #     print("Er is helaas geen winnaar...")
    # else:
    #     print(f"De winnaar is speler {winner+1}!")
    # return 0

def minimal() -> int:
    means = np.random.random_sample((5,5))
    game = mg.Minimal(print_flag=True, means=means)
    gm = GameManager(game, mg.CBTMinimalPlayer(0), mg.HumanPlayer(1),
                     print_flag=True, data_flag=False)
    winner = gm.play()

    print(f"The outcome is {gm.points} and winner is player {winner}")
    return 0

if __name__ == '__main__':
    sys.exit(minimal())
