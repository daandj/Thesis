from __future__ import annotations
import collections
from collections.abc import Collection, Iterable
import copy
from functools import reduce
from math import log, sqrt
from operator import add, sub
import random
from typing import Final, NewType
from klaverjas import Card, GameStateReader, Suit, Trick, Value
import player

# For programmability (is that a word?) this also include the hand of _this_ player.

InformationSet = NewType('InformationSet', tuple[set[Card], set[Card],
                                                 set[Card], set[Card]])

def UCB1(d: Determinization, child: ISMCTSNode) -> float:
    k: Final[float] = 0.75 # (uit het ISMCTS paper)
    return child.reward(d)/child.n+k*sqrt(log(child.n_accent)/child.n)

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
        
        return player.Player.moves(self.trump, self.curr_trick,
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

# Every node in the game of Klaverjas is essentially a card being
# played. Except for the first node, where the choice is what the 
# trump card is going to be. Furthermore it is a matter of what
# cards the player holds.
#
# In this characterization, a determinization is a choice for the
# cards in the hands of all other players.

class ISMCTSBaseNode: # Also used as root node, because is doesn't need most fields
    n: int
    n_accent: int
    _children: set[ISMCTSNode]
    r: list[int]
    
    def __init__(self):
        self.n = 0                              # Visit count
        self.n_accent = 0                       # Availability count 
        self.r = [0,0]                          # Total rewards
        self._children = set()                  # Child nodes

    def print(self) -> None:
        print(f"\tISMCTSNode {self} with values:")
        print(f"\tn={self.n}, n'={self.n_accent}, r={self.r}, ")
        print(f"\twith {len(self._children)} children, with the actions:")
        print("\t\t", ', '.join(map(lambda c: str(c.prev_move),self._children)))

    def children(self, d: Determinization) -> Iterable[ISMCTSNode]:
        return filter(lambda child: child.prev_move in set(d.moves()), self._children)
    
    def add_child(self, move: Card | Suit) -> ISMCTSNode:
        child: ISMCTSNode = ISMCTSNode(self, move)
        self._children.add(child)
        return child

    def missing_moves(self, d: Determinization) -> Collection[Card] | Collection[Suit]:
        res = set(d.moves()).difference(map(lambda child: child.prev_move, self._children))
        return res

    def reward(self, d: Determinization) -> int:
        return (self.r[d.current_player % 2]
                - self.r[(d.current_player + 1) % 2])
    
    def all_children(self) -> set[ISMCTSNode]:
        return self._children

class ISMCTSNode(ISMCTSBaseNode):
    parent: ISMCTSBaseNode
    prev_move: Card | Suit

    def __init__(self, parent: ISMCTSBaseNode, prev_move: Suit | Card):
        super().__init__()
        self.parent = parent                    # Parent node
        self.prev_move = prev_move

    def print(self) -> None:
        super().print()
        print(f"\tFurthermore, it has the parent {self.parent} ",
              f"and previous_move={self.prev_move}.")


class TrumpNode(ISMCTSBaseNode):
    def __init__(self):
        super().__init__()

    def missing_moves(self, d: Determinization) -> Collection[Suit]:
        res = set(Suit.list()).difference(map(lambda child: child.prev_move, self._children))
        return res

    def children(self, d: Determinization) -> set[ISMCTSNode]:
        # The first player is always allowed to pick any Suit to be the trump,
        # so we just return all children
        return self._children

class ISMCTS:
    bandit_method = UCB1

    @classmethod
    def run(cls, 
            reader: GameStateReader,
            trick: Trick,
            starting_player: int,
            information_set: InformationSet,
            iter: int = 1000,
            pick_trump: bool = False) -> Card | Suit:
        root = cls.make_root(pick_trump)

        for i in range(iter):
            print(f"iter = {i}")
            d0: Determinization = cls.determinize(reader, 
                                                  trick, 
                                                  starting_player, 
                                                  information_set)
            
            v, d = cls.select(root, d0)
            print(f'past select, v=')
            v.print()

            if len(v.missing_moves(d)) > 0:
                v, d = cls.expand(v, d)

            print(f'past expand, v=')
            v.print()
            res = cls.simulate(v, d)
            print(f'past simulate, v=')
            v.print()
            cls.backpropagate(v,d,res)
            print(f'past backpropagate, v=')
            v.print()
        
        best_child = max(root.all_children(), key=lambda child: child.n)
        return best_child.prev_move
    
    # This is a sort of factory method, that gives the right type of root node
    # for the right algorithm
    @classmethod
    def make_root(cls, 
                  pick_trump: bool = False
                  ) -> ISMCTSBaseNode:
        if pick_trump:
            return TrumpNode()
        else:
            return ISMCTSBaseNode()

    # This function creates a determinization i.e. a random set of hands for 
    # each player that could be possible with a certain information set.
    @classmethod
    def determinize(cls,
                    reader: GameStateReader,
                    trick: Trick, 
                    starting_player: int,
                    info_set: InformationSet) -> Determinization:
        # For each player calculate the amount of cards they should have in their hands
        played_cards = [len(reader.tricks)] * 4
       
        for i in range(len(trick)):
            played_cards[(starting_player+i)%4] += 1

        cards_left = list(map(sub, [8] * 4, played_cards))
        # Then pick the appropriate amount of cards form each information set
        # uniform randomly.

        hands: InformationSet = InformationSet((set(), set(), set(), set()))

        counter: collections.Counter[Card] = collections.Counter()
        for hand in info_set:
            counter.update(hand)

        if len(counter) != sum(cards_left):
            raise RuntimeError(f"Not enough cards to assign")

        # First assign the cards that can only go to one player
        while (counter.most_common()[-1][1] == 1):
            one_left = counter.most_common()[-1][0]
            idxs = [i for i in range(4) if one_left in info_set[i]]
            
            if len(idxs) != 1:
                raise Exception("There was a logic error in the code")
            
            hands[idxs[0]].add(one_left)
            del counter[one_left]
            if len(counter.most_common()) == 0:
                break

        unassigned_cards = set(counter.keys())
        
        # For the remaining cards assign them randomly, but only if it 
        # doesn't make filling the other hands impossible.
        while len(unassigned_cards) > 0:
            card = random.choice(list(unassigned_cards))

            # Check if it is _needed_ by more than one player
            needed_by = []
            possible_for = []
            for player in range(4):
                if (len(info_set[player] & unassigned_cards) 
                    < cards_left[player] - len(hands[player])):
                    needed_by += [player]

                if card in info_set[player] and len(hands[player]) < cards_left[player]:
                    possible_for += [player]

            if len(needed_by) > 1:
                raise RuntimeError("No determinization possible")
            elif len(needed_by) == 1:
                hands[needed_by[0]].add(card)
                unassigned_cards.remove(card)
            else:
                hands[random.choice(possible_for)].add(card)
                unassigned_cards.remove(card)

        d = Determinization.from_reader(reader, hands,
                                        (starting_player+len(trick))%4)
        d.curr_trick = copy.deepcopy(trick)
        return d

    @classmethod
    def select(cls, v: ISMCTSBaseNode, 
               d: Determinization) -> tuple[ISMCTSBaseNode, Determinization]:
        
        while not d.finished() and len(v.missing_moves(d)) == 0:
            next: ISMCTSNode = max(v.children(d), key=lambda v: cls.bandit_method(d,v))
            d.make_move(next.prev_move)
            v = next
        return v, d
    
    @classmethod
    def expand(cls, v: ISMCTSBaseNode, d: Determinization) -> tuple[ISMCTSNode, Determinization]:
        moves: list[Card | Suit] = list(v.missing_moves(d))

        new_move = random.choice(moves)
        d.make_move(new_move)
        v = v.add_child(new_move)
        return v, d
    
    # Update visitations and scores in the entire tree
    @classmethod
    def backpropagate(cls, v: ISMCTSBaseNode, d: Determinization, score: list[int]) -> None:
        node: ISMCTSBaseNode | None = v
        while node:
            node.n += 1
            node.r = [node.r[0] + score[0], node.r[1] + score[1]]

            # Here n' is incremented for all children, it should be 
            # siblings according to Cowling et al. (2012).
            # TODO: Check that that makes a difference
            for child in v.children(d):
                print(f"Updating n' in {child} in backpropagate")
                child.n_accent += 1
            
            if type(node) == ISMCTSNode:
                node = node.parent
            else:
                node = None

            if node:
                d.undo_move()

    
    # Simulate the rest of this determinization and return the end score.
    @classmethod
    def simulate(cls, v: ISMCTSBaseNode, d: Determinization) -> list[int]:
        counter: int = 0
        while not d.finished():
            moves: list[Card] = list(d.moves())
            next: Card = random.choice(moves)
            d.make_move(next)
            counter += 1
        
        d.score()
        scores = [d.points[0] + d.roem[0], d.points[1] + d.roem[1]]

        d.undo_move(counter)

        return scores 