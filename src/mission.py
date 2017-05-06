import MalmoPython
import movement
# from worldbuilder import generate_world
import os
import sys
import time
import numpy as np
from SuperMarioBros.layout_loader import layout_toxml, layout_fromdefault

DEBUG = False

layout = layout_fromdefault()
missionXML = layout_toxml(layout, {"template_path": "SuperMarioBros/mission_template.xml"})

if DEBUG:
    print(missionXML)


# start mission
agent_host = MalmoPython.AgentHost()
agent_host.addOptionalIntArgument("speed,s", "Length of tick, in ms.", 1)
try:
    agent_host.parse(sys.argv)
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)


my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()
my_mission.allowAllAbsoluteMovementCommands()
my_mission.allowAllDiscreteMovementCommands()
agent_host.startMission(my_mission, my_mission_record)


# Loop until mission starts:
if DEBUG:
    print "Waiting for the mission to start ",
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    if DEBUG:
        sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text


# Loop until mission ends:
while world_state.is_mission_running:
    actor = movement.AstarActor(agent_host, layout)
    actor.run()

print
print "Mission ended"
