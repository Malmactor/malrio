"""Main program for running keyboard agent without annoying malmo stuff :)
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import SuperMarioBros as SMB
import Agent as AG
import Utility as UT


config = SMB.simulation_config
config.update(SMB.render_config)

layout = SMB.layout_fromdefault()

render = UT.TKRender(layout, config=config)

simulation = SMB.MarioSimulation(layout, config=config)

keypoller = SMB.KeyPoller()

AG.keyboard_agent(simulation, keypoller, render, config=config)
