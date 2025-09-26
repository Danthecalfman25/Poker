#player
from card import *
from deck import *
from table import *

class Player():
    def __init__(self, name, table):
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.hand = [] 
        self.table = table
        self.name = name
        self.chips = 0
        self.bet = 0
        self.total_hand = []
        self.final_hand = None


    def receiveCard(self, cards):
        for card in cards:
            self.hand.append(card)
            
    def display(self):
        print(f"{self.name}'s cards:")
        for card in self.hand:
            card.display()

    def displayChips(self):
        print(self.chips)

    def updateChips(self, change):
        self.chips += change
    
    def displayBet(self):
        print(self.bet)

    def updateBet(self, bet):
        self.bet += bet
        self.updateChips(-bet)
        self.table.updatePot(bet)


class humanPlayer(Player):
    pass

class aiPlayer(Player):
    pass