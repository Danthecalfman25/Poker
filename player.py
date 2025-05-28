from card import *
from deck import *
from table import *

class Player():
    def __init__(self):
        self.hand = [] 
        self.table = Table()

    def receive(self, card):
        self.hand.append(card)

    def ispair(self):
        if (self.hand[0].rank == self.hand[1].rank):
            return True
        for card in self.hand:
            for com in self.table.community:
                if card.rank == com.rank:
                    return True
        return False
    
    def displayHand(self):
        for card in self.hand:
            card.display()

