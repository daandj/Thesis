from abc import ABC, abstractmethod

from cbt.game import Game


class Player(ABC):
    loc: int

    def __init__(self, location: int, data_flag: bool = False):
        self.data_flag = data_flag
        self.loc = location

    @abstractmethod
    def make_move(self, game: Game) -> int:
        raise NotImplementedError()
