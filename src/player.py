from abc import abstractmethod
from collections.abc import Iterable
import copy
import random
from typing import final
from games.klaverjas.gamestate import GameStateReader
from games.klaverjas.definitions import Suit, Trick, Card, Value

class Player:
    # The variable hand is made private so it can be guaranteed, without
    # knowing anything about the implementation of the child class, that
    # the move that is played is a valid one, and that the hand variable
    # is updated accordingly. The actual choice between cards is made in
    # a protected method which is implemented in the child class.
    __hand: list[Card] = []
    loc: int

    @final
    def __init__(self, location: int):
        self.loc = location

    @final
    def deal(self, hand: list[Card]):
        if len(hand) != 8:
            raise ValueError('Dealt hand does not have the correct number of cards')
        self.__hand = hand

        self._get_cards()

    def _get_cards(self) -> None:
        pass

    @final
    def make_move(self, state_reader: GameStateReader, trick: Trick) -> Trick:
        copy_trick = copy.copy(trick)
        card = self._choose_move(state_reader, copy_trick)

        if not card in self.__hand:
            raise Exception('Illegal move')
        elif not self.isLegal(state_reader, trick, card):
            raise Exception('Illegal move')
        
        self.__hand.remove(card)
        trick.play(card)
        return trick
    
    @final
    def get_hand(self) -> list[Card]:
        return copy.copy(self.__hand)
    
    @staticmethod
    @final
    def moves(trump: Suit,
              trick: Trick,
              hand: Iterable[Card]) -> list[Card]:
        def isTrump(card: Card) -> bool: 
            return trump == card.suit
        
        def keyTrump(card: Card) -> int:
            return Value.order_trump().index(card.value)
        
        # The first person can choose any card
        if len(trick) == 0:
            return list(copy.copy(hand))
        
        matches_first_card: list[Card] = list(filter(
            lambda card: card.suit == trick[0].suit, hand))
        # Check if the first card is not a trump card and ot can be matched by
        # the player
        if (not isTrump(trick[0]) and matches_first_card):
            return list(matches_first_card)
        
        # In all the remaining cases the player must play a (higher) trump card
        # if they have one. If they don't have one, any card may be played.
        trump_cards_in_hand = list(filter(isTrump, hand))
        if (not trump_cards_in_hand):
            return list(copy.deepcopy(hand))
        
        # If they do have a trump card, a higher one must be played if possible.

        # First find the highest trump card that hase been played so far.
        trumps_played = list(filter(isTrump, trick))
        if not trumps_played:
            return list(trump_cards_in_hand)
        
        highest_trump_played = max(trumps_played, key=keyTrump)

        # If the player holds a higher trump card, return a set of those,
        # else return them all
        higher_trumps_in_hand = list(filter(
            lambda card: keyTrump(card) > keyTrump(highest_trump_played),
            trump_cards_in_hand
        ))
        if higher_trumps_in_hand:
            return list(higher_trumps_in_hand)
        else:
            return list(trump_cards_in_hand)
    
    @final
    def legal_moves(self,
                    trump: Suit,
                    trick: Trick,
                    hand: Iterable[Card] | None = None) -> list[Card]:
        if not hand:
            hand = self.__hand
        return self.moves(trump, trick, hand)

    @abstractmethod
    def _choose_move(self, state_reader: GameStateReader, trick: Trick) -> Card:
        raise NotImplementedError()
    
    @abstractmethod
    def pick_trump(self, reader: GameStateReader) -> Suit:
        raise NotImplementedError()

    @final
    def isLegal(self, reader: GameStateReader, trick: Trick, card: Card) -> bool:
        return card in self.legal_moves(reader.trump, trick)
    
    @final
    def sort_hand(self) -> None:
        self.__hand.sort(key=lambda card: card.number)

class RandomPlayer(Player):
    def _choose_move(self, state_reader: GameStateReader, trick: Trick) -> Card:
        return random.choice(self.legal_moves(state_reader.trump, trick))
    
    def pick_trump(self, _: GameStateReader) -> Suit:
        return random.choice([Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, 
                              Suit.SPADES])