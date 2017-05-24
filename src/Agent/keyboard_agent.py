"""Agent plays with keyboard input
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

from key_catch import *

key_act_map = {
    "u'a'": "left_nojump",
    "u'd'": "right_nojump",
    " ": "nolr_jump",
    "u'a' ": "left_jump",
    "u'd' ": "right_jump"
}


def keyboard_agent(simulation, render, config=None):
    """
    Play game from keyboard input
    :param simulation: Simulation instance
    :param keypoller: Input instance
    :param empty_act: The action for no action/no key pressed
    :param render: Render instance
    :param config: Global configuration. empty_action is required.
    :return: None
    """

    empty_action = config["empty_action"]
    def processKeyInput(key):
        if key and key in key_act_map:
            print key_act_map[key]
            simulation.advance_frame(key_act_map[key])
        else:
            print "N"
            simulation.advance_frame(empty_action)

        renderable = simulation.get_renderable()
        render.render(renderable)
    key = None
    init_listener(processKeyInput)

