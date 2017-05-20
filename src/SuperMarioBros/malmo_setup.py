"""Instantiate a connection to Malmo
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import MalmoPython
import time
from configuration import *
from layout_loader import *


def instantiate_malmo(start_layout=None):
    """
    Instantiate a malmo agenthost from a given layout
    :param layout: 2d numpy array of a layout
    :return: Malmo agenthost instance
    """
    layout = layout_fromdefault() if start_layout is None else start_layout
    missionXML = layout_toxml(layout, {"template_path": "SuperMarioBros/mission_template.xml"})

    # start mission
    agent_host = MalmoPython.AgentHost()
    agent_host.addOptionalIntArgument("speed,s", "Length of tick, in ms.", 1)

    my_mission = MalmoPython.MissionSpec(missionXML, True)
    my_mission_record = MalmoPython.MissionRecordSpec()
    my_mission.allowAllAbsoluteMovementCommands()
    my_mission.allowAllDiscreteMovementCommands()
    agent_host.startMission(my_mission, my_mission_record)

    # Loop until mission starts:
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print "Error:", error.text

    return agent_host