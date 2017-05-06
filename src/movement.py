import time
import json
import numpy as np
import pqdict

from SuperMarioBros.simulation import MarioSimulation

class Actor:
    def __init__(self, host, layout):
        self.host = host
        self.world = host.getWorldState()
        self.sim = MarioSimulation(layout, {"dtype": "float16"})

    def get_action(self):
        """Get next action.
        ret: {0: freeze, 1: left, 2: right, 3: jump}
        """
        #### TODO ####
        # if numpy.random.randint(5) == 0:
        #     return 2
        return 2

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
        note: the initial position is (0, 2) from the feet, (0, 3) from center
              in our solver, the initial position is (1, 3) since we pad the map with a wall box
        """
        self.layout = pad_layout(layout) # map
        self.target = target # end point
        self.start = np.array([1, 3])
        self.end = np.argwhere(self.layout == target).flatten()

    def current_state(self):
        return str(self.sim.mario.state)

    def init_path(self):
        r, c = self.layout.shape

        # directions = [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1])]
        init_state = self.current_state()
        path = []
        path_pre = {init_state: None}
        cost = {init_state: 0}
        frontier_queue = pqdict.minpq({0: [init_state]})

        # TODO: use actoin (base on state matrix) + domain (possible induced state matrix)
        # instead of directions. For each loop in the heap, pop top state, calc all possible
        # induced state, then push them into the heap. Notice that final position could be
        # a range (rough position), since we use float.


        # while frontier_queue:
        #     priority = frontier_queue.top()
        #     frontier = frontier_queue[priority][0]
        #     del frontier_queue[priority][0]
        #     if not frontier_queue[priority]:
        #         del frontier_queue[priority]
        #
        #     if frontier == self.end:
        #         break

        # while frontier_queue:
        #     priority = frontier_queue.top()
        #     frontier = frontier_queue[priority][0]
        #     del frontier_queue[priority][0]
        #     if not frontier_queue[priority]:
        #         del frontier_queue[priority]
        #
        #     if frontier == self.end:
        #         break
        #
        #     for dir_neighbor in directions:
        #         next_node = tuple(frontier + dir_neighbor)
        #         next_cost = cost[frontier] + 1
        #         if self.layout[next_node] in [0, 3, 4] and (next_node not in cost or next_cost < cost[next_node]):
        #             cost[next_node] = next_cost
        #             path_pre[next_node] = frontier
        #             heuristic = next_cost + l1_distance(next_node, self.end)
        #             # print(next_node)
        #             if heuristic in frontier_queue:
        #                 frontier_queue[heuristic].append(next_node)
        #             else:
        #                 frontier_queue[heuristic] = [next_node]
        #
        # node = self.end
        # while node is not None:
        #     path.insert(0, (node[0]-1, node[1]-1)) # cancel the padding offset
        #     node = path_pre[node]
        # return path

    def get_action(self):
        # TODO: read from path
        return 3
