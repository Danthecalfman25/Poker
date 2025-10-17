from card import *
from deck import *

class Table():
    def __init__(self):
        self.community =[]
        self.current_bet = 0
        self.pot = 0
        
    
    def receive(self, cards):
        for card in cards:
            self.community.append(card)
    
    def display(self):
        print(f"Community cards:")
        for card in self.community:
            card.display()

    def updatePot(self, bet):
        self.pot += bet
    
    def displayPot(self):
        print("Pot: ", self.pot)

    def update_bet_in_round(self, bet):
        self.bet_in_round += bet

    