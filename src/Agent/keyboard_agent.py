"""Agent plays with keyboard input
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


key_act_map = {
    "a": "left",
    "d": "right",
    " ": "press_jump"
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

    while not key == "q":
        key = keypoller()
        if key and key in key_act_map:
            simulation.advance_frame(key_act_map[key])
        else:
            simulation.advance_frame(empty_action)

        renderable = simulation.get_renderable()
        render.render(renderable)
