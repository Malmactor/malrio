"""Interactive Agent that stops until commands
"""

__author__ = "Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np
import time

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
    key = None
    none_times = 0
    prevkey = None
    actions = []

    while not key == "m":
        key = keypoller()
        
        if key and key in key_act_map:
            prevkey = key
            print key_act_map[key]
            print simulation.mario.state
            simulation.advance_frame(key_act_map[key])
            actions.append(key_act_map[key])
            none_times = 0
            renderable = simulation.get_renderable()
            render.render(renderable)
        elif none_times <= 1:
            simulation.advance_frame(empty_action)
            actions.append(empty_action)
            none_times += 1
            renderable = simulation.get_renderable()
            render.render(renderable)
        # else:
        #     none_times = simulation.next_none_time(none_times)
    return actions
