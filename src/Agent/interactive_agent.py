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

    actions = []
    empty_action = config["empty_action"]
    interval = config["interval"]
    key = None
    none_times = -1
    round_start = False

    while not key == "m":
        key = keypoller()

        if key and key in key_act_map:
            actions.append(key_act_map[key])
            simulation.advance_frame(key_act_map[key])
            none_times = 0
            renderable = simulation.get_renderable()
            render.render(renderable)
            if DEBUG:
                print key_act_map[key]

        elif none_times < interval-1:
            actions.append(empty_action)
            simulation.advance_frame(empty_action)
            none_times += 1
            renderable = simulation.get_renderable()
            render.render(renderable)

    return actions
