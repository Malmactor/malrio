"""Agents following static paths
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


import numpy as np

def static_agent(path, simulation, render, config=None):

    init_pos = np.array([0, 3, 0]) if config is None or "init_pos" not in config else config["init_pos"]
    for step in path:
        simulation.advance_frame(step)

        renderables = simulation.get_renderable()
        render.render(renderables)