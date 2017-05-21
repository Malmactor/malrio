"""Tensorflow graph definition of neural network architecture
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


import tensorflow as tf


def nn_model(params, config=None):
    """
    NN graph definition
    :param params: Network parameters
    :param config: Configuration constants
    :return: Dict of exported graph nodes
    """
    # Just an example
    tf.reset_default_graph()
    exported_nodes = {}

    # Input and label nodes
    input_node = tf.placeholder(config["dtype"], shape=())
    label_node = tf.placeholder(config["dtype"], shape=())

    exported_nodes.update({"input": input_node, "label": label_node})

    # Conv, fc, what-so-ever
    weights = tf.get_variable("weights", shape=(512, 4), dtype=config["dtype"])
    logits = tf.matmul(input_node, weights)

    exported_nodes.update({"logits": logits})

    # Loss
    loss = tf.losses.softmax_cross_entropy(label_node, logits)

    exported_nodes.update({"loss": loss})

    # Gradient descent
    trainer = tf.train.AdadeltaOptimizer(0.3).minimize(loss)

    exported_nodes.update({"trainer": trainer})

    return exported_nodes
