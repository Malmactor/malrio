import time
import json
import numpy as np
import pqdict
from abc import ABCMeta, abstractmethod

from SuperMarioBros.simulation import MarioSimulation

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
                    return self.die()


def l1_distance(a, b):
    return np.sum(np.abs(a - np.array(b)))


def pad_layout(layout):
    return np.pad(layout, (1, 1), 'constant', constant_values=1)


class AstarActor(Actor):
    def __init__(self, host, layout):
        Actor.__init__(self, host, layout)
        self.feed_map(layout, target=3) # we use the red mashroom as goal
        self.init_path()

    def feed_map(self, layout, target):
        """Feed the layout into the solver.
        The initial position is (0, 2) from the feet, (0, 3) from center.
        In our solver, the initial position is (1, 3) since we pad the map with a wall box.
        """
        self.layout = pad_layout(layout) # map
        self.target = target # end point
        self.start = np.array([1, 3])
        self.end = np.argwhere(self.layout == target).flatten()

    def encode_state(self, state):
        return str(state.flatten())

    def decode_state(self, state):
        return np.fromstring(state[1:-1], dtype="float16", sep=' ').reshape((3, 3))

    def init_path(self):
        r, c = self.layout.shape
        init_state = self.encode_state(self.sim.mario.state)

        # we use path to record states, and state_action_map to map state to action
        path = []
        state_action_map = {init_state: None}
        # state dict for previous state
        path_pre = {init_state: None}
        # cost to get this state, in terms of time (moves)
        cost = {init_state: 0}

        frontier_queue = pqdict.minpq({0: [init_state]})

        # TODO: use actoin (base on state matrix) + domain (possible induced state matrix)
        # instead of directions. For each loop in the heap, pop top state, calc all possible
        # induced state, then push them into the heap. Notice that final position could be
        # a range (rough position), since we use float.

        node = None
        while frontier_queue:
            # initial setup
            priority = frontier_queue.top()
            raw_frontier = frontier_queue[priority][0]
            frontier = self.decode_state(raw_frontier)
            # print frontier[0:2, 0], cost[raw_frontier]
            self.sim.mario.state = frontier
            del frontier_queue[priority][0]
            if not frontier_queue[priority]:
                del frontier_queue[priority]

            # task end test
            if l1_distance(self.end, frontier[0:2, 0]) < 0.5:
                node = raw_frontier

            # expand frontier
            next_cost = cost[raw_frontier] + 1
            for i in range(4):
                self.sim.run(action=i, printable=False)
                next_state = self.sim.mario.state
                raw_next_state = self.encode_state(next_state)
                # if new state is legal
                if not np.array_equal(next_state, frontier) and (
                        raw_next_state not in cost or next_cost < cost[raw_next_state]):
                    print i, next_state[0:2, 0]
                    cost[raw_next_state] = next_cost
                    path_pre[raw_next_state] = raw_frontier
                    state_action_map[raw_next_state] = i
                    heuristic = next_cost + l1_distance(self.end, next_state[0:2, 0])
                    if heuristic in frontier_queue:
                        frontier_queue[heuristic].append(raw_next_state)
                    else:
                        frontier_queue[heuristic] = [raw_next_state]

                self.sim.mario.state = frontier

        action_path = []
        while node:
            action_path.insert(state_action_map[node])
            node = path_pre[node]

        self.action_path = action_path


    def get_action(self):
        if self.action_path:
            return self.action_path.pop()
        return 3
