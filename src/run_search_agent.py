"""Main program for testing search agent
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import Agent as AG
import Utility as UT
import SuperMarioBros as SMB
import Supervised as SV

config = SMB.simulation_config
config.update(SMB.render_config)

layout = SMB.layout_fromdefault()

# host = SMB.instantiate_malmo(layout)

# render = SMB.Renderer(host)

simulation = SMB.MarioSimulation(layout, config=config)

actions = ["right_jump", "right_jump", "nolr_jump", "remains"]

#action_path = SV.a_star(layout, simulation, config["init_pos"], config["end_pos"], actions, interval=5, config=config)

action_path = ['right_jump', 'remains', 'remains', 'remains', 'remains', 'right_jump', 'remains', 'remains', 'remains', 'remains', 'right_jump', 'remains', 'remains', 'remains', 'remains', 'right_jump', 'remains', 'remains', 'remains', 'remains', 'right_jump', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'remains', 'right_jump', 'remains', 'remains', 'remains', 'remains', 'right_jump', 'remains', 'remains', 'remains', 'remains']
print action_path

render = UT.TKRender(layout, config=config)

AG.static_agent(action_path, simulation, render, config=config)
