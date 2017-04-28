import time
import json
import numpy

## TODO:
## 1. bound back check and reaction
## 2. touch ground check, to prevent increment gain in height

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

    def printpos(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)


construe_action = {
    0: [pos(0, 0, 0.1), pos(0, 0, 0.1), pos(0, 0, 0.15), pos(0, 0, 0.15),
        pos(0, 0, 0.15), pos(0, 0, 0.15), pos(0, 0, 0.1), pos(0, 0, 0.1)], # move left
    1: [pos(0, 0, -0.1), pos(0, 0, -0.1), pos(0, 0, -0.15), pos(0, 0, -0.15),
        pos(0, 0, -0.15), pos(0, 0, -0.15), pos(0, 0, -0.1), pos(0, 0, -0.1)], # move right
    2: [pos(0, 0.14, 0), pos(0, 0.14, 0), pos(0, 0.13, 0), pos(0, 0.13, 0), pos(0, 0.13, 0),
        pos(0, 0.12, 0), pos(0, 0.12, 0), pos(0, 0.11, 0), pos(0, 0.11, 0), pos(0, 0.11, 0),
        pos(0, -0.11, 0), pos(0, -0.11, 0), pos(0, -0.11, 0), pos(0, -0.12, 0), pos(0, -0.12, 0),
        pos(0, -0.13, 0), pos(0, -0.13, 0), pos(0, -0.13, 0), pos(0, -0.14, 0), pos(0, -0.14, 0)], # low jump
    3: [pos(0, 0, 0)], # mid jump
    4: [pos(0, 0, 0)], # high jump
    5: [pos(0, 0, 0)], # do nothing
}

def current_pos(state):
    obs = json.loads(state.observations[-1].text)
    return pos(obs[u'XPos'], obs[u'YPos'], obs[u'ZPos'])

def get_action():
    return 2  # numpy.random.randint(6)

def act(host):
    actlist = []
    on_jump = False
    on_lr = False
    while True:
        world_state = host.getWorldState()
        if world_state.number_of_observations_since_last_state > 0:
            # get next action list
            actnum = get_action()
            # check or set if is in the air, or moving left and right
            if actnum > 1 and actnum < 5:
                if on_jump:
                    actnum = 5
                else:
                    on_jump = True
            elif actnum < 2:
                if on_lr:
                    actnum = 5
                else:
                    on_lr = True
            newactlist = construe_action[actnum]
            # merge into current action list
            for i in range(len(newactlist)):
                if len(actlist) > i:
                    actlist[i].eltadd(newactlist[i])
                else:
                    actlist.append(newactlist[i])
            # calc next position
            nextpos = current_pos(world_state)
            # reselt checker
            if actlist[0].y == 0:
                on_jump = False
            if actlist[0].z == 0:
                on_lr = False
            print(nextpos.printpos())
            print(actlist[0].printpos())
            nextpos.eltadd(actlist.pop(0))
            print(nextpos.printpos())
            print
            # action
            host.sendCommand("tp " + str(nextpos.x) + " " + str(nextpos.y) + " " + str(nextpos.z))
            prev_actnum = actnum
            time.sleep(0.1)
