"""
This module implements the Contextual Bandit Tree (CBT) algorithm and its supporting
components for decision-making in game-like environments.

The CBT algorithm is designed to maximize outcomes by leveraging a contextual bandit
approach. It includes the `Bandit` class for managing bandit-related computations and
the `CBT` class for the tree search process.

Classes:
    Bandit: Implements a contextual bandit algorithm for decision-making.
    CBT: Implements the Contextual Bandit for Tree search (CBT) algorithm for maximizing outcomes.
"""

from __future__ import annotations
import copy
from math import sqrt, log
import random
import sys
from typing import Final
import numpy as np
import numpy.typing as npt

from cbt.game import Game

class CBTNode:
    n: int
    parent: CBTNode | None
    children: list[CBTNode]
    prev_move: int
    n_accent: int
    r: float
    depth: int
    leaf: bool
    p: npt.NDArray[np.float64]


    def __init__(self, parent: CBTNode | None = None):
        self.parent = parent
        self.n_accent = 0
        self.n = 0
        self.children = []
        self.r = 0

        self.depth = parent.depth+1 if parent else 0

    def add_child(self, move: int) -> CBTNode:
        child = CBTNode(self)
        child.prev_move = move
        self.children.append(child)
        return child

    def add_parent(self, parent: CBTNode) -> None:
        if self.parent:
            raise RuntimeError("Node already has a parent")

        self.parent = parent
        self.depth = self.parent.depth+1

    def print_tree(self) -> None:
        """
        Print the tree structure for debugging purposes.
        """
        print("\t" * self.depth + \
            f"Node: {self.depth=}, {self.n=}, {self.r=}, {self.n_accent=}",
            file=sys.stderr)
        for child in self.children:
            child.print_tree()

class UCBBandit:
    """
    Implements a Upper Confidence Bound bandit algorithm.
    """
    def __init__(self) -> None:
        self.rng = np.random.default_rng()

    def initialize_node(self, node: CBTNode, game: Game) -> None:
        """
        Initialize the node with uniform probabilities.
        """
        if game.finished:
            node.leaf = True
        else:
            length = len(game.moves)
            node.p = np.ones(length) / length
            node.leaf = False

    def update_node(self, node: CBTNode, game: Game, score: int) -> None:
        """
        Update the statistics of the given node and its children based on the score.
        """
        node.n += 1
        node.r += score

        if not node.leaf:
            for child in node.children:
                child.n_accent += 1

        if node.children:
            if node.leaf:
                return

            if node.depth == 0:
                idx, _ = max(enumerate(node.children), key=lambda tup: self.UCB1(tup[1]))
            elif node.depth == 1:
                idx, _ = min(enumerate(node.children), key=lambda tup: self.LCB1(tup[1]))
            else:
                raise RuntimeError("Invalid node depth")

            node.p = np.zeros(len(game.moves))
            node.p[idx] = 1

    def choose_arm(self, v: CBTNode) -> CBTNode:
        """
        Sample a child node (arm) based on the probability distribution p.
        """
        choice = self.rng.choice(len(v.children), p=v.p)
        return v.children[choice]

    def LCB1(self, v: CBTNode) -> float:
        """
        Calculate the UCB1 value for the given node.
        """
        k: Final[float] = 0.75
        return v.r / v.n - k * sqrt(log(v.n_accent) / v.n)

    def UCB1(self, v: CBTNode) -> float:
        """
        Calculate the UCB1 value for the given node.
        """
        k: Final[float] = 0.75
        return v.r / v.n + k * sqrt(log(v.n_accent) / v.n)

# class LCBBandit:
#     """
#     Implements the Lower Confidence Bound bandit algorithm.
#     """

#     def __init__(self) -> None:
#         self.rng = np.random.default_rng()

#     def initialize_node(self, node: CBTNode, game: Game) -> None:
#         """
#         Initialize the node with uniform probabilities.
#         """
#         if game.finished:
#             node.leaf = True
#         else:
#             length = len(game.moves)
#             node.p = np.ones(length) / length
#             node.leaf = False

#     def update_node(self, node: CBTNode, game: Game, score: int) -> None:
#         """
#         Update the statistics of the given node and its children based on the score.
#         """
#         self._update_node_statistics(node, score)

#         if not node.leaf:
#             self._update_children_statistics(node)

#         if node.children:
#             if node.leaf:
#                 return

#             idx, _ = min(enumerate(node.children), key=lambda tup: self.LCB1(tup[1]))

#             node.p = np.zeros(len(game.moves))
#             node.p[idx] = 1

