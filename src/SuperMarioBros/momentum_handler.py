"""Momentum and acceleration handlers for change in movement
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np

from configuration import *


# State interpretation rules:
# 1. if y-velocity is 0, mario is on the ground, since collision resolution would have cleared y-velocity in that case.

# Physics constants initialization
def init_phyx_const():
    norm = phyx_const["norm"]
    for k, v in phyx_const.items():
        if isinstance(v, str):
            phyx_const[k] = np.float32(int(v, base=16) / norm)


def give_gravity(state):
    state[1, 2] = phyx_const["gravity"]


# Collision-related handlers
def collision_resolved(state, delta):
    # Back to a collision-free position
    state[0:2, 0] -= delta


def hit_ground(state):
    # Clear y-velocity
    state[1, 1] = 0.0
    state[1, 2] = 0.0


def hit_sides(state):
    # Clear x-velocity
    print "hit sides"
    state[0, 1] = 0


def hit_ceiling(state):
    # Invert the y-direction velocity
    state[1, 1] = -state[1, 1]


# Action related handlers
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

    # Clamp maximum speed
    sign = np.sign(state[0, 1])
    speed = np.abs(state[0, 1])
    speed = np.minimum(speed, phyx_const["max_walk_speed"])
    state[0, 1] = sign * speed


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
            state[1, 1] = phyx_const["jump_hix_init_v"]
            state[1, 2] = phyx_const["jump_mix_hold_g"]

    # Hold A in midair
    else:
        if np.abs(state[0, 1]) < phyx_const["jump_lomi_threshold"]:
            state[1, 2] = phyx_const["jump_lox_hold_g"]

        elif np.abs(state[0, 1]) < phyx_const["jump_mihi_threshold"]:
            state[1, 2] = phyx_const["jump_mix_hold_g"]

        else:
            state[1, 2] = phyx_const["jump_mix_hold_g"]

    # Clamp maximum speed
    sign = np.sign(state[1, 1])
    speed = np.abs(state[1, 1])
    speed = np.minimum(speed, phyx_const["max_fall_speed"])
    state[1, 1] = sign * speed


def horizontal_deact(state):
    # Ground case
    if np.abs(state[1, 1]) < simulation_config["epsilon"]:

        # If mario is in skidding state, the deceleration will not change
        # Otherwise, the releasing deceleration will be given to mario
        if np.abs(np.abs(state[0, 2]) - phyx_const["skid_dec"]) > simulation_config["epsilon"]:
            sign = np.sign(state[0, 1])
            state[0, 2] = sign * -1 * phyx_const["rels_dec"]

        # The x-velocity and x-acceleration would be cleared when mario is not moving horizontally
        if np.abs(state[0, 1]) < phyx_const["stop_threshold"]:
            state[0, 1] = 0
            state[0, 2] = 0

    # Midair case
    else:
        # Releasing the direction buttons in midair will only drop horizontal accelerations
        state[0, 2] = 0


def vertical_deact(state):
    # Releasing A on the ground has no effect on mario
    # Only consider midair cases
    if np.abs(state[1, 1]) > simulation_config["epsilon"]:
        if np.abs(state[0, 1]) < phyx_const["jump_lomi_threshold"]:
            state[1, 2] = phyx_const["jump_lox_rels_g"]
        elif np.abs(state[0, 1]) < phyx_const["jump_mix_rels_g"]:
            state[1, 2] = phyx_const["jump_mix_rels_g"]
        else:
            state[1, 2] = phyx_const["jump_hix_rels_g"]


def left_nojump(state):
    horizontal_enact(state, -1)
    vertical_deact(state)


def left_jump(state):
    horizontal_enact(state, -1)
    vertical_enact(state)


def right_nojump(state):
    horizontal_enact(state, 1)
    vertical_deact(state)


def right_jump(state):
    horizontal_enact(state, 1)
    vertical_enact(state)


def nolr_jump(state):
    horizontal_deact(state)
    vertical_enact(state)


def no_key(state):
    horizontal_deact(state)
    vertical_deact(state)


def remains(state):
    pass


action_mapping = {
    "remains": remains,
    "left_nojump": left_nojump,
    "right_nojump": right_nojump,
    "left_jump": left_jump,
    "right_jump": right_jump,
    "nolr_jump": nolr_jump,
    "no_key": no_key
}
