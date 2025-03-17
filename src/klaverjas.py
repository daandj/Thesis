from __future__ import annotations
import copy
from enum import IntEnum
from functools import reduce
from operator import add
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

class GameState:
    trump_card: Suit
    tricks: list[Trick]
    points: list[int]
    rounds_won: list[int]
    roem: list[int]

    def __init__(self):
        self.tricks = []
        self.trump_card = None
        self.points = [0,0]
        self.rounds_won = [0,0]
        self.roem = [0,0]

    def update(self, trick: Trick) -> None:
        self.tricks.append(trick)

        if len(self.tricks) == 8:
            self.score()

    def winner(self, trick: Trick) -> int:
        trump = self.trump_card
        begin_suit = trick[trick.starting_player].suit

        def keyTrump(card: Card) -> int:
            return Value.order_trump().index(card.value)
        
        if len(trick) != 4:
            raise RuntimeError("An unfinished trick can not have a winner.")
        
        trumps_played = list(filter(lambda card: trump == card.suit, trick))
        if trumps_played:
            highest_trump_played = max(trumps_played, key=keyTrump)
            return trick.index(highest_trump_played)
        
        begin_played = list(filter(lambda card: begin_suit == card.suit, trick))
        highest_played = max(begin_played, key=lambda card: int(card.value))
        return trick.index(highest_played)
    
    def score(self) -> None:
        for idx, trick in enumerate(self.tricks):
            winners = self.winner(trick) % 2
            self.points[winners] += self.__score_trick(trick)
            self.roem[winners] += self.__roem_trick(trick)
            self.rounds_won[winners] += 1

            # The winner of the last rounds gets 10 extra points
            if idx == 7:
                self.points[winners] += 10

            print(f"Intermediate stand: {winners=}, {self.points=}, {self.roem=}")

        # Check for 'nat', note that only the team of the first player can be 'nat'
        if self.points[0] + self.roem[0] <= self.points[1] + self.roem[1]:
            self.points = [0, 162]
            self.roem = [0, sum(self.roem)]

        # Check is a 'pit' is played
        if self.rounds_won[0] == 0:
            self.roem[1] += 100
        elif self.rounds_won[1] == 0:
            self.roem[0] += 100

    def __score_trick(self, trick: Trick) -> int:
        return reduce(add, map(lambda card: self.__score_card(card), trick))
    
    def __roem_trick(self, trick: Trick) -> int:
        roem = 0
        # Check for drie-/vierkaart:
        first_triplet = False
        second_triplet = False
        for suit in Suit:
            cards = sorted(filter(lambda card: card.suit == suit, trick),
                           key=lambda card: card.order)
            if len(cards) < 3:
                continue
            if (cards[1].order + 1 != cards[2].order):
                continue
            if (cards[0].order + 1 == cards[1].order):
                first_triplet = True
            if (len(cards) == 4 and cards[2].order + 1 == cards[3].order):
                second_triplet = True
        if (first_triplet and second_triplet):
            # Check for four in a row
            roem = 50
        elif first_triplet or second_triplet:
            # Check for three in a row
            roem = 20
        elif (trick[0].value in [Value.QUEEN, Value.KING, Value.ACE, Value.TEN]
            and trick[0].value == trick[1].value
            and trick[0].value == trick[2].value
            and trick[0].value == trick[3].value):
            # Check for four equal cards
            roem = 100
        elif (trick[0].value == Value.JACK
              and trick[1].value == Value.JACK
              and trick[2].value == Value.JACK
              and trick[3].value == Value.JACK):
            # Check for four jacks
            roem = 200

        # Check for 'stuk', trump queen + trump king (which can happen
        # at the same time as 'drie-/vierkaart')
        trump_king = Card(self.trump_card, Value.KING)
        trump_queen = Card(self.trump_card, Value.QUEEN)

        if trump_king in trick and trump_queen in trick:
            roem += 20

        return roem

    def __score_card(self, card: Card) -> int:
        if card.suit == self.trump_card:
            return [0, 0, 14, 20, 3, 4, 10, 11][int(card.value)]
        else:
            return [0, 0, 0, 2, 3, 4, 10, 11][int(card.value)]

class GameStateReader:
    __state: GameState

    def __init__(self, state: GameState):
        self.__state = state

    @property
    def trump(self) -> Suit:
        return self.__state.trump_card
    
    @property
    def tricks(self) -> list[Trick]:
        return copy.deepcopy(self.__state.tricks)