from collections.abc import Iterable
from math import log, sqrt
from typing import Final, Iterable
from algorithms.ISMCTS.determinization import Determinization
from algorithms.bandits import bandit


class UCB1(bandit.Bandit):
    k: Final[float] = 0.75 # (From Cowling et al. (2012))
    
    @classmethod
    def score(cls, d: Determinization, child: bandit.Node) -> float:
        print(f"Child.reward(d)={child.reward(d)}, here the d.current_player={d.current_player}")

        return child.reward(d)/child.n+cls.k*sqrt(log(child.n_accent)/child.n)
    
    @classmethod
    def new_score(cls, child: bandit.Node) -> float:
        print(f"Child.cumul_score={child.cumul_score}")
        return child.cumul_score/child.n_test+cls.k*sqrt(log(child.n_accent_test)/child.n_test)
    
    @classmethod
    def choose_arm(cls, node: bandit.Node,
                   children: Iterable[bandit.Node] = [],
                   *args) -> bandit.Node:
        d: Determinization = args[0]
        old = max(node.children(d), key=lambda v: cls.score(d,v))
        new = max(children, key=lambda v: cls.new_score(v))

        if (old.prev_move != new.prev_move):
            raise RuntimeError("uhoh")
        
        return new
    
    @classmethod
    def initialize_node(cls, node: bandit.Node) -> None:
        node.cumul_score = 0
        node.n_test = 0
        node.n_accent_test = 0
    
    @classmethod
    def update_node(cls, node: bandit.Node,
                    children: Iterable[bandit.Node],
                    score: int) -> None:
        node.cumul_score += score
        node.n_test += 1

        # Here n' is incremented for all children, it should be 
        # siblings according to Cowling et al. (2012).
        # TODO: Check that that makes a difference
        for child in children:
            child.n_accent_test += 1