#player
from card import *
from deck import *
from table import *

class Player():
    def __init__(self, name):
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.hand = [] 
        self.table = Table()
        self.name = name
        self.bet = 0
        self.total_hand = []

    def find_hand(self):
        self.total_hand = self.hand[:] + self.table.community[:]
        hand = self.isRoyalFlush()
        if hand: return hand
        hand = self.isStraightFlush()
        if hand: return hand
        hand = self.isQuads()
        if hand: return hand
        hand = self.isFullHouse()
        if hand: return hand
        hand = self.isFlush()
        if hand: return hand
        hand = self.isStraight()
        if hand: return hand
        hand = self.isTrips()
        if hand: return hand
        hand = self.isTwoPair()
        if hand: return hand
        hand = self.isPair()
        if hand: return hand
        return self.HighCard()


    def receive(self, cards, chips):
        for card in cards:
            self.hand.append(card)
            self.chips = chips

    def HighCard(self):
        self.total_hand.sort(reverse= True)
        return ("HighCard:", self.total_hand[0].rank)

    def isPair(self):
        high_pair = -1
        for i in range(len(self.total_hand)):
            for j in range(i+1,len(self.total_hand)):
                if self.total_hand[i] == self.total_hand[j]:
                    high_pair = max(self.ranks.index(self.total_hand[i].rank), high_pair)
        if high_pair != -1:
            return ("Pair", self.ranks[high_pair])
        return False
        
     
    def isTwoPair(self):
        pairs = []
        for i in range(len(self.total_hand)):
            for j in range(i+1,len(self.total_hand)):
                if self.total_hand[i] == self.total_hand[j]:
                    pairs.append(self.ranks.index(self.total_hand[i].rank))
        pairs = sorted(set(pairs), reverse=True)
        if len(pairs) >= 2:
            return ("Two Pair", self.ranks[pairs[0]], self.ranks[pairs[1]])
        return False
    
    def isTrips(self):
        high_card = -1
        for i in range(len(self.total_hand)):
            for j in range(i+1,len(self.total_hand)):
                for k in range(j+1, len(self.total_hand)):
                    if self.total_hand[i] == self.total_hand[j] == self.total_hand[k]:
                        high_card = max(high_card, self.ranks.index(self.total_hand[i].rank))
        if high_card != -1:
            return ("Trips", self.ranks[high_card])
        return False
    
    def isStraight(self):
        self.total_hand.sort()

        indices = sorted(set(self.ranks.index(c.rank) for c in self.total_hand))

        if self.ranks.index("A") in indices:
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
            return ("Straight", self.ranks[best_high])  
        return False 
    
    def isFlush(self):
        suits = {"H":[], "D":[], "S":[], "C":[]}

        for card in self.total_hand:
            suits[card.suit].append(card)
        
        for suit_cards in suits.values():
            if len(suit_cards) >= 5:
                highest_index = max(self.ranks.index(c.rank) for c in suit_cards) 
                return ("Flush", self.ranks[highest_index])
            
        return False
    
    def isFullHouse(self):
        card_count = {}
        for card in self.total_hand:
            if card.rank in card_count:
                card_count[card.rank] += 1
            else: card_count[card.rank] = 1
        trips = []
        pair = []
        for rank, count in card_count.items():
            if count == 3:
                trips.append(self.ranks.index(rank))
            if count == 2:
                pair.append(rank)
        
        trips.sort()
        if ((trips and pair) or (len(trips) == 2)):
            return ("Full House", trips[-1])
    
    def isQuads(self):
        high_card = -1
        for i in range(len(self.total_hand)):
            for j in range(i+1,len(self.total_hand)):
                for k in range(j+1, len(self.total_hand)):
                    for l in range(k+1, len(self.total_hand)):
                        if self.total_hand[i] == self.total_hand[j] == self.total_hand[k] == self.total_hand[l]:
                            return ("Quads", self.total_hand[j].rank)
        return False

    def isStraightFlush(self):
        if (self.isStraight() != False and self.isFlush() != False):
            suits = {"H":[], "D":[], "S":[], "C":[]}

            for card in self.total_hand:
                suits[card.suit].append(card)
            
            for suit_cards in suits.values():
                if len(suit_cards) >= 5:
                    suit_cards.sort()

                    indices = sorted(set(self.ranks.index(c.rank) for c in suit_cards))

                    if self.ranks.index("A") in indices:
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
                        return ("StraightFlush", self.ranks[best_high])  
        return False
    
    def isRoyalFlush(self):
        sf = self.isStraightFlush()
        if sf and sf[1] == "A":
            return ("RoyalFlush", "A")

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


player = Player("Daniel")

player.hand = [
    Card("A", "H"), Card("K", "H"), Card("Q", "H"),
    Card("J", "H"), Card("10", "H"), Card("3", "S"), Card("2", "D")
]

hand = player.find_hand()
print(hand)
