import MalmoPython
from movement import pos, movelist, testmove
from worldbuilder import generate_world
import os
import sys
import time


# generate world
world_dict = {}
missionXML = generate_world(world_dict)
print(missionXML)

# start mission
agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

my_mission = MalmoPython.MissionSpec(missionXML, True)
# my_mission.requestVideo( 320, 240, 1 )
my_mission_record = MalmoPython.MissionRecordSpec()     
agent_host.startMission(my_mission, my_mission_record)
my_mission.allowAllAbsoluteMovementCommands()



# start action
# testmove(agent_host)



# Loop until mission ends:
while world_state.is_mission_running:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission ended"
# Mission has ended.
