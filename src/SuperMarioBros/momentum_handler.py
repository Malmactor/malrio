"""Momentum and acceleration handlers for change in movement
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

from configuration import *
import numpy as np


def collision_resolved(state, delta):
    # Back to a collision-free position
    state[0:2, 0] -= delta


def hit_ground(state):
    # Cancel the gravitational acceleration abd y-speed
    state[1, 1] = 0.0
    state[:, 2] = [0.0, 0.0, 0.0]


def hit_sides(state):
    # Invert the x-direction velocity
    state[0, 1] = -state[0, 1]


def hit_ceiling(state):
    # Invert the y-direction velocity
    state[1, 1] = -state[1, 1]


def walk(state, direction=1):
    # Change the x-direction velocity to walk speed
    speed = int(phyx_const["walk_speed"], base=16) / phyx_const["norm"]

    state[0, 1] = direction * speed


def right(state):
    return walk(state, direction=1)


def left(state):
    return walk(state, direction=-1)


def stop(state):
    # Change the x-direction velocity to 0
    state[0, 1] = 0


def press_jump(state):
    # Add initial velocity and gravity to the state
    v0 = int(phyx_const["jump_v0"], base=16) / phyx_const["norm"]
    gravity = int(phyx_const["gravity"], base=16) / phyx_const["norm"]

    if np.abs(state[1, 2]) > simulation_config["epsilon"]:
        state[1, 2] = gravity

    else:
        state[1, 1] = v0
        state[1, 2] = gravity


def remains(state):
    # no action
    pass


action_mapping = {
    0: remains,
    1: left,
    2: right,
    3: press_jump
}
