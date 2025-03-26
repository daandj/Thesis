import sys
import games.tictactoe as ttt

def main() -> int:
    game = ttt.TicTacToe(ttt.CBT1Player(0),ttt.MCTSPlayer(1), print=True)
    game.set_board_size(5)
    winner = game.play()

    if game.points == 0:
        print(f"Er is helaas geen winnaar...")
    else:
        print(f"De winnaar is speler {winner+1}!")
    return 0

if __name__ == '__main__':
    sys.exit(main())
