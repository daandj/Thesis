from ISMCTS import ISMCTS, InformationSet
from klaverjas import Card, GameStateReader, Suit, Trick
import player


class ISMCTSPlayer(player.Player):
    iset: InformationSet

    def _choose_move(self, reader: GameStateReader, trick: Trick) -> Card:
        # First we must update the available information set based on the cards
        # other players played in the previous and current trick.
        self.update_isets(reader, trick)

        self.sort_hand()
        card = ISMCTS.run(reader, trick, (self.loc-len(trick))%4, self.iset)
        self.iset[self.loc].remove(card)

        return card

    def pick_trump(self, reader: GameStateReader) -> Suit:
        trick = Trick()
        self.sort_hand()
        suit = ISMCTS.run(reader, trick, (self.loc-len(trick))%4, 
                          self.iset, pick_trump=True)
        return suit

    def _get_cards(self) -> None:
        result_list: list[set[Card]] = []
        for _ in range(4):
            result_list += [set([Card.from_number(i) for i in range(32)]) \
            - set(self.get_hand())]
        
        result_list[self.loc] = set(self.get_hand())

        self.iset = tuple(result_list)

    # This function takes 
    def update_iset(self,
                    trump: Suit,
                    trick: Trick,
                    card: Card,
                    player: int) -> None:
        tries = 5
        
        while card not in self.legal_moves(trump, trick, self.iset[player]):
            self.iset[player].difference_update(set(self.legal_moves(trump, trick, self.iset[player])))
            tries -= 1
            
            if tries == 0:
                raise Exception('Infinite loop')
            
        for i in range(4):
            self.iset[i].discard(card)

        self.iset[player].difference_update(set([card for card in trick]))

    def update_isets(self, reader: GameStateReader, trick: Trick):
        # If there was a previous trick, update the iset with all cards that
        # were played after ours.
        if len(reader.tricks) > 0:
            previous_trick = reader.tricks[-1]

            nr_new_moves = (previous_trick.starting_player-self.loc-1) % 4

            tmp_trick = Trick()
            for i in range(4-nr_new_moves):
                tmp_trick.play(
                    previous_trick[(previous_trick.starting_player+i)%4]
                )
            
            for i in range(nr_new_moves):
                player = (previous_trick.starting_player-nr_new_moves+i)%4
                self.update_iset(reader.trump,
                                 tmp_trick,
                                 previous_trick[player],
                                 player)
                tmp_trick.play(previous_trick[player])
        
        # Now update for the current trick.
        tmp_trick = Trick()
        starting_player = (self.loc - len(trick)) % 4
        for i in range(len(trick)):
            player = (starting_player+i)%4
            self.update_iset(reader.trump,
                             tmp_trick,
                             trick[i],
                             player
            )
            tmp_trick.play(trick[i])