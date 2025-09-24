class Game():
    def __init__(self, table):
        self.players = []
        self.active = []
        self.button = 0
        self.smallBlind = 0
        self.bigBlind = 0
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

    def incrementButton(self):
        self.button = ((self.button + 1 ) % len(self.players))
    
    def folded(self, other):
        self.active.remove(other)
        self.current_player_index += -1
    
    def resetPlayers(self):
        self.active = self.players[:]
    
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
        
    def endGame(self):
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