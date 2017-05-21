"""Main program for testing search agent
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


import time
import numpy as np
import SuperMarioBros as SMB
import Supervised as SV
import Agent as AG


config = SMB.simulation_config

layout = SMB.layout_fromdefault()

host = SMB.instantiate_malmo(layout)

render = SMB.Renderer(host)

simulation = SMB.MarioSimulation(layout, config=config)

actions = list(SMB.action_mapping.keys())

action_path = SV.a_star(layout, simulation, config["init_pos"], config["end_pos"], actions, interval=5, config=config)

AG.static_agent(action_path, simulation, render, config=config)
