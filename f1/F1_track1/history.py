#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: history.py
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import numpy as np
from tensorpack.RL import HistoryFramePlayer

__all__ = ['HistoryPlayerWithVar']

class HistoryPlayerWithVar(HistoryFramePlayer):
    def current_state(self):
        assert len(self.history) != 0
        assert len(self.history[0]) == 2, "state needs to be like [img, vars]"
        diff_len = self.history.maxlen - len(self.history)
        zeros = [np.zeros_like(self.history[0][0]) for k in range(diff_len)]
        for k in self.history:
            zeros.append(k[0])
        img = np.concatenate(zeros, axis=2)
        gvar = self.history[-1][1]
        return img, gvar

