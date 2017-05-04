import time
import json
import numpy as np
from SuperMarioBros.simulation import MarioSimulation

class Actor:
    def __init__(self, host, layout):
        self.host = host
        self.world = host.getWorldState()
        self.sim = MarioSimulation(layout, {"init_pos": (0, 2, 0), "dtype": "float16"})

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

    def run(self):
        print 'int_state:', self.sim.mario.state
        print
        cnt = 0
        while True:
            self.world = self.host.getWorldState()
            if self.world.number_of_observations_since_last_state > 0:
                cnt += 1
                print 'iter:', cnt
                # get next action
                actnum = self.get_action()
                # update pos, dpos ddpos
                self.sim.run(action=actnum)
                # change location
                self.host.sendCommand("tp " + str(self.sim.mario.state[0, 0]) +
                        " " + str(self.sim.mario.state[1, 0]) +
                        " " + str(self.sim.mario.state[2, 0]))
                print
                # death check
                if self.sim.mario.state[1, 0] < 0:
                    return die()
