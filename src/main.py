import sys
from games.klaverjas.ISMCTSplayer import ISMCTSPlayer
from games.klaverjas.humanplayer import HumanPlayer
from games.klaverjas.klaverjas import KlaverjasGame

def main() -> int:
    player1 = HumanPlayer(0)
    player2 = ISMCTSPlayer(1)
    [player3, player4] = [ISMCTSPlayer(i+2) for i in range(0,2)]

    game = KlaverjasGame(player1, player2, player3, player4)
    winner = game.play()

    player1.print_trick(game.state.tricks[7])

    print("Spelers ", winner + 1, " en ", winner + 3, " hebben gewonnen met  ", 
          game.base_points[0], " versus ", game.base_points[1], " punten en ",
          game.roem[0], " versus ", game.roem[1], " roem!")

    return 0

if __name__ == '__main__':
    sys.exit(main())
