"""Main program for running keyboard agent without annoying malmo stuff :)
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import Agent as AG
import SuperMarioBros as SMB
import Utility as UT
import Supervised as SV

config = SMB.simulation_config
config.update(SMB.render_config)

layout = SV.make_simple_layout(config)

render = UT.TKRender(layout, config=config)

simulation = SMB.MarioSimulation(layout, config=config)

keypoller = SMB.KeyPoller()

actions = AG.interactive_agent(simulation, keypoller, render, config=config)

SV.data.store(actions, layout, 'gclayout.txt', 'gcpath.txt')
