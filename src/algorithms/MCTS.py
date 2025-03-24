from __future__ import annotations
from collections.abc import Collection
import copy
from math import log, sqrt
import random
from typing import Final, Protocol

class Board(Protocol):
    prev_player: int 
    @property
    def finished(self) -> bool:
        pass
    
    @property
    def moves(self) -> list[int]:
        pass

    @property
    def points(self) -> int:
        pass

    def update(self, place: int) -> bool:
        pass

    def undo(self, place: int) -> None:
        pass
    
class MCTSNode:
    n: int
    parent: MCTSNode | None
    children: list[MCTSNode]
    prev_move: int
    n_accent: int
    r: int
    depth: int

    def __init__(self, parent: MCTSNode | None = None):
        self.parent = parent
        self.n_accent = 0
        self.n = 0
        self.children = list()
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

    def reward(self, b: Board) -> int:
        if b.prev_player == 0:
            return self.r
        else:
            return self.r
        

class MCTS:

    @classmethod
    def run(cls,
            board: Board,
            levels: int = 2,
            iter: int = 1000) -> int:
        
        root = MCTSNode()
        
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
        
        depth = 0

        while not b.finished and len(cls.missing_moves(v, b)) == 0 and depth < levels:
            next: MCTSNode = max(v.children, key=lambda v: UCB1(v,b))
            depth += 1
            v = next
            b.update(next.prev_move)
        return v
    
    @classmethod
    def expand(cls, v: MCTSNode, b: Board) -> MCTSNode:
        moves: list[int] = list(cls.missing_moves(v,b))

        new_move = random.choice(moves)
        v = v.add_child(new_move)

        b.update(v.prev_move)
        return v
    
    # Update visitations and scores in the entire tree
    @classmethod
    def backpropagate(cls, v: MCTSNode, b: Board, score: int) -> None:
        node: MCTSNode | None = v
        while node:
            node.n += 1
            node.r = node.r + score

            # Here n' is incremented for all children, it should be 
            # siblings according to Cowling et al. (2012).
            # TODO: Check that that makes a difference
            for child in node.children:
                child.n_accent += 1

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
