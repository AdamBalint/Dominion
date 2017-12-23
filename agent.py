import random


class Agent(object):
    def __init__(self):
        '''Base agent class. Agents are used to make decisions for each
        player in the game. Custom agents can be created by inheriting
        this class and modifying the decision functions.'''
        pass

    def _get_game_state(self):
        pass

    def select_action(self, valid_actions):
        pass

    def select_buy(self, valid_buys):
        pass


class RandomAgent(Agent):
    def __init__(self):
        '''Agent that makes decisions randomly.'''
        pass

    def select_action(self, valid_actions):
        '''Randomly select an action from the list of valid actions.

        Args:
            valid_actions (list): Contains the actions that can be
            played this turn.
        '''
        selected_action = random.choice(valid_actions)
        return selected_action

    def select_buy(self, valid_buys):
        '''Randomly select a card to purchase from the list of valid buys.

        Args:
            valid_buys (list): Contains the cards that can be purchased
            this turn.
        '''
        valid_buys.remove('Curse')
        selected_buy = random.choice(valid_buys)
        return selected_buy

class ProbabilisticAgent(Agent):
    def __init__(self):
        print ("NI")
        self.total_cards = 10.0
        self.total_victory = 3
        self.total_money = 7
        self.total_actions = 0
        self.victory = ["Estate", "Province", "Dutchy", "Curse"]
        self.money = ["Copper", "Silver", "Gold"]


    def select_action(self, valid_actions):
        selected_action = random.choice(valid_actions)
        return selected_action


    def select_buy(self, valid_buys):
        #print ("In buy phase")
        valid_buys.remove('Curse')
        #print (valid_buys)
        probs = [(self.total_victory/self.total_cards, "victory"), (self.total_money/self.total_cards, "money"), (self.total_actions/self.total_cards, "action")]
        probs.sort(key=lambda probs: probs[0])
        #print (probs)
        for prob, card_type in probs:
            #print (valid_buys)
            #print ("Can buy " + card_type + ":", self.can_buy(card_type, valid_buys))
            if (self.can_buy(card_type, valid_buys)):
                choices = self.get_subset(card_type, valid_buys)
                selected_buy = random.choice(choices)
                print (choices)
                if card_type == 'money':
                    self.total_money += 1
                    self.total_cards += 1
                elif card_type == 'victory':
                    self.total_victory += 1
                    self.total_cards += 1
                elif card_type == 'action':
                    self.total_actions += 1
                    self.total_cards += 1
                #print (selected_buy)
                return selected_buy
        selected_buy = random.choice(valid_buys)
        return  selected_buy

    def get_category(self, card):
        if card in self.victory:
            return 'victory'
        elif card in self.money:
            return 'money'
        if card == 'Curse' or card == 'end_buy_phase':
            return None
        return 'action'

    def can_buy(self, card_type, valid_buys):
        types = [self.get_category(x) for x in valid_buys]
        if card_type in types:
            return True
        return False

    def get_subset(self, card_type, valid_buys):
        subset = []
        for valid_buy in valid_buys:
            if card_type == self.get_category(valid_buy):
                subset.append(valid_buy)
        return subset

    