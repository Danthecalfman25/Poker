from deck import *
from card import *
from player import *
from game import *
from table import *

def preflop(game, deck, table):
    #deal 2 card to each player
    deck.shuffle()
    print("Dealing:\n")
    for player in game.active:
        player.receive(deck.deal(2))
        player.display()
        print("\n")
    game.players[(game.button + 1) % len(game.players)].updateBet(game.smallBlind) 
    game.players[(game.button + 2) % len(game.players)].updateBet(game.bigBlind)
    table.updatePot(game.smallBlind + game.bigBlind)
    bettingRoundPreFlop(game, table)

def bettingRoundPreFlop(game, table):
    game.current_player_index = game.player[game.button + 3] % len(game.players)
    game.current_player = game.players[game.current_player_index]
    table.current_bet = game.bigBlind
    game.last_raiser = game.players[(game.button + 2) % len(game.players)]
    while True:
        game.current_player = game.active[game.current_player_index % len(game.active)]
        if (game.current_player == game.last_raiser) and (game.blind_turn > 0):
            break
        if (game.current_player == game.players[game.button + 2]):
            game.blind_turn += 1
        playerTurn(game, game.current_player, table)
        game.current_player_index = (game.current_player_index + 1) % len(game.players) 


def playerTurn(game, player, table):
    
    choice = input("1.Bet/Raise\n2.Call/Check\n3.Fold\n:")
    
    if (choice == "1"):
        player.displayChips()
        bet = int(input("Enter bet:"))
        player.updateBet(bet)
        player.updateChips(-bet)
        player.displayBet()
        player.displayChips()
        table.current_bet = player.bet
        table.updatePot(bet)
        table.displayPot()
        game.last_raiser = player
    if (choice == "2"):
        player.displayChips()
        bet = table.current_bet - player.bet
        player.updateBet(bet)
        player.updateChips(-bet)
        player.displayBet()
        player.displayChips()
        table.updatePot(bet)
        table.displayPot()
    if (choice == "3"):
        game.folded(player)
    

        


        

        
def main():
    game = Game()
    name = input("Enter name:")
    player = Player(name)
    game.players.append(player)
    computer = Player("computer")
    game.players.append(computer)
    game.resetPlayers()
    deck = Deck()
    table = Table()
    game.smallBlind = 10
    game.bigBlind = 20
    for player in game.players:
        player.chips = 1000
    preflop(game, deck, table)



main()