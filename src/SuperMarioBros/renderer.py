"""Render actions to Malmo
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


class Renderer:
    def __init__(self, host):
        self.host = host

    def render(self, rigid):
        pos = rigid.state[:, 0]
        self.host.sendCommand("tp " + " ".join(map(lambda num: str(num), pos)))
