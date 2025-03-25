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
    def points(self) -> float:
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
    r: float
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

    def reward(self, b: Board) -> float:
        if b.prev_player == 0:
            return self.r
        else:
            return -self.r
        

class MCTS:
    levels: int
    b: Board

    def __init__(self, board: Board,
                 levels: int = 2):
        self.levels = levels
        self.b = board

    def run(self, iter: int = 1000) -> int:
        
        root = MCTSNode()
        
        for i in range(iter):
            v = self.select(root)

            if len(self.missing_moves(v)) > 0:
                v = self.expand(v)

            res = self.simulate()
            self.backpropagate(v, res)
            
        best_child = max(root.children, key=lambda child: child.n)
        return best_child.prev_move

    def select(self, v: MCTSNode) -> MCTSNode:
        def UCB1(v: MCTSNode) -> float:
            k: Final[float] = 0.75
            return v.reward(self.b)/v.n+k*sqrt(log(v.n_accent)/v.n)
        
        depth = 0

        while not self.b.finished and len(self.missing_moves(v)) == 0 and depth < self.levels:
            next: MCTSNode = max(v.children, key=lambda v: UCB1(v))
            depth += 1
            v = next
            self.b.update(next.prev_move)
        return v
    
    def expand(self, v: MCTSNode) -> MCTSNode:
        moves: list[int] = list(self.missing_moves(v))

        new_move = random.choice(moves)
        v = v.add_child(new_move)

        self.b.update(v.prev_move)
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

            if (node.parent != None):
                self.b.undo(node.prev_move)

            node = node.parent

    
    # Simulate the rest of this determinization and return the end score.
    def simulate(self) -> float:
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