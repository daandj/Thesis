import sys
from ISMCTSplayer import ISMCTSPlayer
from game import Game
from humanplayer import HumanPlayer
import klaverjas

def main() -> int:
    player1 = HumanPlayer(0)
    player2 = ISMCTSPlayer(1)
    [player3, player4] = [ISMCTSPlayer(i+2) for i in range(0,2)]

    game = Game(player1, player2, player3, player4)
    winner = game.play()

    player1.print_trick(game.state.tricks[7])

    print("Spelers ", winner + 1, " en ", winner + 3, " hebben gewonnen met  ", 
          game.points[0], " versus ", game.points[1], " punten en ",
          game.roem[0], " versus ", game.roem[1], " roem!")

    return 0

def test():
    print(type(klaverjas.Suit.list()[0]))

if __name__ == '__main__':
    sys.exit(test())
