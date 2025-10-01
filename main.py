from deck import *
from card import *
from player import *
from game import *
from table import *

        

        
def main():
    table = Table()
    game = Game(table)
    name = input("Enter name:")
    player = Player(name, table)
    deck = Deck()
    game.players.append(player)
    computer = Player("computer", table)
    game.players.append(computer)
    game.resetPlayers()
    game.smallBlind = 10
    game.bigBlind = 20
    for player in game.players:
        player.chips = 1000
    preflop(game, deck, table)
    flop(game, deck, table)
    turn(game, deck, table)
    river(game, deck, table)




main()
