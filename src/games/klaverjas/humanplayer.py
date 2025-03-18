from games.klaverjas.definitions import Card, Suit, Trick
from games.klaverjas.gamestate import GameStateReader
from games.klaverjas.klaverjasplayer import KlaverjasPlayer


class HumanPlayer(KlaverjasPlayer):
    def _choose_move(self, state_reader: GameStateReader, trick: Trick) -> Card:

        if len(state_reader.tricks) > 0:
            print("De vorige slag was:")
            self.print_trick(state_reader.tricks[-1])
        
        print("Troef is ", state_reader.trump)

        print("De huidige slag is tot nu toe:")
        self.print_trick(trick)

        self.print_hand()
        while True:
            card_input = input("Kies een kaart om te spelen "
                          f"(0-{len(self.get_hand())-1}): ")
            if (not card_input.isdigit() 
                or int(card_input) >= len(self.get_hand()) 
                or int(card_input) < 0):
                
                print("Dat is niet een geldige keuze... Probeer het opnieuw.")
                continue

            card: Card = self.get_hand()[int(card_input)]
            if not self.isLegal(state_reader, trick, card):
                print("Die kaart is niet toegestaan, speel een andere.")
                continue
            
            return card
        
    def _get_cards(self) -> None:
        pass
    
    def pick_trump(self, _: GameStateReader) -> Suit:
        print()
        self.print_hand()
        print()

        while True:
            troef = input("Welke kleur wil je kiezen voor troef? "
                          "(0: ♣, 1: ♥, 2: ♠ of 3: ♦): ")
            if troef.isdigit() and int(troef) < 4 and int(troef) >= 0:
                return Suit(int(troef))
            
            print("Dat is niet een geldige keuze... Probeer het opnieuw.")
    
    def print_hand(self) -> None:
        self.sort_hand()
        print("Je hebt de volgende kaarten in je hand:")
        print(', '.join([str(i) + ": " + str(card) for i, card in enumerate(self.get_hand())]))

    def print_trick(self, trick: Trick) -> None:
        if len(trick) < 4:
            point_str = [""] * (4-len(trick)) + [str(card) for card in trick]
        else:
            point_str = [str(card) for card in Trick.rotate(trick, -self.loc)]

        print(("Speler "+str((self.loc+2)%4+1)+":").center(60))
        print(str(point_str[2]).center(60))
        print(f"Speler {(self.loc+1)%4+1}:".center(30),f"Speler {(self.loc+3)%4+1}:".center(30))
        print(str(point_str[1]).center(30),str(point_str[3]).center(30))
        print(f"Speler {(self.loc)%4+1} (jij):".center(60))
        print(str(point_str[0]).center(60))

        print()