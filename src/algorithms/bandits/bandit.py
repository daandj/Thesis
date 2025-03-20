from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Protocol


class Node(Protocol):
    _children: Iterable[Node]

class Bandit(Protocol):
    
    @classmethod
    def initialize_node(cls, node: Node) -> None:
        pass

    @classmethod
    def update_node(cls, node: Node,
                    children: Iterable[Node],
                    score: int) -> None:
        pass

    @classmethod
    @abstractmethod
    def choose_arm(self, node: Node, 
                    children: Iterable[Node],
                    *args) -> Node:
        raise NotImplementedError()