"""Interactive Agent that stops until commands
"""

__author__ = "Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np
import time
import sys

DEBUG = True

key_act_map = {
    "a": "left_nojump",
    "d": "right_nojump",
    "w": "nolr_jump",
    "q": "left_jump",
    "e": "right_jump",
    "s": "remains"
}

action_remapping = {
    0:"s",
    1:"a",
    2:"d",
    3:"q",
    4:"e",
    5:"w",
    6:"",
}

def interactive_agent(simulation, keypoller, render, history, config=None):

    empty_action = config["empty_action"]
    interval = config["interval"]
    key = None
    none_times = -1
    round_start = False

    # for action in history:
    #     simulation.advance_frame(key_act_map[key])
    #     renderable = simulation.get_renderable()
    #     render.render(renderable)

    pos_act_pairs = []
    postions = []
    actions = []

    def ndprint(a):
        print '[',
        for b in a:
            print '[',
            for c in b:
                print c,
                print ',',
            print('],')
        print ']',
    count = 0
    action_path = ["","","","","","","","","","","","","","","","",""]

    with open("input_action.txt") as actiontxt:
        for i,line in enumerate(actiontxt):
            tlist = map(np.float32,line.split())
            tpath = [action_remapping[int(val)] for val in tlist]
            action_path.extend(tpath)

    while not key == "m":
        if len(action_path) > 0:
            key = action_path.pop(0)
        else:
            key = "m"
        
        if key and key in key_act_map:
            round_start = True
            postions.append((simulation.mario.state[0, 0], simulation.mario.state[1, 0]))
            actions.append(key_act_map[key])
            simulation.advance_frame(key_act_map[key])
            # print key_act_map[key], 
            none_times = 0
            renderable = simulation.get_renderable()
            render.render(renderable)
            if DEBUG:
                print key_act_map[key]

        elif none_times < interval-1:
            # print "remains ",
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

    ndprint(simulation.mario.state)
    print(count)
    
    
    # print(simulation.mario.state)
    return pos_act_pairs
