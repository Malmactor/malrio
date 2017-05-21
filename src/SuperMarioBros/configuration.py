"""Simulation configuration parameters
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


import numpy as np

simulation_config = {
    "dtype": "float16",
    "delta_t": 1.0,
    "template_path": "SuperMarioBros/mission_template.xml",
    "epsilon": 0.001,
    "sec_per_frame": 0.016,
    "init_pos": np.array([0, 3, 0]),
    "end_pos": np.array([7, 4, 0]),
}

phyx_const = {
    "norm": 65536.0,
    "walk_speed": "02000", # original: "01900", here we increase it to simulate "continuous pressing the button"
    "jump_v0": "04000",
    "gravity": "-001E0"
}
