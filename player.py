#player
from card import *
from deck import *
from table import *
from hand_detection import *

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
            
    def display_hand(self):
        print(f"{self.name}'s cards:")
        for card in self.hand:
            card.display()

    def displayChips(self):
        print(self.chips)

    def updateChips(self, change):
        self.chips += change
    
    





class humanPlayer(Player):
    def get_action(self):
        choice = input("1.Bet/Raise\n2.Call/Check\n3.Fold\n:")
        
        if (choice == "1"):
            self.displayChips()
            bet = int(input("Enter bet:"))
            return ("Bet", bet)
        if (choice == "2"):
            self.displayChips()
            return ("Call",)
        if (choice == "3"):
            return ("Fold",)

class aiPlayer(Player):
    def get_action(self):
        pass