from collections.abc import Iterable
import copy
from math import sqrt, log
import random
from typing import Final

import numpy as np
from algorithms.MCTS import Board, MCTSNode

class Bandit:
    def __init__(self, nu: int, gamma: float) -> None:
        self.nu = nu
        self.gamma = gamma
        self.rng = np.random.default_rng()

    def initialize_node(self, node: MCTSNode, b: Board) -> None:
        length = len(b.moves)
        node.p = np.ones(length)/length
        node.mu_hat = np.ones(length)/length

    def update_node(self, node: MCTSNode,
                    board: Board,
                    score: int) -> None:
        
        node.n += 1
        node.r = node.r + score

        # Here n' is incremented for all children, it should be 
        # siblings according to Cowling et al. (2012).
        # TODO: Check that that makes a difference
        for child in node.children:
            child.n_accent += 1

        # Calculate the new probility distribution over all actions
        if node.depth == 1 and node.children:
            idx, child = min(enumerate(node.children), key=lambda tup: self.UCB1(tup[1],board))
            node.p = np.zeros(len(board.moves))
            node.p[idx] = 1

            self.update_avgs(node, board)
        elif node.depth == 0:
            pi = np.zeros(len(board.moves))
            for idx, child in enumerate(node.children):
                pi[idx] = np.dot(child.p, child.mu_hat)

            j = np.argmax(pi)
            
            for idx, pi_i in enumerate(pi):
                if idx == j:
                    continue

                node.p[idx] = 1/(self.nu+self.gamma*(pi[j]-pi_i))
            node.p[j]=1+node.p[j]-np.sum(node.p)

    def choose_arm(self, v: MCTSNode,
                   b: Board) -> MCTSNode:
        # Sample from the distribution p, regardles of what kind of node.
        return self.rng.choice(v.children, p=v.p)

    def UCB1(self, v: MCTSNode, b: Board) -> float:
        k: Final[float] = 0.75
        return v.r/v.n+k*sqrt(log(v.n_accent)/v.n)
    
    def update_avgs(self, node: MCTSNode, board: Board) -> None:
        node.mu_hat = np.zeros(len(board.moves))
        for i, child in enumerate(node.children):
            node.mu_hat[i] = child.r/child.n


class CBT1:
    K: int
    levels: int
    nu: float
    gamma: float
    b: Board

    def __init__(self, board: Board,
                 levels: int = 2,
                 nu: float | None = None,
                 gamma: float | None = None):
        self.K: Final[int] = len(board.moves)
        self.levels = levels
        self.nu = nu
        self.gamma = gamma
        self.b = board

    def run(self, iter: int = 1000) -> int:

        if not self.nu:
            self.nu = self.K

        if not self.gamma:
            self.gamma = sqrt(
                2*self.K*iter/self.regression_regret(iter)
            )
        bandit = Bandit(self.nu, self.gamma)
        
        root = MCTSNode()
        bandit.initialize_node(root, self.b)
        
        for i in range(iter):
            v = self.select(bandit, root)

            if len(self.missing_moves(v)) > 0:
                v = self.expand(bandit, v)

            res = self.simulate()
            self.backpropagate(bandit, v, res)
            
        best_child = max(root.children, key=lambda child: child.n)
        return best_child.prev_move

    def select(self, bandit: Bandit, v: MCTSNode) -> MCTSNode:
        while not self.b.finished and \
            len(self.missing_moves(v)) == 0 and v.depth < self.levels:
            v = bandit.choose_arm(v, self.b)
            self.b.update(v.prev_move)

        return v
    
    def expand(self, bandit: Bandit, v: MCTSNode) -> MCTSNode:
        moves: list[int] = list(self.missing_moves(v))

        #TODO: Change this to adding all children at once.
        #UPDATE: This is hard, because those children aren't visited yet
        # which leads to a division by zero problem in de UCB1 calculation.
        # for move in moves:
        #     child = v.add_child(move)

        #     b.update(child.prev_move)
        #     Bandit.initialize_node(child,b)
        #     b.undo(child.prev_move)

        # v = random.choice(v.children)
        # b.update(v.prev_move)

        new_move = random.choice(moves)
        v = v.add_child(new_move)

        self.b.update(v.prev_move)
        bandit.initialize_node(v,self.b)

        return v
    
    # Update visitations and scores in the entire tree
    def backpropagate(self, bandit: Bandit, v: MCTSNode, score: int) -> None:
        node: MCTSNode | None = v
        while node:
            bandit.update_node(node, self.b, score)

            if (node.parent != None):
                self.b.undo(node.prev_move)

            node = node.parent
    
    # Simulate the rest of this determinization and return the end score.
    def simulate(self) -> int:
        board: Board = copy.deepcopy(self.b)
        while not board.finished:
            moves: list[int] = list(board.moves)
            next: int = random.choice(moves)
            board.update(next)
        
        score = board.points

        return score
    
    def missing_moves(self, v: MCTSNode) -> list[int]:
        res = set(self.b.moves).difference(map(lambda child: child.prev_move, v.children))
        return list(res)
    
    def regression_regret(self, t: int) -> float:
        return sqrt(t) # TODO: This, but correct.
