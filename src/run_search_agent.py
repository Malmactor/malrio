"""Main program for testing search agent
"""

__author__ = "Liyan Chen, Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import Agent as AG
import Utility as UT
import SuperMarioBros as SMB
import Supervised as SV
import numpy as np


use_astar = False
use_mc = False


action_remapping = {
    0:"remains",
    1:"left_nojump",
    2:"right_nojump",
    3:"left_jump",
    4:"right_jump",
    5:"nolr_jump",
    6:"no_key"
}
config = SMB.simulation_config
config.update(SMB.render_config)

layout = SMB.layout_fromdefault()

simulation = SMB.MarioSimulation(layout, config=config)

if use_astar:
    actions = ["right_nojump", "right_jump", "nolr_jump", "remains"]
    action_path = SV.a_star(layout, simulation, config["init_pos"], config["end_pos"], actions, interval=5, config=config)
else:
    action_path = ['remains', 'remains', 'remains', 'remains', 'remains',
        'remains', 'remains', 'remains', 'remains', 'remains',
        'remains', 'remains', 'remains', 'remains', 'remains']
    with open("input_action.txt") as actiontxt:
        for i,line in enumerate(actiontxt):
            tpath = [action_remapping[int(val)] for val in map(np.float32,line.split())]
            action_path.extend(tpath)

print len(action_path)

if use_mc:
    host = SMB.instantiate_malmo(layout)
    render = SMB.Renderer(host)
else:
    render = UT.TKRender(layout, config=config)

AG.static_agent(action_path, simulation, render, config=config)
