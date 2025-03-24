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

    @classmethod
    def run(cls,
            board: Board,
            levels: int = 2,
            iter: int = 1000,
            nu: int | None = None,
            gamma: int | None = None) -> int:

        K: Final[int] = len(board.moves)
        
        if not nu:
            nu = K

        if not gamma:
            gamma = sqrt(2*K*iter/cls.regression_regret(iter))
        bandit = Bandit(nu, gamma)
        
        root = MCTSNode()
        bandit.initialize_node(root, board)
        
        for i in range(iter):
            v = cls.select(bandit, root, board, levels)

            if len(cls.missing_moves(v, board)) > 0:
                v = cls.expand(bandit, v, board)

            res = cls.simulate(v, board)
            cls.backpropagate(bandit, v, board, res)
            
        best_child = max(root.children, key=lambda child: child.n)
        return best_child.prev_move

    @classmethod
    def select(cls, bandit: Bandit, v: MCTSNode, b: Board, levels: int) -> MCTSNode:
        while not b.finished and len(cls.missing_moves(v, b)) == 0 and v.depth < levels:
            v = bandit.choose_arm(v, b)
            b.update(v.prev_move)

        return v
    
    @classmethod
    def expand(cls, bandit: Bandit, v: MCTSNode, b: Board) -> MCTSNode:
        moves: list[int] = list(cls.missing_moves(v,b))

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

        b.update(v.prev_move)
        bandit.initialize_node(v,b)

        return v
    
    # Update visitations and scores in the entire tree
    @classmethod
    def backpropagate(cls, bandit: Bandit, v: MCTSNode, b: Board, score: int) -> None:
        node: MCTSNode | None = v
        while node:
            bandit.update_node(node, b, score)

            if (node.parent != None):
                b.undo(node.prev_move)

            node = node.parent
    
    # Simulate the rest of this determinization and return the end score.
    @classmethod
    def simulate(cls, v: MCTSNode, b: Board) -> int:
        board: Board = copy.deepcopy(b)
        while not board.finished:
            moves: list[int] = list(board.moves)
            next: int = random.choice(moves)
            board.update(next)
        
        score = board.points

        return score
    
    @classmethod
    def missing_moves(cls, v: MCTSNode, b: Board) -> list[int]:
        res = set(b.moves).difference(map(lambda child: child.prev_move, v.children))
        return list(res)
    
    @classmethod
    def regression_regret(cls, t: int):
        return sqrt(t) # TODO: This, but correct.
