from deck import *
from card import *
from player import Player
from player import humanPlayer
from player import aiPlayer
from table import Table
from hand_detection import Hand_Detection


class Game():
    def __init__(self, table):
        self.deck = Deck()
        self.judge: "Hand_Detection" = Hand_Detection()
        self.players = []
        self.active = []
        self.button = 0
        self.smallBlind_Bet = 10
        self.bigBlind_Bet = 20
        self.current_player_index = 0
        self.current_player = None
        self.last_raiser = None
        self.turns_taken = 0
        self.table: "Table" = table
        self.last_raise_amount = 0
        self.street = 0
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['H', 'S', 'D', 'C']
        self.hand_rankings = [
    "HighCard",
    "Pair",
    "Two Pair",
    "Trips",
    "Straight",
    "Flush",
    "Full House",
    "Four of a Kind",
    "Straight Flush",
    "Royal Flush"
] 
    def reset(self):
        for player in self.players:
            if player.chips <= 0:
                player.chips = 1000
        self.resetPlayers()
        self.resetGame()
        self.table.reset()
        self.deck = Deck()
        self.deck.shuffle()
        for player in self.players:
            player.total_bet = 0
            player.clear_hand()
            player.all_in = False
        self.postBlinds()
        self.preflop()
        #self.players = [p for p in self.players if p.chips > 0]
        self.last_raiser = self.bigBlind()
        return self.get_state()
    
    
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
        #for player in self.players:
        #    if player.chips == 0:
        #        self.players.remove(player)
        self.active = self.players[:]
    
    def resetGame(self):
        self.current_player_index = 0
        self.current_player = None
        self.last_raiser = None
        self.turns_taken = 0
        self.incrementButton()



    def preflop(self):
        #deal 2 card to each player
        self.street = 0
        #print("Dealing:\n")
        for player in self.active:
            player.receiveCard(self.deck.deal(2))
            #player.displayHand()
            #print("\n")


    def flop(self):
        self.street = 1
        if (len(self.active) == 1):
            self.end_game()
        self.endRound()
        self.table.receive(self.deck.deal(3))
        self.table.display()
        self.table.displayPot()

    """def bettingRound(self, stage):
        self.last_raise_amount = self.bigBlind_Bet
        if stage == "Preflop":
            self.current_player_index = self.UTG_index()
            self.last_raiser = self.bigBlind()
        else:
            self.current_player_index = self.smallBlind_index()
            self.last_raiser = self.active[self.button]
        while True:
            self.current_player = self.active[self.current_player_index]
            self.playerTurn(self.current_player)
            self.incrementTurn()
            if self.check_endRound():
                break
                """

    def step(self, action):
        actions = ["fold", "check", "call", "half_raise", "3/4_raise", "pot_raise", "all-in"]

        player= self.active[self.current_player_index]
        starting_chips = player.chips
        self.execute_action(action)

        self.incrementTurn()

        if self.check_endRound():
            self.advance_street()
        
        done = False
        if len(self.active) == 1 or self.street > 3:
            self.end_game()
            done = True
        
        ending_chips = player.chips

        reward = 0
        if done:
            reward = ending_chips - starting_chips
        if action in [3, 4, 5, 6]: # Raise/All-In actions
            reward += 5
        return self.get_state(), reward, done        
        

    def turn(self):
        self.street = 2
        if (len(self.active) == 1):
            self.end_game()
        self.endRound()
        self.table.receive(self.deck.deal(1))
        self.table.display()
        self.table.displayPot()


    def river(self):
        self.street = 3
        if (len(self.active) == 1):
            self.end_game()
        self.endRound()
        self.table.receive(self.deck.deal(1))
        self.table.display()
        self.table.displayPot()

    def showdown(self):
        judge = Hand_Detection()
        for player in self.active:
            hand = judge.find_hand(player.hand, self.table.community)
            player.final_hand = []
            player.final_hand.append(self.hand_rankings.index(hand[0]))
            for i in range(1, len(hand)):
                player.final_hand.append(self.ranks.index(hand[i]))
            player.final_hand = tuple(player.final_hand)

        
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
        """
        
        min_raise = self.table.current_bet + self.last_raise_amount
        amount_to_call =self.table.current_bet - player.bet_in_round
        """
        amount_to_call = self.table.current_bet - player.bet_in_round
        action_type = player.get_action(valid_actions, amount_to_call=amount_to_call, pot=self.table.pot)
                
        if (action_type == "Bet"):
            max_bet = player.chips
            min_bet = self.bigBlind_Bet
            bet_amount = player.get_bet_amount(min_bet, max_bet)

            self.last_raise_amount = bet_amount

            player.updateChips(-bet_amount)
            self.table.updatePot(bet_amount)
            player.bet_in_round += bet_amount
            self.table.current_bet = player.bet_in_round
            self.last_raiser = player
            self.isAllIn(player)
            #print(f"{player.name} bets/raises to {player.bet_in_round}")
        
        elif (action_type == "Raise"):
            amount_to_call = self.table.current_bet - player.bet_in_round
            min_raise_total = self.table.current_bet + self.last_raise_amount
            max_raise_total = player.chips + player.bet_in_round

            min_raise_total = min(min_raise_total, max_raise_total)

            total_bet = player.get_bet_amount(min_raise_total, max_raise_total)

            new_raise_amount = total_bet - self.table.current_bet
            self.last_raise_amount = new_raise_amount
            chips_to_move = total_bet - player.bet_in_round
            player.updateChips(-chips_to_move)
            self.table.updatePot(chips_to_move)
            player.bet_in_round = total_bet
            self.table.current_bet = player.bet_in_round
            self.last_raiser = player
            self.isAllIn(player)
            #print(f"{player.name} raises to {total_bet}")

        elif (action_type == "Call"):
            amount_to_call = self.table.current_bet - player.bet_in_round

            chips_to_move = min (amount_to_call, player.chips)
            player.updateChips(-chips_to_move)
            self.table.updatePot(chips_to_move)
            player.bet_in_round += chips_to_move

            self.isAllIn(player)
            #print(f"{player.name} calls {chips_to_move}")

        elif action_type == "Check":
            #print(f"{player.name} checks.")
            pass

        elif action_type == "Fold":
            #print(f"{player.name} folds.")
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
    
    def UTG_index(self):
        return (self.button + 3) % len(self.players)
    
    def bigBlind_index(self):
        return (self.button + 2) % len(self.players)

    def smallBlind_index(self):
        return (self.button + 1) % len(self.players)
    
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
        for player in self.active:
            player.total_bet += player.bet_in_round
            player.bet_in_round = 0
        
 
    def incrementTurn(self):
        if len(self.active) == 0:
            return

    def check_for_winner(self):
        if len(self.active) == 1:
            self.end_game()
        
    def end_game(self):
        # CASE 1: Everyone else folded (One player left)
        if len(self.active) == 1:
            winner = self.active[0]
            winner.updateChips(self.table.pot)
            self.table.pot = 0
            return
        
        # CASE 2: Showdown (Compare Hands)
        # 1. Calculate everyone's hand strength
        self.showdown()

        # 2. Find the winner(s)
        best_hand = (-1,)
        winners = []

        for player in self.active:
            # Check if this player beats the current best
            if player.final_hand > best_hand:
                best_hand = player.final_hand
                winners = [player] # New single winner
            # Check for a tie (Split pot)
            elif player.final_hand == best_hand:
                winners.append(player)
        
        # 3. Pay the winner(s)
        if len(winners) > 0:
            # Integer division for split pots
            win_amount = self.table.pot // len(winners)
            for w in winners:
                w.updateChips(win_amount)
        
        # 4. Clear the pot
        self.table.pot = 0
            

    def compute_pots(self):
        eligible_players = self.active[:]
        last_bet_level = 0
        while len(eligible_players) > 0 :
            min_bet = 10000000000000000
            for player in eligible_players:
                min_bet = min(player.total_bet, min_bet)
            bet_per_player = min_bet - last_bet_level
            pot_size = bet_per_player * len(eligible_players)
            self.table.pots.append({
                        'amount': pot_size,
                        'eligible_players': eligible_players[:]
                    })  
            
            last_bet_level = min_bet

            eligible_players = [p for p in eligible_players if p.total_bet > min_bet]

    def isButton(self, player):
        if self.players.index(player) == self.button:
            return 1
        return 0
    
    def advance_street(self):
        self.street += 1
        
        if self.street == 1:
            self.flop()
        elif self.street == 2:
            self.turn()
        elif self.street == 3:
            self.river()
    
    def execute_action(self, action):
        player: "Player" = self.active[self.current_player_index]
        amount_to_call = self.table.current_bet - player.bet_in_round

        if action == 0:
            self.folded(player)
            
        
        elif action == 1 and amount_to_call > 0:
            self.folded(player)
        
        elif action == 2:
            bet = min(player.chips, amount_to_call)
            player.updateChips(-bet)
            player.bet_in_round += bet
            self.table.updatePot(bet)
            self.isAllIn(player)

        elif action == 3:
            raise_amount = int(self.table.pot * 0.5)
            raise_amount = max(raise_amount, self.last_raise_amount)
            
            total_cost = raise_amount + amount_to_call
            
            if total_cost >= player.chips:
                total_cost = player.chips 
                player.all_in = True
                
                actual_raise = total_cost - amount_to_call
                
                if actual_raise > 0:
                    self.last_raise_amount = actual_raise
                    self.last_raiser = player
                    self.table.current_bet = player.bet_in_round + total_cost
            
            else:
                self.last_raise_amount = raise_amount
                self.last_raiser = player
                self.table.current_bet = player.bet_in_round + total_cost

            player.updateChips(-total_cost)
            player.bet_in_round += total_cost
            self.table.updatePot(total_cost)

        elif action == 4:
            raise_amount = int(self.table.pot * 0.75)
            raise_amount = max(raise_amount, self.last_raise_amount)
            
            total_cost = raise_amount + amount_to_call
            
            if total_cost >= player.chips:
                total_cost = player.chips 
                player.all_in = True
                
                actual_raise = total_cost - amount_to_call
                
                if actual_raise > 0:
                    self.last_raise_amount = actual_raise
                    self.last_raiser = player
                    self.table.current_bet = player.bet_in_round + total_cost
            
            else:
                self.last_raise_amount = raise_amount
                self.last_raiser = player
                self.table.current_bet = player.bet_in_round + total_cost

            player.updateChips(-total_cost)
            player.bet_in_round += total_cost
            self.table.updatePot(total_cost)

        elif action == 5:
            raise_amount = int(self.table.pot)
            raise_amount = max(raise_amount, self.last_raise_amount)
            
            total_cost = raise_amount + amount_to_call
            
            if total_cost >= player.chips:
                total_cost = player.chips 
                player.all_in = True
                
                actual_raise = total_cost - amount_to_call
                
                if actual_raise > 0:
                    self.last_raise_amount = actual_raise
                    self.last_raiser = player
                    self.table.current_bet = player.bet_in_round + total_cost
            
            else:
                self.last_raise_amount = raise_amount
                self.last_raiser = player
                self.table.current_bet = player.bet_in_round + total_cost

            player.updateChips(-total_cost)
            player.bet_in_round += total_cost
            self.table.updatePot(total_cost)
        elif action == 6:
            bet = player.chips
            player.updateChips(-bet)
            player.bet_in_round += bet
            self.table.updatePot(bet)
            player.all_in = True

            if player.bet_in_round > self.table.current_bet:
                raise_size = player.bet_in_round - self.table.current_bet
                self.last_raise_amount = raise_size
                self.last_raiser = player
                self.table.current_bet = player.bet_in_round
                
    def get_state(self):
        hero = self.active[self.current_player_index]
        villain_index = (self.current_player_index + 1) % len(self.active)
        villain = self.active[villain_index]

        state = []

        for card in hero.hand:
            rank_val = self.ranks.index(card.rank) / 12.0 
            suit_val = self.suits.index(card.suit) / 3.0
            state.extend([rank_val, suit_val])

        for i in range(5):
            if i < len(self.table.community):
                card = self.table.community[i]
                rank_val = self.ranks.index(card.rank) / 12.0
                suit_val = self.suits.index(card.suit) / 3.0
                state.extend([rank_val, suit_val])
            else:
                state.extend([-1.0, -1.0])

        MAX_CHIPS = 1000.0 
        
        state.append(hero.chips / MAX_CHIPS)
        state.append(villain.chips / MAX_CHIPS)
        state.append(self.table.pot / MAX_CHIPS)
        state.append(self.table.current_bet / MAX_CHIPS)
        state.append(self.street / 4.0)

        return state