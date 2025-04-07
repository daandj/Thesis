"""
This module implements the Contextual Bandit Tree (CBT) algorithm and its supporting
components for decision-making in game-like environments.

The CBT algorithm is designed to maximize outcomes by leveraging a contextual bandit
approach. It includes the `Bandit` class for managing bandit-related computations and
the `CBT2` class for the tree search process.

Classes:
    Bandit: Implements a contextual bandit algorithm.
    CBT2: Implements the Contextual Bandit for Tree search (CBT) algorithm.
    CBT2Player: A player that uses the CBT1 algorithm to make decisions in any game.
"""

from __future__ import annotations
import copy
import random
import sys
import numpy as np
import numpy.typing as npt

from cbt.game import Game
from cbt.player import Player

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
    b: npt.NDArray[np.float64]
    mu_hat: npt.NDArray[np.float64]
    A_inv: npt.NDArray[np.float64]


    def __init__(self, parent: CBTNode | None = None):
        self.parent = parent
        self.n_accent = 0
        self.n = 0
        self.children = []

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

class CBandit:
    """
    Implements a contextual bandit algorithm for decision-making in the CBT framework.
    """
    def __init__(self, nu: float = 10, gamma: float = 0.5) -> None:
        self.nu = nu
        self.gamma = gamma
        self.rng = np.random.default_rng()

    def initialize_node(self, node: CBTNode, game: Game) -> None:
        """
        Initialize the given node with uniform probabilities, identity matrix, and zero vectors.
        """
        node.leaf = False

        length = len(game.moves)
        node.p = np.ones(length) / length
        node.b = np.zeros(length)
        node.A_inv = np.identity(length)
        node.mu_hat = np.ones(length) / length

    def update_node(self, node: CBTNode, game: Game, score: int, player: int) -> None:
        """
        Update the statistics of the given node and its children based on the score.
        """
        if game.finished:
            node.leaf = True
            node.r = score
            return

        if node.children:
            self._update_distribution(node, game, player)

            self._update_regression(node, score)
        else:
            pass


    def choose_arm(self, v: CBTNode) -> CBTNode:
        """
        Sample a child node (arm) based on the probability distribution p.
        """
        choice = self.rng.choice(len(v.children), p=v.p)
        return v.children[choice]

    def _update_distribution(self, node: CBTNode, game: Game, player: int) -> None:
        if not node.children:
            raise RuntimeError("Node has no children")

        pi = np.zeros(len(node.children))
        for idx, child in enumerate(node.children):
            if child.leaf:
                # In this case we know for sure what the outcome will be,
                # no need for predictions.
                pi[idx] = child.r
            else:
                pi[idx] = np.dot(child.p, child.mu_hat)
        if player == 0:
            j = np.argmax(pi)
        elif player == 1:
            j = np.argmin(pi)
        else:
            raise ValueError("Invalid player")

        # Set p to zeroes, so children that are not yet added won't be selected.
        node.p = np.zeros(len(game.moves))
        for idx, pi_i in enumerate(pi):
            if idx == j:
                continue
            if player == 1:
                node.p[idx] = 1 / (self.nu + self.gamma * (pi[j] - pi_i))
            elif player == 0:
                node.p[idx] = 1 / (self.nu + self.gamma * (pi_i - pi[j]))
        node.p[j] = 1 + node.p[j] - np.sum(node.p)

    def _update_regression(self, node: CBTNode, score: float) -> None:
        """
        Update the regression parameters for the given node based on the score.
        """
        node.b += score * node.p
        mul_x = np.dot(node.A_inv, node.p)
        num = np.outer(mul_x, mul_x)
        denom = 1 + np.dot(node.p, mul_x)
        node.A_inv -= num / denom
        node.mu_hat = np.dot(node.b, node.A_inv)

class CBT2:
    """
    Implements the Contextual Bandits for Tree search (CBT)
    algorithm for maximizing outcomes in a game-like environment.
    """
    K: int
    nu: float
    gamma: float
    game: Game
    player: int
    exploration: float
    learning_rate: float

    def __init__(self, game: Game,
                 data_flag: bool = False,
                 print_flag: bool = False,
                 exploration: float = 10.0,
                 learning_rate: float = 1000.0) -> None:
        self.K: int = len(game.moves)
        self.moves = game.moves
        self.game = game
        self.print_data = data_flag
        self.print_flag = print_flag
        self.bandit = CBandit(nu=exploration, gamma=learning_rate)
        self.player = 0

    def run(self, iters: int = 1000) -> int:
        """
        Run the CBT algorithm for a specified number of iterations and return the best move.
        """

        root = CBTNode()
        self.bandit.initialize_node(root, self.game)

        for i in range(iters):
            v = self.select(root)

            if len(self.missing_moves(v)) > 0:
                v = self.expand(v)

            res = self.simulate()

            self.backpropagate(v, res)

            if self.print_data:
                print(f"{i} {res}")

            if self.print_flag:
                if i % 10000 == 0:
                    print(f"t={i}")

        # TODO: Think about what to return
        best_child = root.children[np.argmax(root.p)]
        # best_child = max(root.children, key=lambda child: child.n)

        return best_child.prev_move

    def select(self, v: CBTNode) -> CBTNode:
        """
        Traverse the tree to select a node for expansion.
        """
        while len(self.missing_moves(v)) == 0 and not self.game.finished:
            v = self.bandit.choose_arm(v)
            self.player = self.game.do(v.prev_move)

        return v

    def expand_root(self, root: CBTNode) -> CBTNode:
        """
        Expand the root node by adding all possible children.
        """
        moves: list[int] = list(self.missing_moves(root))
        for move in moves:
            child = root.add_child(move)
            self.player = self.game.do(move)
            self.bandit.initialize_node(child, self.game)
            self.player = self.game.undo()

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

        self.player = self.game.do(new_move)
        self.bandit.initialize_node(v,self.game)

        return v

    def backpropagate(self, v: CBTNode, score: int) -> None:
        """
        Update the statistics of all nodes along the path from the given node to the root.
        """
        node: CBTNode | None = v
        while node:
            bandit = self.bandit

            bandit.update_node(node, self.game, score, self.player)

            if node.parent is not None:
                self.player = self.game.undo()

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

class CBT2Player(Player):
    iterations: int
    exploration: float
    learning_rate: float

    def __init__(self, location, data_flag = False, print_flag = False):
        super().__init__(location, data_flag=data_flag, print_flag=print_flag)
        self.iterations = 1000
        self.exploration = 10.0
        self.learning_rate = 1000.0

    def make_move(self, game: Game) -> int:
        alg = CBT2(
            game,
            self.data_flag,
            self.print_flag,
            self.exploration,
            self.learning_rate
        )

        move = alg.run(self.iterations)
        return move


    def set_parameters(self, exploration: float, learning_rate: float) -> None:
        """
        Set the parameters for the bandit algorithm.
        """
        self.exploration = exploration
        self.learning_rate = learning_rate
