import sys
from games.klaverjas.ISMCTSplayer import ISMCTSPlayer
from games.klaverjas.humanplayer import HumanPlayer
from games.klaverjas.klaverjas import KlaverjasGame
import games.tictactoe as ttt

def main() -> int:
    player1 = HumanPlayer(0)
    player2 = ISMCTSPlayer(1)
    [player3, player4] = [ISMCTSPlayer(i+2) for i in range(0,2)]

    for i in range(4):

        game = KlaverjasGame(player1, player2, player3, player4)
        winner = game.play()

        print(f"Spel {i}: Spelers ", winner + 1, " en ", winner + 3, " hebben gewonnen met  ", 
                game.base_points[0], " versus ", game.base_points[1], " punten en ",
                game.roem[0], " versus ", game.roem[1], " roem!")

    return 0

def tictactoe() -> int:
    game = ttt.TicTacToe(ttt.HumanPlayer(0), ttt.RandomPlayer(1))
    game.set_board_size(4)
    winner = game.play()

    print(f"De winnaar is speler {winner+1}!")
    return 0

if __name__ == '__main__':
    sys.exit(tictactoe())
