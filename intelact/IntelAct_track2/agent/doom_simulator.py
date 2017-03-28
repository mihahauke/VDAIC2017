from __future__ import print_function
import sys

sys.path.append('./bin/python')
import vizdoom
import random
import time
import numpy as np
import re


class DoomSimulator:
    def __init__(self, args):

        self.config = args['config']
        self.resolution = args['resolution']
        self.frame_skip = args['frame_skip']
        self.color_mode = args['color_mode']
        self.game_args = args['game_args']

        self._game = vizdoom.DoomGame()
        self._game.load_config(self.config)
        self._game.add_game_args(self.game_args)

        if 'ticrate' in args:
            self._game.set_ticrate(args['ticrate'])

        # set resolution
        try:
            self._game.set_screen_resolution(getattr(vizdoom.ScreenResolution, 'RES_%dX%d' % self.resolution))
        except:
            print("Requested resolution not supported:", sys.exc_info()[0])
            raise

        # set color mode
        if self.color_mode == 'RGB':
            self._game.set_screen_format(vizdoom.ScreenFormat.CRCGCB)
            self.num_channels = 3
        elif self.color_mode == 'GRAY':
            self._game.set_screen_format(vizdoom.ScreenFormat.GRAY8)
            self.num_channels = 1
        else:
            print("Unknown color mode")
            raise

        self.available_controls, self.continuous_controls, self.discrete_controls = self.analyze_controls(self.config)
        self.num_buttons = self._game.get_available_buttons_size()
        assert (self.num_buttons == len(self.discrete_controls) + len(self.continuous_controls))
        assert (len(self.continuous_controls) == 0)  # only discrete for now
        self.num_meas = self._game.get_available_game_variables_size()

        self.game_initialized = False

    def close_game(self):
        self._game.close()

    def analyze_controls(self, config_file):
        with open(config_file, 'r') as myfile:
            config = myfile.read()
        m = re.search('available_buttons[\s]*\=[\s]*\{([^\}]*)\}', config)
        avail_controls = m.group(1).split()
        cont_controls = np.array([bool(re.match('.*_DELTA', c)) for c in avail_controls])
        discr_controls = np.invert(cont_controls)
        return avail_controls, np.squeeze(np.nonzero(cont_controls)), np.squeeze(np.nonzero(discr_controls))

    def step(self, action):

        if not self.game_initialized:
            self._game.init()
            self.game_initialized = True

        rwrd = self._game.make_action(action, self.frame_skip)
        if self._game.is_episode_finished():
            return None, None, rwrd, True
        state = self._game.get_state()

        img = state.screen_buffer
        meas = state.game_variables  # this is a numpy array of game variables specified by the scenario
        term = self._game.is_episode_finished()

        return img, meas, rwrd, term

    def get_random_action(self):
        return [(random.random() >= .5) for i in range(self.num_buttons)]

    def is_new_episode(self):
        return self._game.is_new_episode()
