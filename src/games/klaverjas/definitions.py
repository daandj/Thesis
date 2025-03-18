from __future__ import annotations
import copy
from enum import IntEnum
import warnings

class Suit(IntEnum):
    CLUBS = 0
    HEARTS = 1
    SPADES = 2
    DIAMONDS = 3

    def __str__(self):
        return ["♣","♥","♠","♦"][self.value]
    
    @classmethod
    def list(cls) -> list[Suit]:
        return list(cls)

class Value(IntEnum):
    SEVEN = 0
    EIGHT = 1
    NINE = 2
    JACK = 3
    QUEEN = 4
    KING = 5
    TEN = 6
    ACE = 7

    @classmethod
    def order_trump(self):
        return [self.SEVEN, self.EIGHT, self.QUEEN, self.KING, self.TEN, self.ACE, self.NINE, self.JACK]

    def __str__(self):
        return ["7", "8", "9", "J", "Q", "K", "10", "A"][self.value]


class Card:
    # The values of a card object should be immutable, once created an
    # instance represents just that card (this is also assumed to be true
    # whit cheating preventing measures).
    __suit: Suit
    __value: Value

    def __init__(self, suit: Suit, value: Value):
        self.__suit = suit
        self.__value = value

    @classmethod
    def from_number(cls, number: int):
        return cls(Suit(number // 8), Value(number % 8))

    def __str__(self):
        return str(self.__suit) + str(self.__value)
    
    def __hash__(self):
        return hash((self.__suit, self.__value))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        
        return (self.__suit == other.suit 
                and self.__value == other.value)
    
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    @property
    def number(self) -> int:
        return 8*self.__suit.value+self.__value.value
    
    @property
    def suit(self) -> Suit:
        return self.__suit
    
    @property
    def value(self) -> Value:
        return self.__value
    
    @property
    def order(self) -> int:
        return [
            Value.SEVEN,
            Value.EIGHT,
            Value.NINE,
            Value.TEN,
            Value.JACK,
            Value.QUEEN,
            Value.KING,
            Value.ACE
        ].index(self.value)

class Trick:
    __cards: list[Card]
    __starting_player: int

    def __init__(self, *cards: Card):
        if len(cards) > 4:
            raise ValueError("A trick can't have more than four played cards.")
        
        self.__cards = list(cards)
        self.__starting_player = 0
    
    def __len__(self) -> int:
        return len(self.__cards)
    
    def __getitem__(self, idx: int) -> Card:
        return copy.copy(self.__cards[idx])
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        
        return self.__cards == other.__cards and self.__starting_player == other.__starting_player

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    def __str__(self) -> str:
        return ', '.join([str(i+1) + ": " + str(card) for i, card in enumerate(self.__cards)])
    
    def __iter__(self):
        return iter(self.__cards)
    
    def play(self, new_card: Card) -> None:
        if len(self.__cards) >= 4:
            raise ValueError('A trick may only contain 4 cards')
        
        self.__cards.append(new_card)

    def undo(self) -> Card:
        if len(self.__cards) == 0:
            raise ValueError('Cannot undo a move from empty trick')
        
        return self.__cards.pop()
    
    def index(self, card: Card) -> int:
        return self.__cards.index(card)
    
    @property
    def starting_player(self) -> int:
        return self.__starting_player

    @classmethod
    def rotate(cls, trick: Trick, times: int) -> Trick:
        if len(trick) != 4:
            warnings.warn("Rotating a non-full trick may lead to"
                          " weird results...", RuntimeWarning)
        cards: list[Card] = trick.__cards + [None] * (4-len(trick.__cards)) # type: ignore
        #(this list should in practice never have a None)
        #TODO: Remove the previous line
        ret = Trick(*(cards[-times:]+cards[:-times]))
        ret.__starting_player = (ret.starting_player + times) % 4
        return ret