from self.deck import *
from card import *
from player import *
from table import *


class Game():
    def __init__(self, table):
        self.deck = Deck()
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
    
    def play(self, player1, player2):
        pass

    def preflop(self):
        #deal 2 card to each player
        self.resetPlayers()
        self.deck.shuffle()
        print("Dealing:\n")
        for player in self.active:
            player.receive(self.deck.deal(2))
            player.display()
            print("\n")
        self.smallBlind().updateBet(self.smallBlind)
        self.bigBlind().updateBet(self.bigBlind)
        self.table.update_currentBet(self.bigBlind)
        bettingRoundPreFlop(self)

def bettingRoundPreFlop(self):
    self.current_player_index = self.UTG()
    self.table.current_bet = self.bigBlind_Bet
    self.last_raiser = self.bigBlind()
    while True:
        self.current_player = self.players[self.current_player_index]
        playerTurn(self, self.current_player)
        self.incrementTurn()
        if self.check_endRound():
            break

def flop(self):
    if (len(self.active) == 1):
        self.endself()
    self.endRound()
    self.table.receive(self.deck.deal(3))
    self.table.display()
    self.table.displayPot()
    bettingRoundFlop(self)

def bettingRoundFlop(self):
    self.current_player_index = self.smallBlind()
    while True:
        self.current_player = self.active[self.current_player_index]
        playerTurn(self, self.current_player)
        self.incrementTurn()
        if self.check_endRound():
            break

def turn(self):
    if (len(self.active) == 1):
        self.endself()
    self.endRound()
    self.table.receive(self.deck.deal(1))
    self.table.display()
    self.table.displayPot()
    bettingRoundFlop(self)

def bettingRoundTurn(self):
    self.current_player_index = self.smallBlind()
    while True:
        self.current_player = self.active[self.current_player_index]
        playerTurn(self)
        self.incrementTurn()
        if self.check_endRound():
            break

def river(self):
    if (len(self.active) == 1):
        self.endself()
    self.endRound()
    self.table.receive(self.deck.deal(1))
    self.table.display()
    self.table.displayPot()
    bettingRoundFlop(self)

def bettingRoundRiver(self):
    self.current_player_index = self.smallBlind()
    while True:
        self.current_player = self.active[self.current_player_index]
        playerTurn(self)
        self.incrementTurn()
        if self.check_endRound():
            break

def showdown(self):
    pass
    


def playerTurn(self, player):
    self.turns_taken += 1
    player.turn()
    choice = input("1.Bet/Raise\n2.Call/Check\n3.Fold\n:")
    
    if (choice == "1"):
        bet = int(input("Enter bet:"))
        self.table.update_currentBet(bet)
        self.table.displayPot()
        self.last_raiser = player
    if (choice == "2"):
        self.table.updatepot()
        self.table.displayPot()
    if (choice == "3"):
        self.folded(player)

    def incrementButton(self):
        self.button = ((self.button + 1 ) % len(self.players))
    
    def folded(self, other):
        self.active.remove(other)
        self.current_player_index += -1
    
    def resetPlayers(self):
        self.active = self.players[:]
    
    def UTG(self):
        return self.players[(self.button + 3) % len(self.players)]
    
    def bigBlind(self):
        return self.players[(self.button + 2) % len(self.players)]

    def smallBlind(self):
        return self.players[(self.button + 1) % len(self.players)]
    
    def check_endRound(self):
        target_bet = None
        if self.turns_taken < len(self.active):
                return False
        for player in self.active:
            if player.chips > 0:
                target_bet = player.bet
                break
        
        for player in self.active:
            if player.chips == 0: continue
            if player.bet != target_bet:
                return False
        return True

    def endRound(self):
        self.last_raiser = None
        self.turns_taken = 0
        self.table.current_bet = 0
        
    def endself(self):
        pass

    def compareHands(self):
        highest_hand = (-1,)
        winner = None
        for player in self.active:
            hand = player.findHand()
            player.final_hand = []
            player.final_hand.append(self.hand_rankings.index(hand[0]))
            for i in range(1, len(hand)):
                player.final_hand.append(self.ranks.index(hand[i]))
            player.final_hand = tuple(player.final_hand)
            
            
            
        for player in self.active:
            if player.final_hand > highest_hand:
                highest_hand = player.final_hand
                winner = player

        return winner
    
    def incrementTurn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.active)