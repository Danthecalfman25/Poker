class Card():
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def displayCard(self):
        print(f"{self.rank}{self.suit}", end = " ")