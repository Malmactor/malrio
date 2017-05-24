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
    "init_pos": np.array([2, 3, 0]),
    "end_pos": np.array([9, 4, 0]),
    "empty_action": "remains"
}

phyx_const = {
    "norm": 65536.0,
    "min_walk_speed": "00130",
    "max_walk_speed": "01900",
    "walk_acc": "00098",
    "skid_dec": "001A0",
    "walk_speed": "02000", # original: "01900", here we increase it to simulate "continuous pressing the button"
    "jump_v0": "04000",
    "gravity": "-001E0"
}
