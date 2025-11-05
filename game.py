from deck import *
from card import *
from player import *
from table import *


class Game():
    def __init__(self, table):
        self.deck = Deck()
        self.judge = Hand_Detection()
        self.players = []
        self.active = []
        self.button = 0
        self.smallBlind_Bet = 0
        self.bigBlind_Bet = 0
        self.current_player_index = 0
        self.current_player = None
        self.last_raiser = None
        self.turns_taken = 0
        self.table = table
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.hand_rankings = [
    "High Card",
    "One Pair",
    "Two Pair",
    "Three of a Kind",
    "Straight",
    "Flush",
    "Full House",
    "Four of a Kind",
    "Straight Flush",
    "Royal Flush"
]
    
    def play_hand(self):
        self.resetPlayers()
        self.resetGame()
        self.resetTable
        self.deck = Deck()
        self.deck.shuffle()
        self.postBlinds()

        self.preflop()
        if self.bettingRound("Preflop"):
            return
        self.flop()
        if self.bettingRound("Flop"):
            return
        self.turn()
        if self.bettingRound("Turn"):
            return
        self.river()
        if self.bettingRound("River"):
            return
        self.showdown()
        self.end_game()

    def postBlinds(self):
        sb = self.smallBlind()
        sbet = min (sb.chips, self.smallBlind_Bet)
        sb.updateChips(-sbet)
        self.table.updatePot(sbet)
        sb.bet_in_round = sbet
        self.isAllIn(sb)
        
        
        
        bb = self.bigBlind()
        bbet = min (bb.chips, self.bigBlind_Bet)
        bb.updateChips(-bbet)
        self.table.updatePot(bbet)
        bb.bet_in_round = bbet
        self.isAllIn(bb)

        self.table.current_bet = max(sbet, bbet)

    def isAllIn(self, player):
        if player.chips == 0:
            player.all_in = True
    
    def resetPlayers(self):
        for player in self.players:
            if player.chips == 0:
                self.players.remove(player)
        self.active = self.players[:]
    
    def resetGame(self):
        self.current_player_index = 0
        self.current_player = None
        self.last_raiser = None
        self.turns_taken = 0
        self.incrementButton()

    def resetTable(self):
        self.table.community.clear()
        self.table.current_bet = 0
        self.table.pot = 0


    def preflop(self):
        #deal 2 card to each player
        print("Dealing:\n")
        for player in self.active:
            player.receive(self.deck.deal(2))
            player.display()
            print("\n")
        self.table.update_currentBet(self.bigBlind)


    def flop(self):
        if (len(self.active) == 1):
            self.end_game()
        self.endRound()
        self.table.receive(self.deck.deal(3))
        self.table.display()
        self.table.displayPot()

    def bettingRound(self, stage):
        if stage == "Preflop":
            self.current_player_index = self.UTG()
            self.last_raiser = self.bigBlind()
        else:
            self.current_player_index = self.smallBlind()
            self.last_raiser = self.active[self.button]
        while True:
            self.current_player = self.active[self.current_player_index]
            self.playerTurn(self.current_player)
            self.incrementTurn()
            if self.check_endRound():
                break

    def turn(self):
        if (len(self.active) == 1):
            self.end_game()
        self.endRound()
        self.table.receive(self.deck.deal(1))
        self.table.display()
        self.table.displayPot()


    def river(self):
        if (len(self.active) == 1):
            self.end_game()
        self.endRound()
        self.table.receive(self.deck.deal(1))
        self.table.display()
        self.table.displayPot()

    def showdown(self):
        judge = Hand_Detection()
        highest_hand = (-1,)
        winner = None
        for player in self.active:
            hand = judge.findHand(player.hand, self.table.community)
            player.final_hand = []
            player.final_hand.append(self.hand_rankings.index(hand[0]))
            for i in range(1, len(hand)):
                player.final_hand.append(self.ranks.index(hand[i]))
            player.final_hand = tuple(player.final_hand)
            if player.final_hand > highest_hand:
                highest_hand = player.final_hand
                winner = player
        return winner
        
    def playerTurn(self, player):
        if player.all_in == True:
            return
        self.turns_taken += 1
        valid_actions = []
        if self.table.current_bet > player.bet_in_round:

            valid_actions.append ("Fold")
            valid_actions.append("Call")
            if player.chips > (self.table.current_bet - player.bet_in_round):
                valid_actions.append("Raise")
        else:
            valid_actions.append("Check")

            if player.chips > 0:
                valid_actions.append("Bet")
        
        action = player.get_action(valid_actions)
        action_type = action[0]
                
        if (action_type == "Bet" or action_type == "Raise"):
            bet = action[1]
            player.updateChips(-bet)
            self.table.updatePot(bet)
            player.bet_in_round += bet

            self.table.current_bet = player.bet_in_round
            self.last_raiser = player
            player.updateChips(-bet)
            self.isAllIn(player)
            print(f"{player.name} bets/raises to {player.bet_in_round}")
            
        elif (action_type == "Call"):
            amount_to_call = self.table.current_bet - player.bet_in_round

            player.updateChips(-amount_to_call)
            self.table.updatePot(amount_to_call)
            player.bet_in_round += amount_to_call

            self.isAllIn(player)
            print(f"{player.name} calls {amount_to_call}")

        elif action_type == "Check":
            print(f"{player.name} checks.")

        elif action_type == "Fold":
            print(f"{player.name} checks.")

        elif action_type == "Fold":
            print(f"{player.name} folds.")
        self.folded(player)

    def incrementButton(self):
        self.button = ((self.button + 1 ) % len(self.players))
    
    def folded(self, other):
        self.active.remove(other)
        self.current_player_index += -1
    
    def UTG(self):
        return self.players[(self.button + 3) % len(self.players)]
    
    def bigBlind(self):
        return self.players[(self.button + 2) % len(self.players)]

    def smallBlind(self):
        return self.players[(self.button + 1) % len(self.players)]
    
    def check_endRound(self):
        if (self.current_player != self.last_raiser): 
            return False
        for player in self.active:
            if self.current_player.bet_in_round != player.bet_in_round:
                if player.all_in:
                    continue
                return False
        return True

    def endRound(self):
        self.last_raiser = None
        self.turns_taken = 0
        self.table.current_bet = 0
        for player in self.active:
            player.bet_in_round = 0
            player.all_in = False
        
 
    def incrementTurn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.active)

    def check_for_winner(self):
        if len(self.active) == 1:
            self.end_game()
        
    def end_game(self, winner):
        winnings = self.table.pot
        self.table.updatePot(-winnings)
        winner.updateChips(winnings)
        return True
