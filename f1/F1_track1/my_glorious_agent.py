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
    # Log your frags every ~5 seconds
    print("Frags:", game.get_game_variable(GameVariable.FRAGCOUNT))

print(20*"#")
print("Match results:")
print("My frags: " + str(game.get_game_variable(GameVariable.FRAGCOUNT)))
print()
print("Player1: " + str(game.get_game_variable(GameVariable.PLAYER1_FRAGCOUNT)))
print("Player2: " + str(game.get_game_variable(GameVariable.PLAYER2_FRAGCOUNT)))
print("Player3: " + str(game.get_game_variable(GameVariable.PLAYER3_FRAGCOUNT)))
print("Player4: " + str(game.get_game_variable(GameVariable.PLAYER4_FRAGCOUNT)))
print("Player5: " + str(game.get_game_variable(GameVariable.PLAYER5_FRAGCOUNT)))
print("Player6: " + str(game.get_game_variable(GameVariable.PLAYER6_FRAGCOUNT)))
print("Player7: " + str(game.get_game_variable(GameVariable.PLAYER7_FRAGCOUNT)))
print("Player8: " + str(game.get_game_variable(GameVariable.PLAYER8_FRAGCOUNT)))

game.close()
