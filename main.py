from deck import *
from card import *
from player import *

def main():
    #deal 2 card to each player
    player = Player()
    computer = Player()
    deck = Deck()
    table = Table()

    deck.display()
    deck.shuffle()
    deck.display()
    