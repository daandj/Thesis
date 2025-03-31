from abc import ABC


class Player(ABC):
    loc: int

    def __init__(self, location: int):
        self.loc = location

    def make_move(self, *args):
        pass
