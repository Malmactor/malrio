"""Agent plays with keyboard input
"""

__author__ = "Liyan Chen, Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

key_act_map = {
    "a": "left_nojump",
    "d": "right_nojump",
    "w": "nolr_jump",
    "q": "left_jump",
    "e": "right_jump"
}


def keyboard_agent(simulation, keypoller, render, config=None):
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

    key = None

    none_times = 0

    while not key == "m":
        key = keypoller()
        if key and key in key_act_map:
            simulation.advance_frame(key_act_map[key])
            none_times = 0
        elif none_times <= 5:
            simulation.advance_frame(empty_action)
            none_times += 1
        else:
            simulation.advance_frame("no_key")

        renderable = simulation.get_renderable()
        render.render(renderable)
