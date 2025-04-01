from abc import ABC, abstractmethod

class Game(ABC):
    """
    Abstract class for a game.
    """
    # Public methods
    def __init__(self, print_flag: bool = False):
        self.print_flag = print_flag

    # Give everyone their random cards
    @abstractmethod
    def setup(self, *args) -> None:
        raise NotImplementedError()

    @abstractmethod
    def do(self, move: int) -> int:
        """
        Play the move on the board and return the next player.
        """
        raise NotImplementedError()

    def undo(self) -> int:
        """
        Undo the last move and return the player that made it.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def points(self) -> float:
        raise NotImplementedError()

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def num_players(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def finished(self) -> bool:
        raise NotImplementedError()

    @property
    @abstractmethod
    def winner(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the game state to its initial state.
        """
        raise NotImplementedError()
