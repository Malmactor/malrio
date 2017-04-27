# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

import MalmoPython
import json
import math
import os
import random
import sys
import time
import errno
from timeit import default_timer as timer

# Test that AbsoluteMovementCommand teleportation works for long distances.

WIDTH=860
HEIGHT=480


def startMission(agent_host, xml):
    my_mission = MalmoPython.MissionSpec(xml, True)
    my_mission_record = MalmoPython.MissionRecordSpec()
    max_retries = 3
    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_mission_record )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print "Error starting mission",e
                print "Is the game running?"
                exit(1)
            else:
                time.sleep(2)

    world_state = agent_host.peekWorldState()
    while not world_state.has_mission_begun:
        time.sleep(0.1)
        world_state = agent_host.peekWorldState()
        for error in world_state.errors:
            print "Error:",error.text
        if len(world_state.errors) > 0:
            exit(1)

worldXML = '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>Teleportastic</Summary>
        </About>

        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime> <!-- Keep steady daylight to make image parsing simple -->
                </Time>
                <Weather>clear</Weather> <!-- Keep steady weather to make image parsing simple -->
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;;1;" forceReset="true" destroyAfterUse="true"/>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>Brundlefly</Name>
            <AgentStart>
                <Placement x="-100.5" y="4" z="400.5" yaw="0"/>  <!-- Look down at the ground -->
                <Inventory/>
            </AgentStart>
            <AgentHandlers>
                <ObservationFromFullInventory/>
                <AbsoluteMovementCommands/>
                <MissionQuitCommands/>
                <VideoProducer>
                    <Width>''' + str(WIDTH) + '''</Width>
                    <Height>''' + str(HEIGHT) + '''</Height>
                </VideoProducer>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
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

startMission(agent_host, worldXML)
world_state = agent_host.peekWorldState()

_x = 0;
_y = 0;
_z = 0;
agent_host.sendCommand("tp "+str(_x)+" "+str(_y)+" "+str(_z))

_y = _y + 4 #jump by 3
agent_host.sendCommand("tp "+str(_x)+" "+str(_y)+" "+str(_z))
print("Single Jump")
print("tp "+str(_x)+" "+str(_y)+" "+str(_z))
time.sleep(2) #wait for a sec to process the frame

_y = _y + 4 #jump by 3
agent_host.sendCommand("tp "+str(_x)+" "+str(_y)+" "+str(_z))
print("Double Jump")
print("tp "+str(_x)+" "+str(_y)+" "+str(_z))
time.sleep(1) #wait for a sec to process the frame


# Visited all the locations - quit the mission.
agent_host.sendCommand("quit")
while world_state.is_mission_running:
    world_state = agent_host.peekWorldState()

print "Teleport mission over."
world_state = agent_host.getWorldState()

print "Test successful"
exit(0)