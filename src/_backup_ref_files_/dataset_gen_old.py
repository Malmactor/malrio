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

config = {"dtype": "float16",
          "delta_t": 1.0,
          "template_path": "SuperMarioBros/mission_template.xml",
          "epsilon": 0.001,
          "sec_per_frame": 0.016,
          "maze_param": {
            "r": 10,
            "c": 30,
            "transpose": True,
          },
          "num_map": 500,
          "timeout": 60}


rm = SV.generator.RandMap(config["maze_param"])
config["init_pos"] = np.array([rm.init_pos[0], rm.init_pos[1], 0]) # preset init pos
config["end_pos"] = np.array([rm.end_pos[0], rm.end_pos[1], 0]) # preset end pos

for i in range(config["num_map"]):
    print 'iter', i
    saved = False
    while not saved:
        rm.generate()
        simulation = SMB.MarioSimulation(rm.maze, config=config)
        actions = list(SMB.action_mapping.keys())

        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(config["timeout"])
        try:
            action_path = SV.a_star(rm.maze, simulation, config["init_pos"], config["end_pos"], actions, interval=5, config=config)
            signal.alarm(0)
        except Exception, msg:
            print "Timed out!"
            continue

        if action_path: # path find
            if DEBUG:
                print rm.maze
                print action_path
                host = SMB.instantiate_malmo(rm.maze)
                render = SMB.Renderer(host)
                AG.static_agent(action_path, simulation, render, config=config)

            SV.data.store(action_path, rm.maze)
            saved = True
            rm.maze = None
