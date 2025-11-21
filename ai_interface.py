from card import Card

class PokerInterface:
    def __init__(self):
        self.rank_map = self.rank_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
                         '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        
        self.suit_map = self.suit_map = {'H': 1, 'D': 2, 'C': 3, 'S': 4}

    
    def card_to_nums(self, card):
        return [self.rank_map[card.rank], self.suit_map[card.suit]]
    
    def get_game_stat(self, game, player):
        state_vector = []

        for i in range(2):
                state_vector.extend(self.card_to_nums(player.hand[i]))

        community = game.table.community
        for i in range(5):
            if i < len(community):
                 state_vector.extend(self.card_to_nums(community[i]))
                
            else:
                 state_vector.extend([0,0])

        state_vector.append(player.chips)
        state_vector.append