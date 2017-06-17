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
import numpy as np

DEBUG  = True

# may move to global config

config = SMB.simulation_config
config.update(SMB.render_config)


state = [ [ 102.425 , 0.115051 , 0.003479 , ],
[ 5.10396 , -0.250488 , -0.00732422 , ],
[ 0.0 , 0.0 , 0.0 , ],
]


config["init_pos"] = np.array([j[0] for j in state])
def ndprint(a):
        print '[',
        for b in a:
            print '[',
            for c in b:
                print c,
                print ',',
            print('],')
        print ']',

layout = SMB.layout_fromdefault()

# layout = SV.make_simple_layout(config)
# layout=layout.astype(np.int64)
# with open("l.txt", "w") as ll:
#     for line in layout:
#         ll.write('[')
#         for i, entry in enumerate(line):
#             ll.write(str(entry))
#             if i != len(line)-1:
#                 ll.write(', ')
#             else:
#                 ll.write('],\n')


render = UT.TKRender(layout, config)
percept_render = Util.PerceptionRenderer(layout, tfrecord_writer=None, config=config)

simulation = SMB.MarioSimulation(layout, config)


keypoller = SMB.KeyPoller()


new_actions = AG.interactive_agent(simulation, keypoller, render, config)

# print(new_actions)
with open("input_action.txt","a") as f:
    for action in new_actions:
        f.write(action+'\n')

ndprint(simulation.mario.state)

# crop_x = config["pix_per_block"]*config["crop_area"][0]
# crop_y = config["pix_per_block"]*config["crop_area"][1]

# SV.data.store_cropped(crop_x, crop_y, percept_render, pos_act_pairs, 'input_map.txt', 'input_action.txt', config)

# if DEBUG:
    # SV.data.read_cropped("input_map.txt", (5, 60, 60, 4))
    # SV.data.read_cropped("input_action.txt")
