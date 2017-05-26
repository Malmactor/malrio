"""Agents following static paths
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


import numpy as np
import time


def static_agent(path, simulation, render, config=None):

    init_pos = np.array([0, 2, 0]) if config is None or "init_pos" not in config else config["init_pos"]
    simulation.mario.state[:, 0] = init_pos

    for step in path:
        simulation.advance_frame(step)
        renderables = simulation.get_renderable()
        render.render(renderables)
        if config and config["sec_per_frame"]:
            time.sleep(config["sec_per_frame"])