#     def choose_arm(self, v: CBTNode) -> CBTNode:
#         """
#         Sample a child node (arm) based on the probability distribution p.
#         """
#         choice = self.rng.choice(len(v.children), p=v.p)
#         return v.children[choice]

#     def LCB1(self, v: CBTNode) -> float:
#         """
#         Calculate the UCB1 value for the given node.
#         """
#         k: Final[float] = 0.75
#         return v.r / v.n - k * sqrt(log(v.n_accent) / v.n)

#     def UCB1(self, v: CBTNode) -> float:
#         """
#         Calculate the UCB1 value for the given node.
#         """
#         k: Final[float] = 0.75
#         return v.r / v.n + k * sqrt(log(v.n_accent) / v.n)

#     # Helper methods
#     def _update_node_statistics(self, node: CBTNode, score: int) -> None:
#         """
#         Increment visit count and update the reward for the given node.
#         """
#         node.n += 1
#         node.r += score

#     def _update_children_statistics(self, node: CBTNode) -> None:
#         """
#         Increment the n_accent value for all children of the given node.
#         """
#         for child in node.children:
#             child.n_accent += 1

class UCBMinimal:
    """
    Implements the Contextual Bandits for Tree search (CBT)
    algorithm for maximizing outcomes in a game-like environment.
    """
    K: int
    nu: float
    gamma: float
    game: Game

    def __init__(self, game: Game,
                 data_flag: bool = False,
                 print_flag: bool = False) -> None:
        self.K: int = len(game.moves)
        self.moves = game.moves
        self.game = game
        self.print_data = data_flag
        self.print_flag = print_flag
        self.bandit = UCBBandit()

    def run(self, iters: int = 10000) -> int:
        """
        Run the CBT algorithm for a specified number of iterations and return the best move.
        """
        root = CBTNode()
        self.bandit.initialize_node(root, self.game)

        # Create all children of the root node.
        self.expand_root(root)

        for i in range(iters):
            v = self.select(root)

            res = self.simulate()

            self.backpropagate(v, res)

            if self.print_data:
                print(f"{i} {res}")
            if self.print_flag:
                if i % 10000 == 0:
                    print(f"t={i}", file=sys.stderr)

        # TODO: Think about what to return
        best_child = max(root.children, key=lambda child: child.n)

        if self.print_flag:
            root.print_tree()
        return best_child.prev_move

    def select(self, v: CBTNode) -> CBTNode:
        """
        Traverse the tree to select a node for expansion.
        """

        v = self.bandit.choose_arm(v)
        self.game.do(v.prev_move)

        if len(self.missing_moves(v)) == 0:
            # If all children are visited, select the best child based on UCB1.
            v = self.bandit.choose_arm(v)
            self.game.do(v.prev_move)
        else:
            v = self.expand(v)

        return v

    def expand_root(self, root: CBTNode) -> CBTNode:
        """
        Expand the root node by adding all possible children.
        """
        moves: list[int] = list(self.missing_moves(root))
        for move in moves:
            child = root.add_child(move)
            self.game.do(move)
            self.bandit.initialize_node(child, self.game)
            score = self.simulate()
            self.backpropagate(child, score)

        return root

    def expand(self, v: CBTNode) -> CBTNode:
        """
        Expand the tree by adding a new child node to the given node.
        """
        moves: list[int] = list(self.missing_moves(v))

        #TODO: Change this to adding all children at once.
        #UPDATE: This is hard, because those children aren't visited yet
        # which leads to a division by zero problem in de UCB1 calculation.

        new_move = random.choice(moves)
        v = v.add_child(new_move)

        self.game.do(new_move)
        self.bandit.initialize_node(v,self.game)

        return v

    def backpropagate(self, v: CBTNode, score: int) -> None:
        """
        Update the statistics of all nodes along the path from the given node to the root.
        """
        node: CBTNode | None = v
        while node:
            self.bandit.update_node(node, self.game, score)

            if node.parent is not None:
                self.game.undo()

            node = node.parent

    def simulate(self) -> int:
        """
        Simulate the game from the current board state to the end and return the score.
        """
        game: Game = copy.deepcopy(self.game)
        while not game.finished:
            moves: list[int] = list(game.moves)
            next_move: int = random.choice(moves)
            game.do(next_move)

        score = int(game.points)

        return score

    def missing_moves(self, v: CBTNode) -> list[int]:
        """
        Return a list of moves that are not yet explored from the given node.
        """
        res = set(self.game.moves).difference(map(lambda child: child.prev_move, v.children))
        return list(res)

    def regression_regret(self, t: int) -> float:
        """
        Calculate the regression regret for the given number of iterations.
        """
        return sqrt(t) # TODO: This, but correct.
