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
        return False 
    
    def isFlush(self):
        suits = {"H":[], "D":[], "S":[], "C":[]}

        for card in self.total_hand:
            suits[card.suit].append(card)
        
        for suit_cards in suits.values():
            if len(suit_cards) >= 5:
                highest_index = max(Card.ranks.index() for c in suit_cards) 
                return Card.ranks[highest_index]
            
        return False
    
    def isQuads(self):
        for i in range(len(self.total_hand)):
            for j in range(i+1,len(self.total_hand)):
                for k in range(j+1, len(self.total_hand)):
                    for l in range(k+1, len(self.total_hand)):
                        if self.total_hand[i] == self.total_hand[j] == self.total_hand[k] == self.total_hand[l]:
                            return self.total_hand[j].rank
        return False

    def isStraightFlush(self):
        if (self.isStraight() != False and self.isFlush() != False):
            suits = {"H":[], "D":[], "S":[], "C":[]}

            for card in self.total_hand:
                suits[card.suit].append(card)
            
            for suit_cards in suits.values():
                if len(suit_cards) >= 5:
                    suit_cards.sort()

                    indices = sorted(set(Card.ranks.index(c.rank) for c in suit_cards))

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
        return False
    
    def isRoyalFlush(self):
        if self.isStraightFlush() == "A":
            return "A"
        return False


    
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