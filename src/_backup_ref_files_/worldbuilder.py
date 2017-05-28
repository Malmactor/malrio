
__author__ = "Bruce Tan"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


def generate_world(world_dict):

  def genItems():
    result = ''
    if "brick_block" in world_dict:
      for s in world_dict["brick_block"]:
        result += '<DrawBlock x="' + str(s.x) + '" y="' + str(s.y) + '" z="' + str(s.z) + '" type="brick_block"/>'
    if "double_block" in world_dict:
      for warp in world_dict["double_block"]:
        result += '<DrawBlock x="' + str(warp.x) + '" y="' + str(warp.y) + '" z="' + str(warp.z) + '" type="brick_block"/>'
        result += '<DrawBlock x="' + str(warp.x) + '" y="' + str(warp.y+1) + '" z="' + str(warp.z) + '" type="brick_block"/>'
    if "triple_block" in world_dict:
      for warp in world_dict["triple_block"]:
        result += '<DrawBlock x="' + str(warp.x) + '" y="' + str(warp.y) + '" z="' + str(warp.z) + '" type="brick_block"/>'
        result += '<DrawBlock x="' + str(warp.x) + '" y="' + str(warp.y+1) + '" z="' + str(warp.z) + '" type="brick_block"/>'
        result += '<DrawBlock x="' + str(warp.x) + '" y="' + str(warp.y+2) + '" z="' + str(warp.z) + '" type="brick_block"/>'
    if "mushroom" in world_dict:
      for m in world_dict["mushroom"]:
        result += '<DrawBlock x="' + str(m.x) + '" y="' + str(m.y) + '" z="' + str(m.z) + '" type="red_mushroom"/>'
    if "lava" in world_dict:
      for l in world_dict["lava"]:
        result += '<DrawBlock x="' + str(l.x) + '" y="' + str(1) + '" z="' + str(l.z) + '" type="air"/>'
        result += '<DrawBlock x="' + str(l.x) + '" y="' + str(0) + '" z="' + str(l.z) + '" type="lava"/>'
    return result

  return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Hello world!</Summary>
              </About>

              <ModSettings>
                <MsPerTick>17</MsPerTick>
              </ModSettings>

            <ServerSection>
              <ServerInitialConditions>
                <Time>
                    <StartTime>12000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
              </ServerInitialConditions>
              <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,45;17;"/>
                  <DrawingDecorator>
                    ''' + genItems() + '''
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="300000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Creative">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="0" y="2" z="0" yaw="-90"/>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ObservationFromGrid>
                      <Grid name="floor3x3">
                        <min x="-1" y="-1" z="-1"/>
                        <max x="1" y="1" z="-1"/>
                      </Grid>
                  </ObservationFromGrid>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''
