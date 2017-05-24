"""Momentum and acceleration handlers for change in movement
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

from configuration import *
import numpy as np


# State interpretation rules:
# 1. if y-velocity is 0, mario is on the ground, since collision resolution would have cleared y-velocity in that case.

# Physics constants initialization
def init_phyx_const():
    norm = phyx_const["norm"]
    for k, v in phyx_const.items():
        if isinstance(v, str):
            phyx_const[k] = int(v, base=16) / norm

def give_gravity(state):
    state[1, 2] = phyx_const["gravity"]


# Collision related handlers
def collision_resolved(state, delta):
    # Back to a collision-free position
    state[0:2, 0] -= delta


def hit_ground(state):
    # Clear y-velocity
    state[1, 1] = 0.0


def hit_sides(state):
    # Clear x-velocity
    state[0, 1] = 0


def hit_ceiling(state):
    # Invert the y-direction velocity
    state[1, 1] = -state[1, 1]


# Action related handlers
def right(state):
    return horizontal_enact(state, direction=1)


def left(state):
    return horizontal_enact(state, direction=-1)


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
    state[0, 1] = 0


def horizontal_enact(state, direction):

    # Ground case
    if np.abs(state[1, 1]) < simulation_config["epsilon"]:

        # From still to walking
        if np.abs(state[0, 1]) < simulation_config["epsilon"]:
            state[0, 1] = phyx_const["min_walk_speed"] * direction
            state[0, 2] = phyx_const["walk_acc"] * direction

        # Skidding from the opposite direction to still
        elif np.sign(state[0, 1]) * direction == -1.0:
            state[0, 2] = phyx_const["skid_dec"] * direction

        # Accelerate towards the same direction
        else:
            state[0, 2] = phyx_const["walk_acc"] * direction

    # Midair case
    else:

        # Holding forward, including horizontally still cases
        if np.sign(state[0, 1]) * direction >= 0:

            # Low speed case
            if np.linalg.norm(state[:, 1]) < phyx_const["midair_hilo_threshold"]:
                state[0, 2] = phyx_const["midair_forw_lo_acc"] * direction

            # High speed case
            else:
                state[0, 2] = phyx_const["midair_forw_hi_acc"] * direction

        # Holding backward
        else:

            # Low speed and high speed cases
            if np.linalg.norm(state[:, 1]) < phyx_const["midair_hilo_threshold"]:
                state[0, 2] = phyx_const["midair_bckw_lo_acc"]
            else:
                state[0, 2] = phyx_const["midair_bckw_hi_acc"]


def vertical_enact(state):

    # Jump from the ground
    if np.abs(state[1, 1]) < simulation_config["epsilon"]:

        if np.abs(state[0, 1]) < phyx_const["jump_lomi_threshold"]:
            state[1, 1] = phyx_const["jump_lox_init_v"]
            state[1, 2] = phyx_const["jump_lox_hold_g"]

        elif np.abs(state[0, 1]) < phyx_const["jump_mihi_threshold"]:
            state[1, 1] = phyx_const["jump_lox_init_v"]
            state[1, 2] = phyx_const["jump_mix_hold_g"]

        else:




action_mapping = {
    "remains": remains,
    "left": left,
    "right": right,
    "press_jump": press_jump
}
