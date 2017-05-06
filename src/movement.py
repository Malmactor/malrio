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


def l2_distance(a, b):
    return np.linalg.norm(a-b)


def pad_layout(layout):
    return np.pad(layout, (1, 1), 'constant', constant_values=1)


class AstarActor(Actor):
    def __init__(self, host, layout, interval):
        Actor.__init__(self, host, layout)
        self.interval = interval # upsampling interval
        self.interval_cnt = 0
        self.feed_map(layout, target=3) # we use the red mashroom as goal
        self.init_path()
        self.finish = False

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
        closest_distance = 99999
        node = None
        while frontier_queue:
            # initial setup
            priority = frontier_queue.top()
            random_top = np.random.randint(len(frontier_queue[priority]))
            raw_frontier = frontier_queue[priority][random_top]
            frontier = self.decode_state(raw_frontier)
            # print frontier[0:2, 0], cost[raw_frontier]
            self.sim.mario.state = frontier
            del frontier_queue[priority][random_top]
            if not frontier_queue[priority]:
                del frontier_queue[priority]

            # expand frontier
            for i in range(4):
                next_cost = cost[raw_frontier]
                prev_state = self.sim.mario.state
                self.sim.run(action=i, printable=False)
                next_cost += l2_distance(prev_state[0:2, 0], self.sim.mario.state[0:2, 0])

                # upsample runs
                for j in range(self.interval - 1):
                    prev_state = self.sim.mario.state
                    self.sim.run(action=0, printable=False)
                    next_cost += l2_distance(prev_state[0:2, 0], self.sim.mario.state[0:2, 0])

                next_state = self.sim.mario.state
                raw_next_state = self.encode_state(next_state)

                # if new state is legal
                if not np.array_equal(next_state, frontier) and next_state[0][0] > 0 and next_state[1][0] > 0 and (
                        raw_next_state not in cost or next_cost < cost[raw_next_state]):
                    cost[raw_next_state] = next_cost
                    path_pre[raw_next_state] = raw_frontier
                    state_action_map[raw_next_state] = i

                    # task end test
                    closest_distance = min(closest_distance, l1_distance(self.end, next_state[0:2, 0]))
                    print i, next_state[0:2, 0], next_cost, closest_distance
                    if closest_distance < 0.5:
                        node = raw_next_state
                        break

                    heuristic = next_cost + l1_distance(self.end, next_state[0:2, 0])
                    if heuristic in frontier_queue:
                        frontier_queue[heuristic].append(raw_next_state)
                    else:
                        frontier_queue[heuristic] = [raw_next_state]


                self.sim.mario.state = frontier

            if closest_distance < 0.5:
                break

        action_path = []
        while node:
            action_path.insert(0, state_action_map[node])
            node = path_pre[node]
        action_path.pop(0)

        self.action_path = action_path
        print action_path
        self.sim.mario.state = self.decode_state(init_state)


    def get_action(self):
        # upsample check
        if self.interval_cnt == self.interval - 1:
            self.interval_cnt = 0
            # path finish check
            if self.action_path:
                return self.action_path.pop(0)
            elif not self.finish:
                state[:, 1] = [0.0, 0.0, 0.0]
                state[:, 2] = [0.0, 0.0, 0.0]
                self.finish = True
                return 0
            else:
                return 0
        else:
            self.interval_cnt += 1
            return 0
