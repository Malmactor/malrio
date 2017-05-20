"""Main program for testing search agent
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


import numpy as np
import SuperMarioBros as SMB
import Supervised as SV
import Agent as AG


config = {"dtype": "float32",
          "template_path": "SuperMarioBros/mission_template.xml",
          "init_pos": np.array([1, 3, 0]),
          "end_pos": np.array([3, 3, 0])}

layout = SMB.layout_fromdefault()

host = SMB.instantiate_malmo(layout)

simulation = SMB.MarioSimulation(layout, config=config)

actions = list(SMB.action_mapping.keys())

action_path = SV.a_star(layout, simulation, config["init_pos"], config["end_pos"], actions, config=config)

render = SMB.Renderer(host)

AG.static_agent(action_path, simulation, render, config)
