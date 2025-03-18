from __future__ import annotations
from collections.abc import Iterable
import copy
from functools import reduce
from operator import add
from typing import NewType
from games.klaverjas.definitions import Trick, Card, Suit, Value
from games.klaverjas.gamestate import GameStateReader
from games.klaverjas.klaverjasplayer import KlaverjasPlayer


InformationSet = NewType('InformationSet', tuple[set[Card], set[Card],
                                                 set[Card], set[Card]])

class Determinization:
    points: list[int]
    rounds_won: list[int]
    roem: list[int]
    tricks: list[Trick]
    curr_trick: Trick
    current_player: int
    trump: Suit | None
    hands: InformationSet

    def __init__(self, hands: InformationSet, current_player: int):
        self.points = [0,0]
        self.rounds_won = [0,0]
        self.roem = [0,0]
        self.tricks = []
        self.hands = hands
        self.current_player = current_player

    @staticmethod
    def from_reader(reader: GameStateReader,
                    hands: InformationSet,
                    current_player: int) -> Determinization:
        d = Determinization(hands, current_player)
        d.tricks = copy.deepcopy(reader.tricks)
        d.trump = reader.trump

        return d
    
    def finished(self) -> bool:
        return len(self.tricks) == 8
    
    def moves(self) -> Iterable[Card]:
        if self.trump == None:
            raise Exception("There is no trump assigned")
        
        return KlaverjasPlayer.moves(self.trump, self.curr_trick,
                                   self.hands[self.current_player])
    
    def pick_trump(self, move: Suit) -> None:
        if self.trump:
            raise RuntimeError("Cannot assign a trump for the second time")
        
        self.trump = move

    def play_card(self, move: Card) -> None:
        if self.trump == None:
            raise RuntimeError("Cannot play a card yet, a trump suit has to"
                               " be picked first.")
        
        self.hands[self.current_player].remove(move)
        self.curr_trick.play(move)
        self.current_player = (self.current_player + 1) % 4

        if len(self.curr_trick) == 4:
            self.tricks.append(Trick.rotate(self.curr_trick, self.current_player))
            self.current_player = self.winner(self.curr_trick)
            self.curr_trick = Trick()
    
    def make_move(self, move: Card | Suit) -> None:
        match move:
            case Card():
                self.play_card(move)
            case Suit():
                self.pick_trump(move)

    def undo_trump(self) -> None:
        if self.trump == None:
            raise RuntimeError("Cannot undo trump picking move if there "
                               "is no trump card picked yet")
        self.trump = None
    
    def undo_move(self, times: int = 1) -> None:
        for _ in range(times):
            if len(self.curr_trick) == 0 and len(self.tricks) == 0:
                self.undo_trump()
                continue
            elif len(self.curr_trick) == 0:
                del self.curr_trick
                prev_trick = self.tricks.pop()
                self.curr_trick = Trick.rotate(prev_trick,
                                            -prev_trick.starting_player)
                self.current_player = prev_trick.starting_player
            pop = self.curr_trick.undo()
            self.current_player = (self.current_player - 1) % 4
            self.hands[self.current_player].add(pop)

    def score(self) -> None:
        for idx, trick in enumerate(self.tricks):
            winners = self.winner(trick) % 2
            self.points[winners] += self.__score_trick(trick)
            self.roem[winners] += self.__roem_trick(trick)
            self.rounds_won[winners] += 1

            # The winner of the last rounds gets 10 extra points
            if idx == 7:
                self.points[winners] += 10

        # Check for 'nat', note that only the team of the first player can be 'nat'
        if self.points[0] + self.roem[0] <= self.points[1] + self.roem[1]:
            self.points = [0, 162]
            self.roem = [0, sum(self.roem)]

        # Check is a 'pit' is played
        if self.rounds_won[0] == 0:
            self.points[1] += 100
        elif self.rounds_won[1] == 0:
            self.points[0] += 100
        
    def winner(self, trick: Trick) -> int:
        trump = self.trump
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
    
    def __roem_trick(self, trick: Trick) -> int:
        if self.trump == None:
            raise Exception("Cannot assess roem without knowing trump")
        
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
        trump_king = Card(self.trump, Value.KING)
        trump_queen = Card(self.trump, Value.QUEEN)

        if trump_king in trick and trump_queen in trick:
            roem += 20

        return roem
    
    def __score_trick(self, trick: Trick) -> int:
        return reduce(add, map(lambda card: self.__score_card(card), trick))
    
    def __score_card(self, card: Card) -> int:
        if card.suit == self.trump:
            return [0, 0, 14, 20, 3, 4, 10, 11][int(card.value)]
        else:
            return [0, 0, 0, 2, 3, 4, 10, 11][int(card.value)]
