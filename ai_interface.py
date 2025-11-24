from card import Card

class PokerInterface:
    def __init__(self, game, table, bot, opponent):
        self.rank_map = self.rank_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
                         '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        
        self.suit_map = self.suit_map = {'H': 1, 'D': 2, 'C': 3, 'S': 4}

        self.game = game
        self.table = table
        self.bot = bot
        self.opponent = opponent

    
    def card_to_nums(self, card):
        return [self.rank_map[card.rank], self.suit_map[card.suit]]
    
    def get_game_stat(self,):
        state_vector = []

        for i in range(2):
                state_vector.extend(self.card_to_nums(self.bot.hand[i]))

        community = self.game.table.community
        for i in range(5):
            if i < len(community):
                 state_vector.extend(self.card_to_nums(community[i]))
                
            else:
                 state_vector.extend([0,0])

        state_vector.append(self.bot.chips)
        state_vector.append(self.opponent.chips)
        state_vector.append(self.game.table.pot)
        state_vector.append(self.game.table.current_bet)
        state_vector.append(self.game.table.current_bet - self.bet_in_round)
        state_vector.append(self.game.isButton(self))
        state_vector.append(self.game.last_raise_amount)
        state_vector.append(self.game.street)
        street = [0,0,0,0]
        street[self.game.street] = 1
        state_vector(street)