from __future__ import annotations
import collections
from collections.abc import Collection, Iterable
import copy
from operator import sub
import random
from algorithms.ISMCTS.determinization import Determinization, InformationSet
from algorithms.bandits.bandit import Bandit
from algorithms.bandits.UCB1 import UCB1
from games.klaverjas.definitions import Card, Suit, Trick
from games.klaverjas.gamestate import GameStateReader

# For programmability (is that a word?) this also include the hand of _this_ player.

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

    @classmethod
    def run(cls, 
            reader: GameStateReader,
            trick: Trick,
            starting_player: int,
            information_set: InformationSet,
            iter: int = 1000,
            pick_trump: bool = False,
            bandit: Bandit = UCB1) -> Card | Suit:
        root = cls.make_root(pick_trump)
        bandit.initialize_node(root)

        for i in range(iter):
            d0: Determinization = cls.determinize(reader, 
                                                  trick, 
                                                  starting_player, 
                                                  information_set)
            
            v, d = cls.select(root, d0, bandit)

            if len(v.missing_moves(d)) > 0:
                v, d = cls.expand(v, d, bandit)

            res = cls.simulate(v, d)
            cls.backpropagate(v,d,res,bandit)
            
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
               d: Determinization,
               bandit: Bandit) -> tuple[ISMCTSBaseNode, Determinization]:
        
        while not d.finished() and len(v.missing_moves(d)) == 0:
            next: ISMCTSNode = bandit.choose_arm(v,v.children(d),d)
            d.make_move(next.prev_move)
            v = next
        return v, d
    
    @classmethod
    def expand(cls, v: ISMCTSBaseNode,
               d: Determinization,
               bandit: Bandit) -> tuple[ISMCTSNode, Determinization]:
        moves: list[Card | Suit] = list(v.missing_moves(d))

        new_move = random.choice(moves)
        d.make_move(new_move)
        v = v.add_child(new_move)
        bandit.initialize_node(v)
        return v, d
    
    # Update visitations and scores in the entire tree
    @classmethod
    def backpropagate(cls, v: ISMCTSBaseNode, 
                      d: Determinization, score: list[int], 
                      bandit: Bandit) -> None:
        node: ISMCTSBaseNode | None = v
        while node:
            def reward(score: list[int]) -> int:
                return (score[0] - score[1]) * pow(-1, d.current_player) # Switch these around 
                # because the score in this node is the one received by the 
                # player that created it, which is the one associated with a 
                # node one level higher.
            bandit.update_node(node, node.children(d), reward(score))
            node.n += 1
            node.r = [node.r[0] + score[0], node.r[1] + score[1]]

            # Here n' is incremented for all children, it should be 
            # siblings according to Cowling et al. (2012).
            # TODO: Check that that makes a difference
            for child in node.children(d):
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