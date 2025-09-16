from deck import *
from card import *
from player import *
from game import *

def preflop(game, deck, table):
    #deal 2 card to each player
    deck.shuffle()
    print("Dealing:\n")
    for player in game.active:
        player.receive(deck.deal(2))
        player.display()
        print("\n")
    game.player[game.button + 1].updateBet(game.smallBlind)
    game.player[game.button + 2].updateBet(game.bigBlind)
    bettingRoundPreFlop(game, table)

def bettingRoundPreFlop(game, table):
    game.current_player = game.players[game.button + 3] % len(game.players)
    table.current_bet = game.bigBlind
    game.last_raiser = game.players[(game.button + 2) % len(game.players)]
    while True:
        if game.current_player == game.last_raiser:
            break
        playerTurn(game.current_player, table)



def playerTurn(game, player, table):
    
    choice = input("1.Bet/Raise\n2.Call/Check\n3.Fold\n:")
    
    if (choice == 1):
        player.displayChips()
        bet = input("Enter bet:")
        player.updateBet(bet)
        player.updateChips(-bet)
        player.displayBet()
        player.displayChips()
        table.updateCurrent_bet()
    if (choice == 2):
        player.displayChips()
        bet = table.current_bet() - player.bet
        player.updateBet(bet)
        player.updateChips(-bet)
        player.displayBet()
        player.displayChips()
    if (choice == 3):
        game.active.remove(player)
    

        


        

        
def main():
    game = Game()
    name = input("Enter name:")
    player = Player(name)
    game.players.append(player)
    computer = Player("computer")
    game.players.append(computer)
    game.active = game.players[:]
    deck = Deck()
    table = Table()
    preflop(game, deck, table)



main()