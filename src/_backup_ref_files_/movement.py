import time
import json
import numpy as np


class spos:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class pos:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

    def eltadd(self, rhs):
        return pos(self.x+rhs.x, self.y+rhs.y, self.z+rhs.z)

    def shiftcheck(self, rhs):
        """Check if it will shift into another block with given dx and dy.
        ret: 0-8, indicate the target block with [-1, 1] x [-1 , 1]
        """
        dx = int(self.x)-int(rhs.x)+1
        dy = int(self.y)-int(rhs.y)+1
        return dx + 3*dy


class RigidEntity:
    def __init__(self, x=0, y=0, z=0, config=None):
        self.config = config

        self.dtype = "float16" if config is None else config["dtype"]
        self.delta_t = 1.0  if config is None else config["delta_t"]
        self.delta_mat = np.identity(3, self.dtype)
        self.delta_mat[1, 0] = self.delta_t
        self.delta_mat[2, 1] = self.delta_t
        self.delta_mat[2, 0] = self.delta_t ** 2 / 2.0

        self.state = np.zeros([3, 3], dtype=self.dtype)
        self.state[:, 0] = [x, y, z]

    def __str__(self):
        return ' '.join(map(lambda num: str(num), self.state[:, 0]))

    def __getattr__(self, item):
        mapping = {"x": self.state[0, 0], "y": self.state[1, 0], "z": self.state[2, 0]}
        if item in mapping:
            return mapping[item]
        else:
            raise AttributeError("object has no attribute \'{:}\'".format(str(item)))

    def eltadd(self, rhs):
        result = self.__class__(config=self.config)
        result.state = self.state + rhs.state
        return result

    def shiftcheck(self, rhs):
        """Check if it will shift into another block with given dx and dy.
        ret: 0-8, indicate the target block with [-1, 1] x [-1 , 1]
        """
        dx = int(self.x)-int(rhs.x)+1
        dy = int(self.y)-int(rhs.y)+1
        return dx + 3*dy

    def update(self):
        self.state = np.dot(self.state, self.delta_mat)

    def reaction(self, op):
        op(self.state)


class CollisionResolver:
    def __init__(self, passive_box, active_box):
        pass


