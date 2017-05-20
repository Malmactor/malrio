import MalmoPython
import time

import movement
from SuperMarioBros import *

layout = layout_fromdefault()
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

# Loop until mission ends:
if world_state.is_mission_running:
    # actor = movement.TestActor(agent_host, layout)
    actor = movement.AstarActor(agent_host, layout, interval=5)
    actor.run()

print
print "Mission ended"
