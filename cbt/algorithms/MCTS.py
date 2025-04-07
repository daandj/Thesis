from __future__ import annotations
import copy
from math import log, sqrt
import random
import sys
from typing import Final

from cbt.game import Game

class MCTSNode:
    n: int
    parent: MCTSNode | None
    children: list[MCTSNode]
    prev_move: int
    n_accent: int
    r: float
    depth: int

    def __init__(self, parent: MCTSNode | None = None):
        self.parent = parent
        self.n_accent = 0
        self.n = 0
        self.children = []
        self.r = 0

        self.depth = parent.depth+1 if parent else 0

    def add_child(self, move: int) -> MCTSNode:
        child = MCTSNode(self)
        child.prev_move = move
        self.children.append(child)
        return child

    def add_parent(self, parent: MCTSNode) -> None:
        if self.parent:
            raise RuntimeError("Node already has a parent")

        self.parent = parent
        self.depth = self.parent.depth+1

    def reward(self, b: Game) -> float:
        if b.player == 0: # This gives an error, because the player is not
            # exposed. However, most game do have the variable.
            # TODO: Rewrite this to use the return values of `do()` and `undo()`
            # instead of the player variable.
            return self.r

        return -self.r

class MCTS:
    b: Game

    def __init__(self, game: Game,
                 data_flag: bool = False,
                 print_flag: bool = False):
        self.b = game
        self.data_flag = data_flag
        self.print_flag = print_flag

    def run(self, iters: int = 1000) -> int:

        root = MCTSNode()

        for i in range(iters):
            v = self.select(root)

            if len(self.missing_moves(v)) > 0:
                v = self.expand(v)

            res = self.simulate()
            self.backpropagate(v, res)

            if self.data_flag:
                print(f"{i} {res}")

            if self.print_flag:
                if i % 10000 == 0:
                    print(f"t={i}", file=sys.stderr)

        best_child = max(root.children, key=lambda child: child.n)
        return best_child.prev_move

    def select(self, v: MCTSNode) -> MCTSNode:
        def UCB1(v: MCTSNode) -> float:
            k: Final[float] = 0.75
            return v.reward(self.b)/v.n+k*sqrt(log(v.n_accent)/v.n)

        while not self.b.finished \
            and len(self.missing_moves(v)) == 0:
            v = max(v.children, key=UCB1)
            self.b.do(v.prev_move)
        return v

    def expand(self, v: MCTSNode) -> MCTSNode:
        moves: list[int] = list(self.missing_moves(v))

        new_move = random.choice(moves)
        v = v.add_child(new_move)

        self.b.do(v.prev_move)
        return v

    # Update visitations and scores in the entire tree
    def backpropagate(self, v: MCTSNode, score: float) -> None:
        node: MCTSNode | None = v
        while node:
            node.n += 1
            node.r = node.r + score

            # Here n' is incremented for all children, it should be
            # siblings according to Cowling et al. (2012).
            # TODO: Check that that makes a difference
            for child in node.children:
                child.n_accent += 1

            if node.parent is not None:
                self.b.undo()

            node = node.parent


    # Simulate the rest of this determinization and return the end score.
    def simulate(self) -> float:
        board: Game = copy.deepcopy(self.b)
        while not board.finished:
            moves: list[int] = list(board.moves)
            next_move: int = random.choice(moves)
            board.do(next_move)

        score = board.points

        return score

    def missing_moves(self, v: MCTSNode) -> list[int]:
        res = set(self.b.moves).difference(map(lambda child: child.prev_move, v.children))
        return list(res)
