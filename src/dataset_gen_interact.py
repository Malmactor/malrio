"""Main program for running keyboard agent without annoying malmo stuff :)
"""

__author__ = "Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import Agent as AG
import SuperMarioBros as SMB
import Utility as UT
import Supervised as SV
import Utility as Util

DEBUG  = False

# may move to global config

config = SMB.simulation_config
config.update(SMB.render_config)

layout = SV.make_simple_layout(config)

render = UT.TKRender(layout, config)
percept_render = Util.PerceptionRenderer(layout, tfrecord_writer=None, config=config)

simulation = SMB.MarioSimulation(layout, config)

keypoller = SMB.KeyPoller()

pos_act_pairs = AG.interactive_agent(simulation, keypoller, render, config)

crop_x = config["pix_per_block"]*config["crop_area"][0]
crop_y = config["pix_per_block"]*config["crop_area"][1]

SV.data.store_cropped(crop_x, crop_y, percept_render, pos_act_pairs, 'input_map.txt', 'input_action.txt', config)

if DEBUG:
    SV.data.read_cropped("input_map.txt", (5, 60, 60, 4))
    SV.data.read_cropped("input_action.txt")
