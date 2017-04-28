import time
import json
import numpy


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

    def __str__(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)


class Actor:
    def __init__(self, host):
        self.host = host
        self.state = host.getWorldState()
        self.jump_status = 0  # Begin 0~1 Finish, 0 means not jumping, 0.5 for highest point
        self.move_status = 0  # Begin 0~1 Finish, 0 means not left/right movig
        self.jump_type = 0    # 0 for low, 1 for med, 2 for high
        self.move_type = 0    # 0 far left, 1 for right

    def current_pos(self):
        obs = json.loads(self.state.observations[-1].text)
        return pos(obs[u'XPos'], obs[u'YPos'], obs[u'ZPos'])

    def pos_shift(self):
        #### TODO ####
        return pos(0, 0, 1)

    def get_action(self):
        """Get next action.
        ret: {0: freeze, 1: left, 2: right, 3: low jump, 4: mid jump, 5: high jump}
        """
        #### TODO ####
        return 0  # numpy.random.randint(6)

    def boundcheck(self):
        """Check boundaries in all four direction.
        ret: [l ,r, u, d]
        """
        #### TODO ####
        return [False, False, False, False]

    def run(self):
        while True:
            self.state = self.host.getWorldState()
            if self.state.number_of_observations_since_last_state > 0:
                # get next action
                actnum = self.get_action()

                # 1. check all posibilities for current movement
                # -- 1.1 if jumping up and hits block
                if self.jump_status < 0.5 and self.boundcheck()[2] == True:
                    self.jump_status = 0.5
                # -- 1.2 if jumping down and hits block
                elif self.jump_status >= 0.5 and self.boundcheck()[3] == True:
                    self.jump_status = 0
                # -- 1.3 if moving left and hits block
                if self.move_type == 0 and self.move_status != 0 and self.boundcheck()[0] == True:
                    self.move_status = 0
                # -- 1.4 if moving right and hits block
                elif self.move_type == 1 and self.move_status != 0 and self.boundcheck()[1] == True:
                    self.move_status = 0

                # 2. check all posibilities for next movement
                # -- 2.1 check if already in air
                if actnum > 2:
                    if self.jump_status != 0:
                        actnum = 0
                    else:
                        self.jump_type = actnum-3
                # -- 2.2 check if already moving left/right
                elif actnum <= 2 and actnum > 0:
                    if self.move_status != 0:
                        actnum = 0
                    else:
                        self.move_type = actnum

                # 3. calc next position
                nextpos = self.current_pos()
                print(nextpos)
                poxshift = self.pos_shift()
                nextpos.eltadd(poxshift)
                print(nextpos)
                print

                # 4. action
                self.host.sendCommand("tp " + str(nextpos.x) + " " + str(nextpos.y) + " " + str(nextpos.z))
                time.sleep(0.1)

                # 5. reset status
                # if self.jump_status == 1:
                    # self.jump_status = 0
                if self.move_status == 1:
                    self.move_status = 0
