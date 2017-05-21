"""Tensorflow-based training module
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


import tensorflow as tf
import numpy as np
import record


def training(node_map, config=None):
    """
    Training routine
    :param node_map: Graph node map
    :param config: Training configurations
    :return: None
    """
    with tf.Session() as sess:
        sess.run(???)