class Actor:
    def __init__(self, host):
        self.host = host
        self.state = host.getWorldState()
        self.jump_status = 0  # Begin 0~1 Finish, 0 means not jumping, 0.5 for highest point
        self.move_status = 0  # Begin 0~1 Finish, 0 means not left/right movig
        self.jump_type = 0    # 0 for low, 1 for med, 2 for high
        self.move_type = 0    # 0 far left, 1 for right
        self.bound = [False, False, False, False] # srounding boundaries

    def current_pos(self):
        obs = json.loads(self.state.observations[-1].text)
        return RigidEntity(obs[u'XPos'], obs[u'YPos'], obs[u'ZPos'])

    def lowjumpfuc(self):
        return 0.3-0.5*self.jump_status

    def midjumpfuc(self):
        return 0.39-0.65*self.jump_status

    def highjumpfuc(self):
        return 0.78-1.3*self.jump_status

    def movefuc(self):
        return (self.move_type*2 - 1)*(0.3025-(self.jump_status-0.55)*(self.jump_status-0.55))

    def pos_shift(self):
        dx = 0
        dy = 0
        # 1. for jumping
        if self.jump_status > 0:
            if self.jump_type == 0:
                dy += self.lowjumpfuc()
            elif self.jump_type == 1:
                dy += self.midjumpfuc()
            else:
                dy += self.highjumpfuc()
        # 2. for moving left/right
        if self.move_status > 0:
            dx += self.movefuc()
        return RigidEntity(dx, dy, 0)


    def get_action(self):
        """Get next action.
        ret: {0: freeze, 1: left, 2: right, 3: low jump, 4: mid jump, 5: high jump}
        """
        #### TODO ####
        # if numpy.random.randint(5) == 0:
        #     return 2
        return 4

    def die(self):
        #### TODO ####
        pass

    def boundcheck(self):
        """Check boundaries in all four directions [l ,r, u, d]."""
        self.bound = [False, False, False, True]
        # 1. get grid info
        obs = json.loads(self.state.observations[-1].text)
        grid = obs.get(u'floor3x3', 0)
        print(grid)
        # 2. get next interger position
        nextintpos = self.current_pos().shiftcheck(self.current_pos().eltadd(self.pos_shift()))
        # 3. test if a bound is there
        if grid[nextintpos] != u'air':
            if nextintpos % 3 == 0:
                self.bound[0] = True
            elif nextintpos % 3 == 2:
                self.bound[1] = True
            if int(nextintpos / 3) == 0:
                self.bound[3] = True
            elif int(nextintpos / 3) == 2:
                self.bound[2] = True
        print(self.bound)

    def run_1(self):
        self.state = self.host.getWorldState()
        if self.state.number_of_observations_since_last_state > 0:
            # get next action
            actnum = self.get_action()
        self.boundcheck()
        body = self.current_pos()

        def jump_init_velocity(state):
            state[1, 1] = 4.0 / 16.0
            state[1, 2] = 2.0 / 16.0 / 16.0

        body.reaction(jump_init_velocity)
        while True:
            self.state = self.host.getWorldState()
            if self.state.number_of_observations_since_last_state > 0:
                # get next action
                actnum = self.get_action()
            self.host.sendCommand("tp " + str(body.x) + " " + str(body.y) + " " + str(body.z))
            body.update()


    def run(self):
        turn = 0
        def jump_init_velocity(state):
            state[1, 1] = 4.0 / 16.0
            state[1, 2] = -2.0 / 16.0 / 16.0
            state[2, 1:3] = 0.0
        while True:
            self.state = self.host.getWorldState()
            if self.state.number_of_observations_since_last_state > 0:
                # get next action
                actnum = self.get_action()

                # 1. check all prerequisite for next movement
                # -- 1.1 check if already in air
                if actnum > 2:
                    if self.jump_status != 0 or self.bound[3] == False:
                        actnum = 0
                    else:
                        self.jump_type = actnum-3
                        self.jump_status = 0.05
                # -- 1.2 check if already moving left/right
                elif actnum <= 2 and actnum > 0:
                    if self.move_status != 0:
                        actnum = 0
                    else:
                        self.move_type = actnum
                        self.move_status = 0.05

                print("action to take: " + str(actnum))

                # 2. check all boundaries for next movement
                self.boundcheck()
                # -- 2.1 if jumping up and hits block
                if self.jump_status < 0.5 and self.bound[2] == True:
                    self.jump_status = 0.5
                # -- 2.2 if jumping down and hits block
                elif self.jump_status >= 0.5 and self.bound[3] == True:
                    self.jump_status = 0
                # -- 2.3 if moving left and hits block
                if self.move_type == 0 and self.move_status != 0 and self.bound[0] == True:
                    self.move_status = 0
                # -- 2.4 if moving right and hits block
                elif self.move_type == 1 and self.move_status != 0 and self.bound[1] == True:
                    self.move_status = 0

                # 3. calc next position
                if turn == 0:
                    curpos = self.current_pos()
                else:
                    curpos = nextpos
                nextpos = curpos.eltadd(self.pos_shift())

                if turn == 0:
                    body = self.current_pos()
                    body.state = nextpos.state
                    body.reaction(jump_init_velocity)
                    print body.state
                    print body.delta_mat

                print("current: " + str(curpos))
                print("next: " + str(nextpos))
                print "body:", str(body)
                print

                # 4. action
                #self.host.sendCommand("tp " + str(nextpos.x) + " " + str(nextpos.y) + " " + str(nextpos.z))
                self.host.sendCommand("tp " + str(body.x) + " " + str(body.y) + " " + str(body.z))
                body.update()

                # 5. reset status
                # -- 5.1 continue to jump
                if self.jump_status > 0 and self.jump_status < 1:
                    self.jump_status += 0.05
                # -- 5.2 continue to move left/right
                if self.move_status > 0 and self.move_status < 1:
                    self.move_status += 0.05
                # -- 5.3 die if fail inside the world
                if nextpos.y < 0:
                    return self.die()
                # -- 5.4 stop moving left/right if finish moving
                if self.move_status == 1:
                    self.move_status = 0
                turn += 1