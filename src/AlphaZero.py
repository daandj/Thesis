from math import log, sqrt
from typing import Callable, ClassVar, Final

import numpy as np
from ISMCTS import ISMCTS, ISMCTSNode, Determinization, InformationSet, TrumpNode, UCB1
from ISMCTSplayer import ISMCTSPlayer
from klaverjas import Card, GameStateReader, Suit, Trick
from neuralnetwork import NeuralNetwork

class AGZNode(ISMCTSNode):
    p: np.float

    def __init__(self, prob: np.float, parent = None, current_player = None):
        self.p = prob
        super().__init__(parent, current_player)

    def add_child(self, move, p):
        child = super().add_child(move)
        child.p = p
        return child
    
class AGZTrumpNode(TrumpNode):
    p: np.float

    def __init__(self):
        super().__init__()


def PUCT(d: Determinization, child: AGZNode) -> int:
    c: Final[float] = 0.75 # (uit het AlphaGo Zero paper)
    return child.reward(d)/child.n+c*child.p*sqrt(log(child.n_accent))/(1+child.n)

#TODO: Redo this entire class, but for AlphaGo Zero algorithm. Put the training
# (policy iteration) algorithm outside of the class, in a seperate 'main.py'.
class AGZPlayer(ISMCTSPlayer):
    iset: InformationSet

    # An AlphaGo Zero player must be given a NeuralNetwork, which is
    # initialized before. Save games is a flag for keeping track of
    # previous games for training.
    def __init__(self, location: int, 
                 nn: NeuralNetwork, 
                 save_games: bool = False):
        self.nn = nn
        self.save_game = save_games 

        super().__init__(location)

    def _choose_move(self, reader, trick):
        return super()._choose_move(reader, trick)
    
    def pick_trump(self, reader):
        return super().pick_trump(reader)

    def _get_cards(self) -> None:
        return super()._get_cards()
    
    # Return saves games for NN training in the policy iteration algorithm.
    def get_saved_games(self) -> object:
        #TODO: Work out some way of passing these previous games, that includes
        # what action were available and history(?). Maybe it just needs the 
        # input vector that was used and the actual output from self play?
        pass

# In essence the AlphaGo Zero algorithm works just like Monte Carlo tree
# search, so my version will work approximatly the same as ISMCTS. In
# any case, the code from the ISMCTS class can be reused. 
class AlphaGoZero(ISMCTS):
    bandit_method: ClassVar[Callable[[Determinization, ISMCTSNode], int]] = UCB1
    nnet: ClassVar[NeuralNetwork]

    @classmethod
    def run(cls, 
            reader: GameStateReader,
            trick: Trick,
            starting_player: int,
            information_set: InformationSet,
            nnet: NeuralNetwork,
            iter: int = 1000,
            pick_trump: bool = False) -> Card | Suit:
        cls.nnet = nnet
        root = cls.make_root(pick_trump, (starting_player+len(trick))%4)

        for _ in range(iter):
            d0: Determinization = cls.determinize(reader, 
                                                  trick, 
                                                  starting_player, 
                                                  information_set)
            
            v, d = cls.select(root, d0)

            if len(v.missing_moves(d)) > 0:
                v, d = cls.expand(v, d)

            res = cls.simulate(d)
            cls.backpropagate(v,d,res)
        
        # Het paper gebruikt hier 'exponentiated visit count', met een 
        # temperature parameter, dit kan nog, maar voor de vergelijking
        # misschien niet chill en dat moet ik dan later maar implementeren.
        best_child = max(root.all_children(), key=lambda child: child.n)
        return best_child.prev_move

    @classmethod
    def make_root(cls, 
                  pick_trump: bool = False,
                  curr_player: int = None) -> ISMCTSNode:
        if pick_trump:
            return AGZTrumpNode()
        else:
            return AGZNode(current_player=curr_player)
    
    @classmethod
    def select(cls, v, d):
        return super().select(v, d)

    # Apparently all the children are expanded at once in AGZ.
    @classmethod
    def expand(cls,
               node: AGZNode,
               d: Determinization) -> tuple[AGZNode, Determinization]:
        missing_moves: set[Card | Suit] = node.missing_moves(d)
        #TODO: The next line does not yet work for the first move.
        indices = list(map(lambda move: move.number, missing_moves))
        p, v = cls.nnet.predict()
        normaliser = np.sum(p[indices])
        p = p/normaliser
        for move in missing_moves:
            # Deze geeft de p mee van de eerste keer dat de knoop wordt 
            # bereikt, maar de waarde van de vector p is natuurlijk
            # afhankelijk van de determinisatie. Dus dit moet anders,
            # voor nu gebruik ik in ieder geval niet PUCT maar UCT, 
            # dan heb ik in ieder geval niet de waarde nodig.
            node.add_child(move, 0)
        return node, d
    
    # Update the neural network here.
    @classmethod
    def backpropagate(cls, v, d, score):
        return super().backpropagate(v, d, score)
    
    # Run the neural network to get a evaluation of the game state.
    @classmethod
    def simulate(cls, node, d):
        #TODO: The next line does not yet work for the first move.
        moves = [child.prev_move for child in node.children(d)]
        indices = list(map(lambda move: move.number, moves))
        p, v = cls.nnet.predict()
        normaliser = np.sum(p[indices])
        p = p/normaliser
        for child in node.children(d):
            child.p = p[child.prev_move.number]
        return v