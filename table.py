from card import *
from deck import *

class Table():
    def __init__(self):
        self.community =[]
    
    def receive(self, cards):
        for card in cards:
            self.community.append(card)
    
    def display(self):
        for card in self.community:
            card.display()