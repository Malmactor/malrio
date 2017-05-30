"""Render an episode to frame-action pairs
"""

__author__ = "Chang Gao, Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


class PerceptionRenderer:
    def __init__(self, layout, crop_area=None, pix_per_block=4, tfrecord_writer=None, config=None):
        """
        :param layout: Global layout for an episode
        :param crop_area: 2D numpy array (w blocks, h blocks) specifying the cropping area size in BLOCKS
        :param pix_per_block: The number of pixels on every edge of a block. Default=4
        :param tfrecord_writer: TFRecord writer object/function
        :param config: Global configuration
        """
        pass

    def crop_layout(self, mario_center):
        """
        Crop an appropriate area from the episode layout and pad the area when appropriate
        :param mario_center: 2D numpy array of mario center position (x, y)
        :return: A cropped region of the layout represented as a 2D numpy array with size of (w, h)
        """
        pass

    def sample(self, cropped, mario_center):
        """
        Rasterize the cropped region and mario into pixel representations
        :param cropped: 2D numpy array of cropped layout
        :param mario_center: 2D numpy array of the mario center position
        :return: 3D numpy array (w * pix_per_block, h * pix_per_block, 4) of pixel-level one-hot encoding for the
        cropped region
        """
        pass

    def render(self, rigid):
        """
        Render the current state of the environment into pixel-level one-hot encoding. This function shall not give
        returns. Instead, calling it shall result in writing the 3D numpy representation into a TFRecord.
        :param rigid: Mario rigid
        :return: None.
        """
        pos = rigid.get_center()
        pass
