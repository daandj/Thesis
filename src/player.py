from abc import ABC, abstractmethod

from game import Game


class Player(ABC):
    loc: int

    def __init__(self, location: int):
        self.loc = location

    @abstractmethod
    def make_move(self, game: Game) -> int:
        raise NotImplementedError()
