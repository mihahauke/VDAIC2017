#!/usr/bin/python

from __future__ import print_function
from vizdoom import *
from agent import Runner
import time

game = DoomGame()
game.load_config("config/my_custom_config.cfg")

# Name your agent and select color
# colors: 0 - green, 1 - gray, 2 - brown, 3 - red, 4 - light gray, 5 - light brown, 6 - light red, 7 - light blue
game.add_game_args("+name F1 +colorset 2")
game.init()

print("F1 joined the party!")


runner =  Runner(game)


# Play until the game (episode) is over.
while not game.is_episode_finished():
    if game.is_player_dead():
        # Use this to respawn immediately after death, new state will be available.
        game.respawn_player()
        # Or observe the game until automatic respawn.
        #game.advance_action();
        #continue;

    runner.step()
    


game.close()
