"""ConvLSTM RNN Cell
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np
import tensorflow as tf

_k_d = 3
_out_filters = 32
_in_channels = 32
_init = tf.contrib.layers.xavier_initializer_conv2d(uniform=True)
_dtype = "float16"


def ConvLSTM(inputs, state):
    c, h = state

    assert int(inputs.shape[3]) == _in_channels, "inputs channels mismatched with parameters, {} and {}".format(
        int(inputs.shape[3]), _in_channels)
    assert int(h.shape[3]) == _out_filters, "state channels mismatched with parameters, {} and {}".format(
        int(h.shape[3]), _out_filters)

    with tf.variable_scope("Gates"):
        x = tf.concat([inputs, h], axis=3)

        with tf.variable_scope("Conv"):
            in_depth = _in_channels + _out_filters
            kernel = tf.get_variable(
                "Kernel", [_k_d, _k_d, in_depth, _out_filters * 4], initializer=_init, dtype=_dtype)

            pre_gate = tf.nn.convolution(x, kernel, 'SAME')
