"""Interactive Agent that stops until commands
"""

__author__ = "Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np
import time

DEBUG = True

key_act_map = {
    "a": "left_nojump",
    "d": "right_nojump",
    "w": "nolr_jump",
    "q": "left_jump",
    "e": "right_jump",
    "s": "remains"
}

def interactive_agent(simulation, keypoller, render, config=None):

    empty_action = config["empty_action"]
    interval = config["interval"]
    key = None
    none_times = -1
    round_start = False

    pos_act_pairs = []
    postions = []
    actions = []

    while not key == "m":
        key = keypoller()
        
        if key and key in key_act_map:
            round_start = True
            postions.append((simulation.mario.state[0, 0], simulation.mario.state[1, 0]))
            actions.append(key_act_map[key])
            simulation.advance_frame(key_act_map[key])
            none_times = 0
            renderable = simulation.get_renderable()
            render.render(renderable)
            if DEBUG:
                print key_act_map[key]

        elif none_times < interval-1:
            if round_start:
                postions.append((simulation.mario.state[0, 0], simulation.mario.state[1, 0]))
                actions.append(empty_action)
            simulation.advance_frame(empty_action)
            none_times += 1
            if none_times == interval-1:
                if round_start:
                    pos_act_pairs.append((postions, actions))
                postions = []
                actions = []
            renderable = simulation.get_renderable()
            render.render(renderable)

    return pos_act_pairs
