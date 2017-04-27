import MalmoPython
from movement import pos, movelist, testmove
from worldbuilder import generate_world
import os
import sys
import time


# generate world
world_dict = {}
missionXML = generate_world(world_dict)

# start mission
agent_host = MalmoPython.AgentHost()
my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()
my_mission.allowAllAbsoluteMovementCommands()
agent_host.startMission(my_mission, my_mission_record)

# start action
testmove(agent_host)
