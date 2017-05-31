"""Render an episode to frame-action pairs
"""

__author__ = "Chang Gao, Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np
from math import floor, ceil


class PerceptionRenderer:
    def __init__(self, layout, tfrecord_writer=None, config=None):
        """
        :param layout: Global layout for an episode
        :param tfrecord_writer: TFRecord writer object/function
        :param config: Global configuration{
            :param crop_area: 2D numpy array (x, y) specifying the cropping area size in BLOCKS
                              must be **odd** number
            :param pix_per_block: The number of pixels on every edge of a block. Default is 4
        }
        """
        self.layout = layout
        self.crop_area = None if config is None or "crop_area" not in config else config["crop_area"]
        self.layout_area = layout.shape if config is None or "layout_area" not in config else config["layout_area"]
        self.pix_per_block = 4 if config is None or "pix_per_block" not in config else config["pix_per_block"]
        self.tfrecord_writer = tfrecord_writer
        self.mario_bb = None if config is None or "mario_bb" not in config else config["mario_bb"]

        # pad layout, set y-axis pad to be 0, and x-axis pad to be 1 (including the corners)
        pad_layout = np.lib.pad(layout, (int(self.crop_area[0] / 2), int(self.crop_area[1] / 2)), 'constant',
                                constant_values=(1, 1))
        pad_layout[int(self.crop_area[0] / 2):-int(self.crop_area[0] / 2), -int(self.crop_area[1] / 2):] = 0
        self.pad_layout = pad_layout

        # other necessary stuff in config
        self.config = config

    def crop_layout(self, mario_center):
        """
        Crop an appropriate area from the episode layout and pad the area when appropriate
        :param mario_center: 2D numpy array of mario center position (x, y)
        :return: A cropped region of the layout represented as a 2D numpy array with size of (w, h)
        """
        return self.pad_layout[int(mario_center[0]):int(mario_center[0]) + self.crop_area[0],
               int(mario_center[1]):int(mario_center[1]) + self.crop_area[1]]

    def sample(self, cropped, mario_center):
        """
        Rasterize the cropped region and mario into pixel representations
        :param cropped: 2D numpy array of cropped layout
        :param mario_center: 2D numpy array of the mario center position
        :return: 3D numpy array (x * pix_per_block, y * pix_per_block, 4) of pixel-level one-hot encoding for the
        cropped region
        """
        expand_crop = cropped.repeat(self.pix_per_block, axis=0).repeat(self.pix_per_block, axis=1)
        edge_pad = int(self.crop_area[0]/2)*self.pix_per_block

        # bounding box of mario
        x_left = int(floor((mario_center[0] - self.mario_bb[0]) * self.pix_per_block))+edge_pad
        x_right = int(floor((mario_center[0] + self.mario_bb[0]) * self.pix_per_block))+edge_pad+1
        y_left = int(floor((mario_center[1] - self.mario_bb[1]) * self.pix_per_block))+edge_pad
        y_right = int(floor((mario_center[1] + self.mario_bb[1]) * self.pix_per_block))+edge_pad+1

        # generate one-hot encoding
        new_x, new_y = expand_crop.shape
        encoding_crop = np.zeros((new_x, new_y, 4))
        encoding_crop[x_left:x_right, y_left:y_right, 0] = 1 # mario
        encoding_crop[:,:,1][expand_crop == 1] = 1 # block
        encoding_crop[:,:,2][expand_crop == 2] = 1 # lava
        encoding_crop[:,:,3][expand_crop == 3] = 1 # goal

        return encoding_crop

    def render(self, rigid):
        """
        Render the current state of the environment into pixel-level one-hot encoding. This function shall not give
        returns. Instead, calling it shall result in writing the 3D numpy representation into a TFRecord.
        :param rigid: Mario rigid
        :return: None.
        """
        pos = rigid.get_center()
        # self.crop_layout(...)
        # self.sample(...)
        # call writer ...
        pass
