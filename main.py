from deck import *
from card import *
from player import *

def main():
    #deal 2 card to each player
    player = Player()
    computer = Player()
    deck = Deck()
    table = Table()

    print("Original Deck:")
    deck.display()
    print("\n")
    deck.shuffle()
    print("Sorted deck:")
    deck.display()
    print("\n")
    player.receive(deck.deal())
    player.receive(deck.deal())
    player.displayHand()
    print("\n")
    table.receive(deck.deal())
    table.receive(deck.deal())

main()