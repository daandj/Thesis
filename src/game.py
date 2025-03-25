from abc import ABC, abstractmethod
from typing import final
from player import Player

class Game(ABC):
    players: tuple[Player, ...]

    # Public methods
    def __init__(self, *players: Player, print: bool = False):
        self.set_players(players)
        self.print = print

    # For pretty printing using the std library print function
    def __str__(self):
        pass
    
    @final
    def set_players(
            self, 
            players: tuple[Player, ...]
        ) -> None:
        if len(players) != self.num_players:
            raise ValueError(f'A game of {self.name} must have exactly {self.num_players} players')
        
        self.players = players

    @final
    def set_player(self, player: Player, position: int) -> None:
        if position < 0 or position > self.num_players:
            raise ValueError(f'Invalid place number for a player (must be between 0 and {self.num_players})')
        tmp_list = list(self.players)
        tmp_list[position] = player
        self.players = tuple(tmp_list)
    
    @final
    def play(self) -> int:
        starting_player = 0
        self.setup(starting_player)

        while not self.finished:
            starting_player = self.play_round(starting_player, self.print)

        return self.winner
        
    # Give everyone their random cards
    @abstractmethod
    def setup(self, *args) -> None:
        raise NotImplementedError()
    
    # Play one round of the game and then return the player whose turn it is next
    @abstractmethod
    def play_round(self, starting_player: int, print: bool = False) -> int:
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