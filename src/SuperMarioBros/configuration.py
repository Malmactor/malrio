"""Simulation configuration parameters
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

simulation_config = {
    "dtype": "float16",
    "delta_t": 1.0,
    "epsilon": 0.001
}

phyx_const = {
    "norm": 65536.0,
    "walk_speed": "02000", # original: "01900", here we increase it to simulate "continuous pressing the button"
    "jump_v0": "04000",
    "gravity": "-001E0"
}
