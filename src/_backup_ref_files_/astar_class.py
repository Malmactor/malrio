import sys
import os
sys.path.append(os.path.abspath('../'))

import numpy as np
import pqdict
from SuperMarioBros.simulation import MarioSimulation
from SuperMarioBros.layout_loader import layout_toxml, layout_fromdefault


__author__ = "Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


def l1_distance(a, b):
    return np.sum(np.abs(a - np.array(b)))


def l2_distance(a, b):
    return np.linalg.norm(a-b)


def pad_layout(layout):
    return np.pad(layout, (1, 1), 'constant', constant_values=1)


class Astar:
    def __init__(self):
        pass

    def feed_map(self, layout, interval=5, target=3):
        self.interval = interval # upsampling interval
        self.layout = pad_layout(layout) # map
        self.target = target # end point
        self.start = np.array([1, 3])
        self.end = np.argwhere(self.layout == target).flatten()
        self.sim = MarioSimulation(layout, {"dtype": "float16"})

    def encode_state(self, state):
        return tuple(state.flatten())

    def decode_state(self, state):
        return np.array(state).reshape((3, 3))
        #return np.fromstring(state[1:-1], dtype="float16", sep=' ').reshape((3, 3))

    def get_path(self):
        print self.end
        r, c = self.layout.shape
        init_state = self.encode_state(self.sim.mario.state)

        # we use path to record states, and state_action_map to map state to action
        path = []
        state_action_map = {init_state: None}
        # state dict for previous state
        path_pre = {init_state: None}
        # cost to get this state, in terms of time (moves)
        cost = {init_state: 0}

        frontier_queue = pqdict.minpq({init_state: 0})

        # astar search
        closest_distance = 99999999
        expansion = 0
        node = None
        solved = False
        while frontier_queue:

            # get top
            raw_frontier = frontier_queue.pop()
            frontier = self.decode_state(raw_frontier)
            self.sim.mario.state = frontier
            expansion += 1

            # expand frontier
            for i in ["remains", "left_jump", "right_jump", "left_nojump", "right_nojump", "nolr_jump"]:
                next_cost = cost[raw_frontier]
                prev_state = self.sim.mario.state
                self.sim.advance_frame(action=i)
                next_cost += l2_distance(prev_state[0:2, 0], self.sim.mario.state[0:2, 0])

                # upsample runs
                for j in range(self.interval - 1):
                    prev_state = self.sim.mario.state
                    self.sim.advance_frame(action="remains")
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
                    distance_to_end = l1_distance(self.end, next_state[0:2, 0])
                    closest_distance = min(closest_distance, distance_to_end)
                    # print i, next_state[0:2, 0], next_cost, closest_distance
                    if closest_distance < 0.5:
                        node = raw_next_state
                        solved = True
                        break

                    heuristic = next_cost + distance_to_end
                    frontier_queue[raw_next_state] = heuristic


                self.sim.mario.state = frontier

            if closest_distance < 0.5:
                solved = True
                break


        action_path = []

        if solved:
            while node:
                for i in range(self.interval-1):
                    action_path.insert(0, "remains")
                action_path.insert(0, state_action_map[node])
                node = path_pre[node]
            for i in range(self.interval):
                action_path.pop(0)

        print expansion
        return action_path


if __name__ == "__main__":
    astar = Astar()
    astar.feed_map(layout=layout_fromdefault(), interval=5, target=3)
    print astar.get_path()
