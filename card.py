class Card():
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def display(self):
        print(f"{self.rank}{self.suit}", end = " ")

    def __eq__(self, other):
        if isinstance(other, Card):
            if (self.rank == other.rank):
                return True
        elif isinstance(other, str):
            if (self.rank == other):
                return True
        return False
    
    
    def __add__(self, value):
        