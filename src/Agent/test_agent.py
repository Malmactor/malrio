import numpy as np
import time

__author__ = "Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


def test_agent(simulation, render, config=None):
    init_pos = np.array([0, 2, 0]) if config is None or "init_pos" not in config else config["init_pos"]
    simulation.mario.state[:, 0] = init_pos
    simulation.advance_frame("remains")
    renderables = simulation.get_renderable()
    render.render(renderables)
    if config and config["sec_per_frame"]:
        time.sleep(config["sec_per_frame"])
    simulation.advance_frame("remains")
    renderables = simulation.get_renderable()
    render.render(renderables)
    if config and config["sec_per_frame"]:
        time.sleep(config["sec_per_frame"])
    simulation.advance_frame("remains")
    renderables = simulation.get_renderable()
    render.render(renderables)
    if config and config["sec_per_frame"]:
        time.sleep(config["sec_per_frame"])
    simulation.advance_frame("left")
    renderables = simulation.get_renderable()
    render.render(renderables)
    if config and config["sec_per_frame"]:
        time.sleep(config["sec_per_frame"])
    while True:
        simulation.advance_frame("remains")
        renderables = simulation.get_renderable()
        render.render(renderables)
        if config and config["sec_per_frame"]:
            time.sleep(config["sec_per_frame"])
