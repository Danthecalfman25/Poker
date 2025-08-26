from card import *
from deck import *

class Table():
    def __init__(self):
        self.community =[]
        call_amount = 0
        pot = 0
        
    
    def receive(self, cards):
        for card in cards:
            self.community.append(card)
    
    def display(self):
        print(f"Community cards:")
        for card in self.community:
            card.display()

    def updatePot(self, bet):
        self.pot += bet

    def updateCall_amount(self, bet):
        self.call_amount += bet

    