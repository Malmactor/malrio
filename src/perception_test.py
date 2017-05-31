__author__ = "Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np
import Utility as Util
import Supervised as SV

config = {
    'layout_area': (15, 11),
    'crop_area': (5, 5),
    'pix_per_block': 2,
    "mario_bb": np.array([0.45, 0.55]),
}

layout = SV.make_simple_layout(config)
print layout

pr = Util.PerceptionRenderer(layout, tfrecord_writer=None, config=config)

# test crop_layout
mario_center = (0.1, 0.1)
cropped = pr.crop_layout(mario_center)
print cropped
print pr.sample(cropped, mario_center)
