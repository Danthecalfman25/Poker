from deck import *
from card import *
from player import *

def preflop(player1, player2, deck, table):
    print("Original Deck:")
    deck.display()
    print("\n")
    deck.shuffle()
    print("Sorted deck:")
    deck.display()
    print("\n")
    player1.receive(deck.deal(2))
    player1.display()
    print("\n")
    player2.receive(deck.deal(2))
    player2.display()
    print("\n")
    table.receive(deck.deal(3))
    table.display()

def main():
    #deal 2 card to each player
    player = Player()
    computer = Player()
    deck = Deck()
    table = Table()
    preflop(player, computer, deck, table)



main()