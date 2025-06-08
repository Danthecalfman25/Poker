from deck import *
from card import *
from player import *

def preflop(player1, player2, deck, table):
    #deal 2 card to each player
    deck.shuffle()
    print("Dealing:\n")
    player1.receive(deck.deal(2))
    player1.display()
    print("\n")
    player2.receive(deck.deal(2))
    player2.display()
    print("\n")
    #table.receive(deck.deal(3))
    #table.display()

def bettingRoundPreFlop(player):
    choice = input("1.Bet/Raise\n2.Call/Check\n3.Fold\n:")
    
    if (choice == 1):
        player.displayChips()
        bet = input("Enter bet:")
        player.updateBet(bet)
        player.updateChips(-bet)
        player.displayBet()
        player.displayChips()
        pass
    if (choice == 2):
        

        
def main():
    name = input("Enter name:")
    player = Player(name)
    computer = Player("computer")
    deck = Deck()
    table = Table()
    preflop(player, computer, deck, table)



main()