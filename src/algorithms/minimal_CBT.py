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

import copy
from math import sqrt, log
import random
from typing import Final
import numpy as np
from algorithms.MCTS import Board, MCTSNode
from game import Game

class CBandit:
    """
    Implements a contextual bandit algorithm for decision-making in the CBT framework.
    """
    def __init__(self, nu: int = 10, gamma: float = 0.5) -> None:
        self.nu = nu
        self.gamma = gamma
        self.rng = np.random.default_rng()

    def initialize_node(self, node: MCTSNode, g: Game) -> None:
        """
        Initialize the given node with uniform probabilities, identity matrix, and zero vectors.
        """
        length = len(g.moves)
        node.p = np.ones(length) / length
        node.leaf = False

    def update_node(self, node: MCTSNode, game: Game, _: int) -> None:
        """
        Update the statistics of the given node and its children based on the score.
        """
        pi = np.zeros(len(game.moves))
        for idx, child in enumerate(node.children):
            if child.leaf:
                pi[idx] = child.r
            else:
                pi[idx] = np.dot(child.p, child.mu_hat)
        j = np.argmax(pi)
        for idx, pi_i in enumerate(pi):
            if idx == j:
                continue
            node.p[idx] = 1 / (self.nu + self.gamma * (pi[j] - pi_i))
        node.p[j] = 1 + node.p[j] - np.sum(node.p)

    def choose_arm(self, v: MCTSNode) -> MCTSNode:
        """
        Sample a child node (arm) based on the probability distribution p.
        """

        return self.rng.choice(v.children, p=v.p)

class UCBBandit:
    """
    Implements the UCB bandit algorithm for move selection in the CBT framework.
    """

    def __init__(self) -> None:
        self.rng = np.random.default_rng()

    def initialize_node(self, node: MCTSNode, game: Game) -> None:
        """
        Initialize the node with uniform probabilities.
        """
        if game.finished:
            node.leaf = True
        else:
            length = len(game.moves)
            node.p = np.ones(length) / length
            node.leaf = False
            node.b = np.zeros(length)
            node.A_inv = np.identity(length)
            node.mu_hat = np.ones(length) / length

    def update_node(self, node: MCTSNode, game: Game, score: int) -> None:
        """
        Update the statistics of the given node and its children based on the score.
        """
        self._update_node_statistics(node, score)

        if not node.leaf:
            self._update_children_statistics(node)

        if node.children:
            self._update_depth_one_node(node, game, score)

    def choose_arm(self, v: MCTSNode) -> MCTSNode:
        """
        Sample a child node (arm) based on the probability distribution p.
        """
        return self.rng.choice(v.children, p=v.p)

    def UCB1(self, v: MCTSNode) -> float:
        """
        Calculate the UCB1 value for the given node.
        """
        k: Final[float] = 0.75
        return v.r / v.n + k * sqrt(log(v.n_accent) / v.n)

    def update_regression(self, node: MCTSNode, score: float) -> None:
        """
        Update the regression parameters for the given node based on the score.
        """
        node.b += score * node.p
        mul_x = np.dot(node.A_inv, node.p)
        num = np.outer(mul_x, mul_x)
        denom = 1 + np.dot(node.p, mul_x)
        node.A_inv -= num / denom
        node.mu_hat = np.dot(node.b, node.A_inv)

    # Helper methods
    def _update_node_statistics(self, node: MCTSNode, score: int) -> None:
        """
        Increment visit count and update the reward for the given node.
        """
        node.n += 1
        node.r += score

    def _update_children_statistics(self, node: MCTSNode) -> None:
        """
        Increment the n_accent value for all children of the given node.
        """
        for child in node.children:
            child.n_accent += 1

    def _update_depth_one_node(self, node: MCTSNode, game: Game, score: int) -> None:
        """
        Update the probabilities and regression for a depth-one node.
        """
        if node.leaf:
            return
        idx, _ = min(enumerate(node.children), key=lambda tup: self.UCB1(tup[1]))
        node.p = np.zeros(len(game.moves))
        node.p[idx] = 1
        self.update_regression(node, score)

class CBTMinimal:
    """
    Implements the Contextual Bandits for Tree search (CBT)
    algorithm for maximizing outcomes in a game-like environment.
    """
    K: int
    nu: float
    gamma: float
    game: Game

    def __init__(self, game: Game,
                 data_flag: bool = False) -> None:
        self.K: Final[int] = len(game.moves)
        self.moves = game.moves
        self.game = game
        self.print_data = data_flag
        self.cbandit = CBandit()
        self.ucb_bandit = UCBBandit()

    def run(self, iters: int = 10000) -> int:
        """
        Run the CBT algorithm for a specified number of iterations and return the best move.
        """
        self.cbandit.nu = self.K

        self.cbandit.gamma = sqrt(
            2*self.K*iters/self.regression_regret(iters)
        )

        root = MCTSNode()
        self.cbandit.initialize_node(root, self.game)

        # Create all children of the root node.
        self.expand_root(root)

        for i in range(iters):
            v = self.select(root)

            res = self.simulate()

            self.backpropagate(v, res)

            if self.print_data:
                print(f"Iteration {i}: {v.prev_move} -> {res}")
                # TODO: Add make this more comprehensive

        # TODO: Think about what to return
        best_child = max(root.children, key=lambda child: child.n)
        return best_child.prev_move

    def select(self, v: MCTSNode) -> MCTSNode:
        """
        Traverse the tree to select a node for expansion.
        """

        v = self.cbandit.choose_arm(v)
        self.game.do(v.prev_move)

        if len(self.missing_moves(v)) == 0:
            # If all children are visited, select the best child based on UCB1.
            v = self.ucb_bandit.choose_arm(v)
            self.game.do(v.prev_move)
        else:
            v = self.expand(v)

        return v

    def expand_root(self, root: MCTSNode) -> MCTSNode:
        """
        Expand the root node by adding all possible children.
        """
        moves: list[int] = list(self.missing_moves(root))
        for move in moves:
            child = root.add_child(move)
            self.game.do(move)
            self.ucb_bandit.initialize_node(child, self.game)
            self.game.undo()

        return root

    def expand(self, v: MCTSNode) -> MCTSNode:
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
        self.ucb_bandit.initialize_node(v,self.game)

        return v

    def backpropagate(self, v: MCTSNode, score: int) -> None:
        """
        Update the statistics of all nodes along the path from the given node to the root.
        """
        node: MCTSNode | None = v
        while node:
            if node.depth == 0:
                bandit = self.cbandit
            else:
                bandit = self.ucb_bandit

            bandit.update_node(node, self.game, score)

            if node.parent is not None:
                self.game.undo()

            node = node.parent

    def simulate(self) -> int:
        """
        Simulate the game from the current board state to the end and return the score.
        """
        if not self.game.finished:
            raise RuntimeError("I made a mistake")
        game: Board = copy.deepcopy(self.game)
        while not game.finished:
            moves: list[int] = list(game.moves)
            next_move: int = random.choice(moves)
            game.update(next_move)

        score = game.points

        return score

    def missing_moves(self, v: MCTSNode) -> list[int]:
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
