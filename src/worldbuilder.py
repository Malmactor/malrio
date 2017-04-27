def generate_world(world_dict):

  def genItems():
    result = ''
    if "brick_block" in world_dict:
      for s in world_dict["brick_block"]:
        result += '<DrawBlock x="' + s.x + '" y="' + s.y + '" z="' + s.z + '" type="brick_block"/>'
    if "warp_pipe" in world_dict:
      for warp in world_dict["warp_pipe"]:
        result += '<DrawBlock x="' + warp.x + '" y="' + warp.y + '" z="' + warp.z + '" type="wool" colour="GREEN" />'
        result += '<DrawBlock x="' + warp.x + '" y="' + warp.y + '" z="' + warp.z + '" type="wool" colour="GREEN" />'
        result += '<DrawBlock x="' + warp.x + '" y="' + warp.y + '" z="' + warp.z + '" type="grass" colour="GREEN" />'
    if "mushroom" in world_dict:
      for m in world_dict["mushroom"]:
        result += '<DrawBlock x="' + m.x + '" y="' + m.y + '" z="' + m.z + '" type="red_mushroom"/>'
    return result

  return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                  <About>
                    <Summary>Hello world!</Summary>
                  </About>
                  <ServerSection>
                    <ServerHandlers>
                        <FlatWorldGenerator generatorString="3;;1;" forceReset="true" destroyAfterUse="true"/>
                        <DrawingDecorator>''' + genItems() + '''</DrawingDecorator>
                        <ServerQuitWhenAnyAgentFinishes />
                    </ServerHandlers>
                  </ServerSection>
                  <AgentSection mode="Survival">
                    <Name>MalmoTutorialBot</Name>
                    <AgentStart>
                      <Placement x="0" y="4" z="0"/>
                    </AgentStart>
                    <AgentHandlers>
                      <ObservationFromFullStats/>
                      <ContinuousMovementCommands turnSpeedDegs="180"/>
                    </AgentHandlers>
                  </AgentSection>
                </Mission>'''
