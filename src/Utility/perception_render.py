"""Render an episode to frame-action pairs
"""

__author__ = "Chang Gao, Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np


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
        self.crop_area = (15, 15) if config is None or "crop_area" not in config else config["crop_area"]
        self.layout_area = layout.shape if config is None or "layout_area" not in config else config["layout_area"]
        self.pix_per_block = 4 if config is None or "pix_per_block" not in config else config["pix_per_block"]
        self.tfrecord_writer = tfrecord_writer

        # pad layout, set y-axis pad to be 0, and x-axis pad to be 1 (including the corners)
        pad_layout = np.lib.pad(layout, (int(self.crop_area[1] / 2), int(self.crop_area[0] / 2)), 'constant',
                                constant_values=(1, 1))
        pad_layout[int(self.crop_area[1] / 2):-int(self.crop_area[1] / 2), -int(self.crop_area[0] / 2):] = 0
        self.pad_layout = pad_layout
        # print pad_layout

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
        :return: 3D numpy array (x * pix_per_block-1, y * pix_per_block-1, 4) of pixel-level one-hot encoding for the
        cropped region
        """
        expand_crop = cropped.repeat(2, axis=0).repeat(2, axis=1)
        dx = int(mario_center[0] / 0.5) % 2
        dy = int(mario_center[1] / 0.5) % 2
        sample_crop = expand_crop[dx:expand_crop.shape[0] - 1 + dx, dy:expand_crop.shape[1] - 1 + dy]
        # TODO: one-hot encoding


        return sample_crop

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
