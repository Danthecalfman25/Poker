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
    
    def isStraight(self):
        self.total_hand.sort()

        indices = sorted(set(Card.ranks.index(c.rank) for c in self.total_hand))

        if Card.ranks.index("A") in indices:
            indices.insert(0, -1)

        count = 1
        best_high = None
        for i in range(1, len(indices)):
            if indices[i] == indices[i - 1] + 1:
                count += 1
                if count >= 5:
                    best_high = indices[i]  
            else:
                count = 1

        if best_high is not None:
            return Card.ranks[best_high]  
        return None 
    
    def isFlush(self):
        heart = 0
        club = 0
        spade = 0
        diamond = 0
        for card in self.total_hand:
            if card.suit == "H":
                heart += 1
            if card.suit == "D":
                diamond += 1
            if card.suit == "S":
                spade += 1
            if card.suit == "C":
                club += 1
        if heart >= 5:
            index = 0
            for card in self.total_hand:
                if card.suit == "H":
                    index = max(index, self.ranks.index(card.rank))




    
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