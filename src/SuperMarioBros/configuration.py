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
    "midair_hilo_threshold": "01900",
    "midair_forw_lo_acc": "00098",
    "midair_forw_hi_acc": "000E4",
    "midair_bckw_lo_acc": "000D0",
    "midair_bckw_hi_acc": "000E4",
    "jump_lomi_threshold": "01000",
    "jump_mihi_threshold": "02500",
    "jump_lox_init_v": "04000",
    "jump_hix_init_v": "05000",
    "jump_lox_hold_g": "-00200",
    "jump_mix_hold_g": "-001E0",
    "jump_hix_hold_g": "-00280"
    "walk_speed": "02000", # original: "01900", here we increase it to simulate "continuous pressing the button"
    "jump_v0": "04000",
    "gravity": "-001E0"
}
