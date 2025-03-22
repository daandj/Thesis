from collections.abc import Collection, Iterable
import copy
from math import sqrt, log
import random
from typing import ClassVar, Final

import numpy as np
from algorithms.MCTS import Board, MCTSNode

class Bandit:
    @classmethod
    def initialize_node(cls, node: MCTSNode, b: Board) -> None:
        length = len(b.moves)
        node.p = np.ones(length)/length
        node.mu_hat = np.ones(length)/length
        node.ucb = None
        pass

    @classmethod
    def update_node(cls, node: MCTSNode,
                    board: Board,
                    score: Iterable[int]) -> None:
        def UCB1(v: MCTSNode, b: Board) -> float:
            k: Final[float] = 0.75
            return v.reward(b)/v.n+k*sqrt(log(v.n_accent)/v.n)
        
        node.n += 1
        node.r = [node.r[0] + score[0], node.r[1] + score[1]]

        # Here n' is incremented for all children, it should be 
        # siblings according to Cowling et al. (2012).
        # TODO: Check that that makes a difference
        for child in node.children:
            child.n_accent += 1
        if node.depth == 1 and node.children:
            node.ucb = max(node.children, key=lambda v: UCB1(v,board))

    @classmethod
    def choose_arm(self, node: MCTSNode,
                   board: Board) -> MCTSNode:
        raise NotImplementedError()

class CBT1:

    rng: ClassVar[np.random.Generator] = np.random.default_rng()

    @classmethod
    def run(cls,
            board: Board,
            levels: int = 2,
            iter: int = 1500,
            nu: int | None = None,
            gamma: int | None = None) -> int:

        K: Final[int] = len(board.moves)
        
        if not nu:
            nu = K

        if not gamma:
            gamma = sqrt(2*K*iter/cls.regression_regret(iter))
        
        root = MCTSNode()
        Bandit.initialize_node(root, board)
        
        for i in range(iter):
            v = cls.select(root, board, levels)

            if len(cls.missing_moves(v, board)) > 0:
                v = cls.expand(v, board)

            res = cls.simulate(v, board)
            cls.backpropagate(v, board, res)
            
        best_child = max(root.children, key=lambda child: child.n)
        return best_child.prev_move

    @classmethod
    def select(cls, v: MCTSNode, b: Board, levels: int) -> MCTSNode:
        def UCB1(v: MCTSNode, b: Board) -> float:
            k: Final[float] = 0.75
            return v.reward(b)/v.n+k*sqrt(log(v.n_accent)/v.n)

        while not b.finished and len(cls.missing_moves(v, b)) == 0 and v.depth < levels:
            if v.depth == 0:
                next: MCTSNode = cls.rng.choice(v.children, p=v.p)
            elif v.depth == 1:
                next: MCTSNode = max(v.children, key=lambda v: UCB1(v,b))
                if next != v.ucb:
                    raise RuntimeError("Oh no...")
            else:
                raise RuntimeError("No algorithm for the third level")

            v = next
            b.update(next.prev_move)

        return v
    
    @classmethod
    def expand(cls, v: MCTSNode, b: Board) -> MCTSNode:
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

        return v
    
    # Update visitations and scores in the entire tree
    @classmethod
    def backpropagate(cls, v: MCTSNode, b: Board, score: list[int]) -> None:
        node: MCTSNode | None = v
        while node:
            Bandit.update_node(node, b, score)

            if (node.parent != None):
                b.undo(node.prev_move)

            node = node.parent

    
    # Simulate the rest of this determinization and return the end score.
    @classmethod
    def simulate(cls, v: MCTSNode, b: Board) -> list[int]:
        board: Board = copy.deepcopy(b)
        while not board.finished:
            moves: list[int] = list(board.moves)
            next: int = random.choice(moves)
            board.update(next)
        
        scores = board.points

        return scores 
    
    @classmethod
    def missing_moves(cls, v: MCTSNode, b: Board) -> list[int]:
        res = set(b.moves).difference(map(lambda child: child.prev_move, v.children))
        return list(res)
    
    @classmethod
    def regression_regret(cls, t: int):
        return sqrt(t) # TODO: This, but correct.
