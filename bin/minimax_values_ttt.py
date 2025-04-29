#!/usr/bin/env python

from functools import reduce
from operator import add
import sys

from cbt.game import Game
import cbt.games.tictactoe as ttt

def main(size: int = 3) -> int:
    game = ttt.TicTacToe(size = size)

    moves = game.moves
    min_max: list[list[float]] = [[] for _ in range(len(moves))]

    for move in moves:
        leaves: list[tuple[float, float]]

        game.do(move)
        print(f"{move=}")

        second_moves = game.moves
        min_max[move] = [0.0] * len(moves)
        for second_move in second_moves:
            game.do(second_move)
            leaves = leave_chances(game)
            exp_value = reduce(add, map(lambda tup: tup[0] * tup[1], leaves))
            min_max[move][second_move] = exp_value
            game.undo()

        game.undo()

    print ("MinMax values:")
    for i, values in enumerate(min_max):
        for j, value in enumerate(values):
            print(f"({i},{j}): {value:.2f}")
    return 0

def leave_chances(state: Game, level: int = 1) -> list[tuple[float, float]]:
    """
    Returns an array of all possible leaves from a game state.
    """
    if state.finished:
        return [(state.points, (1.0/level))]

    res: list[tuple[float, float]] = []
    for move in state.moves:
        branching = len(state.moves)
        state.do(move)
        res += leave_chances(state, level * branching)
        state.undo()

    return res

if __name__ == '__main__':
    s = int(sys.argv[1])

    sys.exit(main(s))
