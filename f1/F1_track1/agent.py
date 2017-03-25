#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: agent.py
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import numpy as np
import cv2
import tensorflow as tf
#assert int(tf.__version__.split('.')[1]) == 9
assert int(np.__version__.split('.')[1]) >= 11

from collections import deque, Counter
import random
import time

from tensorpack import *
from tensorpack.RL import *
from tensorpack.utils.rect import Rect
from history import HistoryPlayerWithVar

NUM_ACTIONS = 6
IMAGE_SIZE = (120, 120)
CHANNEL = 4 * 3 * 2
IMAGE_SHAPE3 = IMAGE_SIZE + (CHANNEL,)

class EOGError:
    """ end of game"""
    pass

class FinalEnv(RLEnvironment):
    def __init__(self, game):
        self.game = game

        self._image_shape = IMAGE_SIZE
        self._frame_skip = 2

        center_patch = 0.22
        frac = center_patch / 2
        W, H = 512, 384
        self._center_rect = Rect(*map(int,
            [W/2 - W*frac, H/2 - H*frac, W*frac*2, H*frac*2]))

        self.last_history = deque(maxlen=60)
        self.current_ammo = 10
        self.timer = 0

    def dead(self):
        self.last_history.clear()
        self.current_ammo = 10
        self.timer = 0

    def parse_state(self, s):
        img = s.screen_buffer
        if img is None:
            raise EOGError()
        img = np.transpose(img, (1,2,0))
        center_patch = self._center_rect.roi(img)
        center_patch = cv2.resize(center_patch, self._image_shape[::-1])
        img = cv2.resize(img, self._image_shape[::-1])
        img = np.concatenate((img, center_patch), axis=2)

        v = s.game_variables
        v = [(v[0] - 50) * 0.01,    # health
             (v[1] - 50) * 0.01, # ammo
             0.5 if v[0] < 10 else -0.5,     # dying
             0.5 if v[1] < 3 else -0.5,   # short of ammo
             0.5 if v[1] == 0 else -0.5      # no ammo
            ]
        self.current_ammo = v[1]
        return img, v

    def current_state(self):
        return self.parse_state(self.game.get_state())

    def repeat_action(self, act):
        cnt = 0
        while len(self.last_history) > cnt + 1 \
                and self.last_history[-(cnt+1)] == act:
            cnt += 1
        return cnt

    def stuck_detect(self):
        if len(self.last_history) < 60:
            return False
        c = Counter(self.last_history)
        if len(c) == 1:
            return True
        c = Counter(list(self.last_history)[-40:])
        if len(c) == 2:
            keys = sorted(c.keys())
            if keys == [0,1]:
                if abs(c[0] - c[1]) < 2:
                    return True
        return False

    def action(self, act):
        # act: a distribution
        self.timer += 1
        act_distrib = act
        act = act.argmax()
        if act == 6: act = 4
        extra_attack = act != 2 and act_distrib[2] > 1e-2
        self.last_history.append(act)
        action = [False] * 8

        if self.current_ammo == 0 and act == 2:
            act_distrib[2] = 0
            action[7] = True    # turn180
            act = 3
        elif extra_attack:
            action[2] = True
        elif self.stuck_detect():
            action[7] = True    # turn180
            self.last_history.append(-1)
        if self.timer < 10:
            action[2] = True

        repeat = self._frame_skip
        is_attacking = extra_attack or (2 in list(self.last_history)[-3:])
        if is_attacking:
            repeat = 1

        if act in [0, 1, 2, 4, 5]:
            action[act] = True
            if act == 2:
                self.game.make_action(action, 1)
            else:
                if act in [0, 1]:
                    if self.repeat_action(act) > 3:
                        action[act] = False
                        action[6] = -9 if act == 0 else 9
                self.game.make_action(action, repeat)
        else:
            action[3] = 37 if not is_attacking else 25
            self.game.make_action(action, repeat)

        if self.game.is_player_dead():
            self.dead()
        return 0, False


class Model(ModelDesc):
    def _get_input_vars(self):
        return [InputVar(tf.float32, (None,) + IMAGE_SHAPE3, 'image'),
                InputVar(tf.float32, (None, 5), 'vars')]

    def _get_NN_prediction(self, state, is_training):
        """ image: [0,255]"""
        image, vars = state
        image = image / 255.0
        with argscope(Conv2D, nl=PReLU.f):
            l = (LinearWrap(image)
                .Conv2D('conv0', out_channel=32, kernel_shape=7, stride=2)
            # 60
                .Conv2D('conv1', out_channel=64, kernel_shape=7, stride=2)
                .MaxPooling('pool1', 3, 2)
            # 15
                .Conv2D('conv3', out_channel=128, kernel_shape=3)
                .MaxPooling('pool3', 3, 2, padding='SAME')
            # 7
                .Conv2D('conv4', out_channel=192, kernel_shape=3, padding='VALID')
            # 5
                .FullyConnected('fcimage', 1024, nl=PReLU.f)())

        vars = tf.tile(vars, [1, 10], name='tiled_vars')
        feat = tf.concat(1, [l, vars])

        policy = FullyConnected('fc-pi-m', feat, out_dim=NUM_ACTIONS, nl=tf.identity) * 0.1
        return policy

    def _build_graph(self, inputs, is_training):
        policy = self._get_NN_prediction(inputs, is_training)
        self.logits = tf.nn.softmax(policy, name='logits')

class Model2(ModelDesc):
    def _get_input_vars(self):
        return [InputVar(tf.float32, (None,) + IMAGE_SHAPE3, 'image'),
                InputVar(tf.float32, (None, 5), 'vars')]

    def _get_NN_prediction(self, state, is_training):
        """ image: [0,255]"""
        image, vars = state
        image = image / 255.0
        with argscope(Conv2D, nl=PReLU.f):
            l = (LinearWrap(image)
                .Conv2D('conv0', out_channel=32, kernel_shape=7, stride=2)
            # 60
                .Conv2D('conv1', out_channel=64, kernel_shape=7, stride=2)
                .MaxPooling('pool1', 3, 2)
            # 15
                .Conv2D('conv3', out_channel=128, kernel_shape=3)
                .MaxPooling('pool3', 3, 2, padding='SAME')
            # 7
                .Conv2D('conv4', out_channel=192, kernel_shape=3, padding='VALID')
            # 5
                .FullyConnected('fcimage', 1024, nl=PReLU.f)())

        vars = tf.tile(vars, [1, 10], name='tiled_vars')
        feat = tf.concat(1, [l, vars])

        policy = FullyConnected('fc-pi-m', feat, out_dim=NUM_ACTIONS+1, nl=tf.identity)
        return policy

    def _build_graph(self, inputs, is_training):
        policy = self._get_NN_prediction(inputs, is_training)
        self.logits = tf.nn.softmax(policy, name='logits')

class Runner(object):
    def __init__(self, game):
        p = FinalEnv(game)
        self.player = HistoryPlayerWithVar(p, 4)

        cfg = PredictConfig(
                model=Model(),
                session_init=SaverRestore('model.tfmodel'),
                input_var_names=['image', 'vars'],
                output_var_names=['logits'])
        self._pred_func = get_predict_func(cfg)

    def action_func(self, inputs):
        f = self._pred_func
        act = f([[inputs[0]], [inputs[1]]])[0][0]
        return act

    def step(self):
        try:
            s = self.player.current_state()
        except EOGError:
            return
        act = self.action_func(s)
        self.player.action(act)
