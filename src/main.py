import sys

import numpy as np
import games.minimal as min
import games.tictactoe as ttt

def main() -> int:
    game = ttt.TicTacToe(ttt.CBTPlayer(0),ttt.MCTSPlayer(1), print=True)
    game.set_board_size(5)
    winner = game.play()

    if game.points == 0:
        print(f"Er is helaas geen winnaar...")
    else:
        print(f"De winnaar is speler {winner+1}!")
    return 0

def minimal() -> int:
    means = np.random.random_sample((5,5))
    game = min.Minimal(min.CBTPlayer(0),
                       min.HumanPlayer(1),
                       print=True, means=means)
    game.play()

    print(f"The outcome is {game.points} and winner is player {game.winner}")
    return 0

if __name__ == '__main__':
    sys.exit(minimal())
