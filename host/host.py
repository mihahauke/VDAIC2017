#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import vizdoom as vzd

MAX_MAP = 5
MAX_PLAYERS = 15
MAX_TIMELIMIT = 999
DEFAULT_TIMELIMIT = 10
SCENARIO = "cig2017.wad"

if __name__ == "__main__":
    parser = ArgumentParser("Host script for ViZDoom Copmetition at CIG 2017.",
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-b', '--bots', metavar="BOTS_NUM", dest='bots_num',
                        default=0, type=int,
                        help='number of bots to add [0,15]')
    parser.add_argument('-p', '--players', metavar="PLAYERS_NUM", dest='players_num',
                        default=1, type=int,
                        help='number of players [1,16]')
    parser.add_argument('-m', '--map', metavar="MAP", dest='map',
                        default=1, type=int,
                        help='map number [1,{}]'.format(MAX_MAP))
    parser.add_argument('-t', '--time', metavar="TIMELIMIT", dest='timelimit',
                        default=DEFAULT_TIMELIMIT, type=float,
                        help='timelimit in minutes [1,{}]'.format(MAX_TIMELIMIT))
    parser.add_argument('-c', '--console', dest='console_enabled', action='store_const',
                        default=False, const=True,
                        help='enable console')
    parser.add_argument('-w', '--watch', dest='watch', action='store_const',
                        default=False, const=True,
                        help='roam the map as a ghost spectator')
    #   TODO add recording settings
    #   TODO add episodic results printing

    args = parser.parse_args()

    players_num = args.players_num
    bots_num = args.bots_num
    map = "map0" + str(args.map)
    console_enabled = args.console_enabled
    timelimit = args.timelimit
    watch = args.watch

    if args.map < 1 or args.map > MAX_MAP:
        raise ValueError("Map number should be between 1 and {}. Got: {}".format(MAX_MAP).format(args.map))
    if players_num < 0:
        raise ValueError("Number of players should be >= 0. Got: {}".format(players_num))

    if bots_num + players_num > MAX_PLAYERS:
        raise ValueError("Maximum number of players and bots: {}. Got: {}".format(MAX_PLAYERS, bots_num + players_num))
    players_num += 1
    if timelimit < 0:
        raise ValueError("Negative time limit given: {}".format(timelimit))

    if timelimit > MAX_TIMELIMIT:
        raise ValueError(
            "Maximum timelimit of {} exceeded. "
            "This must be an erorr: {}".format(MAX_TIMELIMIT, timelimit))

    game = vzd.DoomGame()

    game.set_doom_map(map)

    game.set_doom_scenario_path(SCENARIO)
    game.add_game_args("-deathmatch +viz_nocheat 1 +viz_debug 0 +viz_respawn_delay 10")
    game.add_game_args("+sv_forcerespawn 1 +sv_noautoaim 1 +sv_respawnprotect 1 +sv_spawnfarthest 1 +sv_crouch 1")

    game.add_game_args("+viz_spectator 1")
    game.add_game_args("+name ghost")
    game.add_game_args("-host {}".format(players_num))
    game.add_game_args("+timelimit {}".format(timelimit))
    game.set_console_enabled(console_enabled)

    game.add_available_button(vzd.Button.TURN_LEFT)
    game.add_available_button(vzd.Button.TURN_RIGHT)
    game.add_available_button(vzd.Button.MOVE_RIGHT)
    game.add_available_button(vzd.Button.MOVE_LEFT)
    game.add_available_button(vzd.Button.MOVE_FORWARD)
    game.add_available_button(vzd.Button.MOVE_BACKWARD)
    game.add_available_button(vzd.Button.TURN_LEFT_RIGHT_DELTA)
    game.add_available_button(vzd.Button.LOOK_UP_DOWN_DELTA)
    game.add_available_button(vzd.Button.SPEED)
    game.add_available_button(vzd.Button.MOVE_UP)
    game.add_available_button(vzd.Button.MOVE_DOWN)

    if watch:
        game.set_mode(vzd.Mode.ASYNC_SPECTATOR)
        game.set_window_visible(True)
    else:
        game.set_mode(vzd.Mode.ASYNC_PLAYER)
        game.set_window_visible(False)

    game.set_screen_resolution(vzd.ScreenResolution.RES_1024X576)

    plural = "s"
    pn = "no"
    if players_num > 1:
        pn = players_num - 1
    if players_num == 2:
        plural = ""
    print("Starting vizdoom CIG 2017 host for {} player{}.".format(pn, plural))
    print("   WAD:        {}".format(SCENARIO))
    print("   TIMELIMIT:  {} min.".format(timelimit))
    print("   MAP:        {}".format(map))
    print("   PLAYERS:    {}".format(players_num - 1))
    print("   BOTS:       {}".format(bots_num))
    print("   CONSOLE:    {}".format(console_enabled))
    print()
    game.init()

    game.send_game_command("removebots")
    for i in range(bots_num):
        game.send_game_command("addbot")

    print("Host running.")
    while not game.is_episode_finished():
        game.advance_action()
