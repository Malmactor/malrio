"""Load world map layout into Malmo and other components
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


import xml.etree.ElementTree as ET
import numpy as np
import default_layout


def layout_toxml(layout, config=None):
    shape = layout.shape
    template_path = "mission_template.xml" if config is None or "template_path" not in config else config[
        "template_path"]
    id2block = {0: 'air', 1: 'brick_block', 2: 'lava',
                3: 'red_mushroom'} if config is None or "id2block" not in config else config["id2block"]
    block2id = dict(map(lambda item: (item[1], item[0]), id2block.items()))
    ns = {"ms": "http://ProjectMalmo.microsoft.com"}
    z_plane = 0 if config is None or "z_plane" not in config else config["z_plane"]

    xmltree = ET.parse(template_path).getroot()

    parent = list(xmltree.iter("{http://ProjectMalmo.microsoft.com}DrawingDecorator"))[0]
    for x in range(shape[0]):
        for y in range(shape[1]):
            if layout[x, y] != block2id['air']:
                block_element = ET.Element("{http://ProjectMalmo.microsoft.com}DrawBlock")
                block_element.set('x', str(x))
                block_element.set('y', str(y))
                block_element.set('z', str(z_plane))
                block_element.set('type', id2block[layout[x, y]])
                parent.append(block_element)

    return ET.tostring(xmltree)


def layout_fromfile(filename, config=None):
    return np.load(filename)


def layout_fromdefault():
    return default_layout.simple_layout


def layout_asblank():
    return default_layout.blank_layout
