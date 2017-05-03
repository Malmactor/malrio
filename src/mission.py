import MalmoPython
import movement
from worldbuilder import generate_world
import os
import sys
import time
import numpy as np
from SuperMarioBros.layout_loader import layout_toxml

DEBUG = False

# generate world
world_dict = {
    "brick_block":[movement.spos(-1,3,-1),movement.spos(-1,3,0),movement.spos(-1,3,1),
                   movement.spos(0,3,-1),movement.spos(0,3,0),movement.spos(0,3,1),
                   movement.spos(1,3,-1),movement.spos(1,3,0),movement.spos(1,3,1)],
    "double_block":[movement.spos(8,6,0),movement.spos(14,6,0),movement.spos(16,6,0)],
    "triple_block":[movement.spos(15,8,0),movement.spos(19,8,0),movement.spos(23,8,0),movement.spos(31,8,0)],
    # "lava":[movement.spos(-5,2,0),movement.spos(-6,2,0),movement.spos(26,2,0),movement.spos(27,2,0)]
}
layout = np.array(
    [
        [0, 0, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [0, 0, 0, 1, 1]
    ]
)
#missionXML = generate_world(world_dict)
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
# my_mission.setViewpoint(2)
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
    actor = movement.Actor(agent_host)
    actor.run()

print
print "Mission ended"
