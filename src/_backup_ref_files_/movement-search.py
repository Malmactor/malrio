import time
import json
import numpy as np
import pqdict
from abc import ABCMeta, abstractmethod

from Supervised.Astar import Astar
from src.SuperMarioBros.simulation import MarioSimulation

__author__ = "Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


class Actor:
    __metaclass__ = ABCMeta

    def __init__(self, host, layout):
        self.host = host
        self.world = host.getWorldState()
        self.sim = MarioSimulation(layout, {"dtype": "float16"})

    @abstractmethod
    def get_action(self):
        """Get next action.
        ret: {0: freeze, 1: left, 2: right, 3: jump}
        """
        pass

    def die(self):
        #### TODO ####
        print 'You are dead!'

    def complete(self):
        #### TODO ####
        print 'Mission Complete!'

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
                # check if finished
                if actnum == -1: # or if we detect it is close to target
                    return self.complete()
                # update pos, dpos ddpos
                self.sim.advance_frame(action=actnum)
                # change location
                self.host.sendCommand("tp " + str(self.sim.mario.state[0, 0]) +
                        " " + str(self.sim.mario.state[1, 0]) +
                        " " + str(self.sim.mario.state[2, 0]))
                print
                # death check
                if self.sim.mario.state[1, 0] < 0:
                    return self.die()


class TestActor(Actor):
    """Actor For Testing"""
    def __init__(self, host, layout):
        Actor.__init__(self, host, layout)

    def get_action(self):
        return 2


class AstarActor(Actor):
    def __init__(self, host, layout, interval, target=3):
        Actor.__init__(self, host, layout)
        self.Astar = Astar()
        self.Astar.feed_map(layout, interval, target)
        self.path = self.Astar.get_path()

    def get_action(self):
        if self.path:
            return self.path.pop(0)
        else:
            return -1 # denotes mission complete
