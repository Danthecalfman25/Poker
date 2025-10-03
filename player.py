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
        self.hand_detection = Hand_Detection(self)


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

    def find_hand(self):
        self.hand_detection.find_hand()


class humanPlayer(Player):
    def get_action(self):
        choice = input("1.Bet/Raise\n2.Call/Check\n3.Fold\n:")
        
        if (choice == "1"):
            self.displayChips()
            bet = int(input("Enter bet:"))
            self.updateBet(bet)
            self.displayBet()
            self.displayChips()
            return ("Bet", bet)
        if (choice == "2"):
            self.displayChips()
            self.updateBet(bet)
            self.displayBet()
            self.displayChips()
            return ("Call",)
        if (choice == "3"):
            return ("Fold",)

class aiPlayer(Player):
    def get_action(self):
        choice = input("1.Bet/Raise\n2.Call/Check\n3.Fold\n:")
        
        if (choice == "1"):
            self.displayChips()
            bet = int(input("Enter bet:"))
            self.updateBet(bet)
            self.displayBet()
            self.displayChips()
        if (choice == "2"):
            self.displayChips()
            self.updateBet(bet)
            self.displayBet()
            self.displayChips()
        if (choice == "3"):
            self.folded(player)