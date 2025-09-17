class Game():
    def __init__(self):
        self.players = []
        self.active = []
        self.button = 0
        self.smallBlind = 0
        self.bigBlind = 0
        self.current_player_index = 0
        self.current_player = None
        self.last_raiser = None
        self.blind_turn = 0

    def incrementButton(self):
        self.button = ((self.button + 1 ) % len(self.players))