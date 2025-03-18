from math import log, sqrt
from typing import Final
from algorithms.ISMCTS.determinization import Determinization
from algorithms.bandits import bandit


class UCB1(bandit.Bandit):
    k: Final[float] = 0.75 # (From Cowling et al. (2012))
    
    @classmethod
    def score(cls, d: Determinization, child: bandit.Node) -> float:
        return child.reward(d)/child.n+cls.k*sqrt(log(child.n_accent)/child.n)
    
    @classmethod
    def choose_arm(cls, node: bandit.Node, *args) -> bandit.Node:
        d: Determinization = args[0]
        return max(node.children(d), key=lambda v: cls.score(d,v))