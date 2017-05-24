"""Testing (degbugging) module for physics
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


from layout_loader import *
from simulation import *


# Not unittesting to avoid overcomplicating problems
layout = layout_fromdefault()

simulation = MarioSimulation(layout, config=simulation_config)

simulation.mario.state[:, 0] = [3, 2.5, 0]
simulation.mario.state[:, 1] = [0.5, -0.5, 0]

print simulation.advance_frame("remains")

print simulation.mario.get_center()

# Expected to be [3, 2.5, 0]
print simulation.mario.state[:, 0]
