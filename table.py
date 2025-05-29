from card import *
from deck import *

class Table():
    def __init__(self):
        self.community =[]
        pot = 0
        player
    
    def receive(self, cards):
        for card in cards:
            self.community.append(card)
    
    def display(self):
        print(f"Community cards:")
        for card in self.community:
            card.display()

    def updatePot(self, bet):
        self.pot += bet
    
    def