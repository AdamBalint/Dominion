import random

import click


class Agent(object):
    def __init__(self):
        '''Base agent class. Agents are used to make decisions for each
        player in the game. Custom agents can be created by inheriting
        this class and modifying the decision functions.'''
        pass

    def _get_game_state(self):
        pass

    def select_action(self, valid_actions):
        raise NotImplementedError

    def select_buy(self, valid_buys):
        raise NotImplementedError

    def select_gain(self, valid_gains):
        raise NotImplementedError

    def select_discard(self, valid_discard):
        raise NotImplementedError

    def select_trash(self, valid_trash):
        raise NotImplementedError

    def select_n_discard(self, valid_n):
        raise NotImplementedError

    def select_n_trash(self, valid_n):
        raise NotImplementedError


def _user_select_from_list(option_name, options):
    """Prompt the user to select options of type `option_name` (e.g. buys or
    actions) from the list `options`, by entering a number at the keyboard (or
    q to exit the program).

    Returns the selected element of `options`.
    """
    assert len(options) < 100

    click.echo(
        'Select {} (h for help, q to quit Dominion):'.format(option_name))

    for i, action in enumerate(options):
        click.echo('{}: {}'.format(i, action))

    while True:
        char = click.getchar()
        if char.lower() == 'h':
            click.echo()
            click.echo('  Enter the digit of the desired option.\n\n'
                       '  If there are more than 10 options:\n'
                       '  Enter <digit><space> for single-digit options, and\n'
                       '        <digit><digit> for double-digit options.')
            click.echo()

        elif char.lower() == 'q':
            click.echo('Farewell.')
            exit()

        elif char.isdigit():
            index = int(char)
            if len(options) <= index:
                continue

            # NOTE(brendan): This hacky code handles the case where there are
            # >= 10 options, and the user has to distinguish between single
            # digit and double digit indices.
            if (len(options) > 10) and ((len(options) // 10) >= index):
                next_char = click.getchar()
                if next_char.isspace():
                    return options[index]

                if not next_char.isdigit():
                    continue

                index = int(char + next_char)
                if len(options) <= index:
                    continue

            return options[index]


class HMIAgent(Agent):
    """A Human Machine Interface agent, which takes input from the command
    line.
    """
    def __init__(self):
        super(HMIAgent, self).__init__()

    def select_action(self, valid_actions):
        """Select an action from the list of enumerated valid actions, by
        inputting a number at the keyboard.

        Typing Q quits the Dominion game.
        """
        return _user_select_from_list('action', valid_actions)

    def select_buy(self, valid_buys):
        return _user_select_from_list('buy', valid_buys)

    def select_gain(self, valid_gains):
        return _user_select_from_list('gain', valid_gains)

    def select_discard(self, valid_discard):
        return _user_select_from_list('discard', valid_discard)

    def select_trash(self, valid_trash):
        return _user_select_from_list('trash', valid_trash)

    def select_n_discard(self, valid_n):
        return _user_select_from_list('number of cards to discard', valid_n)

    def select_n_trash(self, valid_n):
        return _user_select_from_list('number of cards to trash', valid_n)


class RandomAgent(Agent):
    def __init__(self):
        '''Agent that makes decisions randomly.'''
        super(RandomAgent, self).__init__()

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
        selected_buy = random.choice(valid_buys)
        return selected_buy

    def select_gain(self, valid_gains):
        '''Randomly select a card to gain from the list of valid cards.

        Args:
            valid_gain (list): Contains the card that will be gained.
        '''
        selected_gain = random.choice(valid_gains)
        return selected_gain

    def select_discard(self, valid_discard):
        '''Randomly select a card to discard.

        Args:
            valid_discard (list): Contains the card that will be discarded.
        '''
        selected_discard = random.choice(valid_discard)
        return selected_discard

    def select_trash(self, valid_trash):
        '''Randomly select a card to trash.

        Args:
            valid_trash (list): Contains the card that will be trashed.
        '''
        selected_trash = random.choice(valid_trash)
        return selected_trash

    def select_n_discard(self, valid_n):
        '''Randomly select a number of cards to discard

        Args:
            valid_n (list): Contains the options for the number of cards
            to discard.
        '''
        selected_n = random.choice(valid_n)
        return selected_n

    def select_n_trash(self, valid_n):
        '''Randomly select a number of cards to trash

        Args:
            valid_n (list): Contains the options for the number of cards
            to trash.
        '''
        selected_n = random.choice(valid_n)
        return selected_n

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

    def select_gain(self, valid_gains):
        return select_buy(valid_gains)

    def select_discard(self, valid_discard):
        raise NotImplementedError

    def select_trash(self, valid_trash):
        raise NotImplementedError

    def select_n_discard(self, valid_n):
        raise NotImplementedError

    def select_n_trash(self, valid_n):
        raise NotImplementedError

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