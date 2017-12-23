from game import Game
from agent import *
from cards import *


def play_game():
    agent_dict = {'DemoBot 1': ProbabilisticAgent()}
    demo_game = Game(n_players=3, agents=agent_dict, card_set='base', verbose=False)

    demo_game.players[0].display_deck()
    print("")

    demo_game.players[0].display_hand()
    print("")

    demo_game.players[0].display_draw_pile()
    print("")

    demo_game.players[0].display_discard_pile()
    print("")

    scores = demo_game.play_game()
    print (scores)

    for player in demo_game.players:
        print (player.player_id)
        player.hand.discard_hand()
        player.display_deck()


if __name__ == '__main__':
    play_game()
