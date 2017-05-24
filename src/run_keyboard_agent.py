"""Main program for keyboard agent
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


import SuperMarioBros as SMB
import Agent as AG
import binascii


config = SMB.simulation_config

layout = SMB.layout_fromdefault()

host = SMB.instantiate_malmo(layout)

render = SMB.Renderer(host)

simulation = SMB.MarioSimulation(layout, config=config)

# keypoller = SMB.KeyPoller()
init_listener = AG.key_catch.init_listener

AG.keyboard_agent(simulation, init_listener, render, config=config)
