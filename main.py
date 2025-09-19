from deck import *
from card import *
from player import *
from game import *
from table import *

def preflop(game, deck, table):
    #deal 2 card to each player
    game.resetPlayers()
    deck.shuffle()
    print("Dealing:\n")
    for player in game.active:
        player.receive(deck.deal(2))
        player.display()
        print("\n")
    game.smallBlind().updateBet(game.smallBlind)
    game.bigBlind().updateBet(game.bigBlind)
    table.update_currentBet(game.bigBlind)
    bettingRoundPreFlop(game, table)

def bettingRoundPreFlop(game, table):
    game.current_player_index = game.players[game.button + 3] % len(game.players)
    game.current_player = game.players[game.current_player_index]
    table.current_bet = game.bigBlind
    game.last_raiser = game.bigBlind
    while True:
        playerTurn(game, game.current_player, table)
        game.current_player_index = (game.current_player_index + 1) % len(game.active)
        game.check_endRound() 


def playerTurn(game, player, table):
    game.turns_taken += 1
    choice = input("1.Bet/Raise\n2.Call/Check\n3.Fold\n:")
    
    if (choice == "1"):
        player.displayChips()
        bet = int(input("Enter bet:"))
        player.updateBet(bet)
        table.update_currentBet(bet)
        player.displayBet()
        player.displayChips()
        table.displayPot()
        game.last_raiser = player
    if (choice == "2"):
        player.displayChips()
        bet = table.current_bet - player.bet
        player.updateBet(bet)
        player.displayBet()
        player.displayChips()
        table.displayPot()
    if (choice == "3"):
        game.folded(player)
    

        


        

        
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



main()