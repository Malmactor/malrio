"""Map dataset generator
"""

__author__ = "Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np
import SuperMarioBros as SMB
import Supervised as SV
import signal

def signal_handler(signum, frame):
    raise Exception("Timed out!")

DEBUG = False
if DEBUG:
    import Agent as AG

config = {
    "dtype": "float32",
    "delta_t": 1.0,
    "template_path": "SuperMarioBros/mission_template.xml",
    "epsilon": 0.00000001,
    "smaller_eps": 0.00000001,
    "greater_eps": 0.001,
    "block_radius": (0.5, 0.5),
    "mario_bb": np.array([0.45, 0.55]),
    "sec_per_frame": 0.016,
    "empty_action": "remains",
    "id2block": {0: 'air', 1: 'brick_block', 2: 'lava', 3: 'red_mushroom'},
    "crop_area": (15, 15),
    'layout_area': (120, 15),
    "num_map": 1,
    "timeout": 120
}


config["init_pos"] = np.array([2, 3, 0]) # preset init pos
config["end_pos"] = np.array([config["layout_area"][0]-1, 3, 0]) # preset end pos

for i in range(config["num_map"]):
    print 'iter', i
    saved = False
    while not saved:
        layout = SV.make_simple_layout(config)
        simulation = SMB.MarioSimulation(layout, config=config)
        actions = list(SMB.action_mapping.keys())

        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(config["timeout"])
        try:
            action_path = SV.a_star(layout, simulation, config["init_pos"], config["end_pos"], actions, interval=5, config=config)
            signal.alarm(0)
        except Exception, msg:
            print "Timed out!"
            continue

        if action_path: # path find
            if DEBUG:
                print layout
                print action_path
                host = SMB.instantiate_malmo(layout)
                render = SMB.Renderer(host)
                AG.static_agent(action_path, simulation, render, config=config)

            SV.data.store(action_path, layout)
            saved = True
            layout = None
