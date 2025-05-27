class Card():
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def display(self):
        print(f"{self.rank}{self.suit}", end = " ")