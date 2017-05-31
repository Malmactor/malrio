__author__ = "Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np
import Utility as Util
import Supervised as SV

config = {
    'layout_area': (11, 11),
    'crop_area': (5, 5),
    'pix_per_block': 4
}

layout = SV.make_simple_layout(config)
print layout

pr = Util.PerceptionRenderer(layout, tfrecord_writer=None, config=config)

# test crop_layout
mario_center = (0, 0)
cropped = pr.crop_layout(mario_center)
print cropped
print pr.sample(cropped, mario_center)
