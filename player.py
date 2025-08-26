#player
from card import *
from deck import *
from table import *

class Player():
    def __init__(self, name):
        self.hand = [] 
        self.table = Table()
        self.name = name
        self.bet = 0
        self.total_hand = []

    def find_hand(self):
        for card in self.hand:
            self.total_hand.append(card)
        for card in self.table.community:
            self.total_hand.append(card)
        if isRoyal_Flush() == True:
            return "Royal Flush"
        if isStraight_Flush() != False:
            return isStraight_Flush()
        if isQuads() == True:
            return "Straight_Flush"
        if isFull_House() == True:
            return "Full House"
        if isFlush() == True:
            return "Flush"
        #find = isStraight()
        #find = isTrips()
        if isPair() == True:
            return "Pair"


    def receive(self, cards, chips):
        for card in cards:
            self.hand.append(card)
            self.chips = chips

    def ispair(self):
        for i in range(len(self.total_hand)):
            for j in range(i+1,len(self.total_hand)):
                if self.total_hand[i] == self.total_hand[j]:
                    return self.total_hand[i].rank
        return False
    
    def istrips(self):
        for i in range(len(self.total_hand)):
            for j in range(i+1,len(self.total_hand)):
                for k in range(j+1, len(self.total_hand)):
                    if self.total_hand[i] == self.total_hand[j] == self.total_hand[k]:
                        return self.total_hand[j].rank
        return False
    
    def isStraight():
        return
    
    def is
    
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