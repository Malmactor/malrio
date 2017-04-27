def generate_world(world_dict):
    return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

                  <About>
                    <Summary>Hello world!</Summary>
                  </About>

                  <ServerSection>
                    <ServerHandlers>
                      <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>
                      <ServerQuitFromTimeUp timeLimitMs="30000"/>
                      <ServerQuitWhenAnyAgentFinishes/>
                    </ServerHandlers>
                  </ServerSection>

                  <AgentSection mode="Survival">
                    <Name>MalmoTutorialBot</Name>
                    <AgentStart>
                      <Placement x="0" y="227" z="0"/>
                    </AgentStart>
                    <AgentHandlers>
                      <ObservationFromFullStats/>
                      <ContinuousMovementCommands turnSpeedDegs="180"/>
                    </AgentHandlers>
                  </AgentSection>
                </Mission>'''
