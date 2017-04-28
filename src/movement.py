import time
import json
import numpy

BTU = 0.01 # base_time_unit

class spos:
    def __init__(self, x, y, z):
        self.x = str(x)
        self.y = str(y)
        self.z = str(z)


class pos:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def eltadd(self, rhs):
        self.x += rhs.x
        self.y += rhs.y
        self.z += rhs.z

construe_action = {
    0: [pos(0, 0, 1)], # move left
    1: [pos(0, 0, -1)], # move right
    2: [pos(0, 1, 0), pos(0, 1, 0), pos(0, -1, 0), pos(0, -1, 0)], # low jump
    3: [pos(0, 1, 0), pos(0, 1, 0), pos(0, 1, 0), pos(0, 1, 0), pos(0, 1, 0),
        pos(0, -1, 0), pos(0, -1, 0), pos(0, -1, 0), pos(0, -1, 0), pos(0, -1, 0)], # mid jump
    4: [pos(0, 1, 0), pos(0, 1, 0), pos(0, 1, 0), pos(0, 1, 0), pos(0, 1, 0),
        pos(0, 1, 0), pos(0, 1, 0), pos(0, 1, 0), pos(0, 1, 0), pos(0, 1, 0),
        pos(0, -1, 0), pos(0, -1, 0), pos(0, -1, 0), pos(0, -1, 0), pos(0, -1, 0),
        pos(0, -1, 0), pos(0, -1, 0), pos(0, -1, 0), pos(0, -1, 0), pos(0, -1, 0)], # high jump
    5: [pos(0, 0, 0)], # do nothing
}

def current_pos(state):
    obs = json.loads(state.observations[-1].text)
    return pos(obs[u'XPos'], obs[u'YPos'], obs[u'ZPos'])

def get_action():
    return numpy.random.randint(6)

def act(host):
    actlist = []
    on_jump = False
    while True:
        world_state = host.getWorldState()
        if world_state.number_of_observations_since_last_state > 0:
            # get next action list
            actnum = get_action()
            # check or set if is in the air
            if actnum > 1 and actnum < 5:
                if on_jump:
                    actnum = 5
                else:
                    on_jump = True
            newactlist = construe_action[actnum]
            # merge into current action list
            for i in range(len(newactlist)):
                if len(actlist) > i:
                    actlist[i].eltadd(newactlist[i])
                else:
                    actlist.append(newactlist[i])
            # calc next position
            nextpos = current_pos(world_state)
            if actlist[0].y == 0:
                on_jump = False
            nextpos.eltadd(actlist.pop(0))
            # action
            time.sleep(BTU)
            host.sendCommand("tp " + str(nextpos.x) + " " + str(nextpos.y) + " " + str(nextpos.z))
