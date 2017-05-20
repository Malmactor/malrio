"""Agents following static paths
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


def static_agent(path, simulation):
    for step in path:
        simulation.advance_frame(step)