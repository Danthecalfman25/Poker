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
        if self.turns_taken != len(self.active):
                return False
        for player in self.active:
            if player.chips > 0:
                target_bet = player.bet
        
        for player in self.active:
            if player.chips == 0: continue
            if player.bet != target_bet:
                return False
        return True