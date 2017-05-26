"""Heuristic search for generating action labels
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


import copy
import itertools
import numpy as np
import pqdict


def l1_distance(a, b):
    return np.sum(np.abs(a - np.array(b)))


def l2_distance(a, b):
    if not isinstance(a, np.ndarray) and not isinstance(b, np.ndarray):
        a = np.array(a)
    return np.linalg.norm(a-b)


def heuristic(pos, target):
    return l1_distance(pos, target)


def encode_state(simulation):
    return tuple(simulation.mario.state.flatten())


def decode_state(encoding, simulation):
    dynamics = np.array(encoding).reshape((3, 3))
    simulation.mario.state = dynamics
    return simulation


def get_state_pos(encoding):
    if isinstance(encoding, tuple):
        return np.array(encoding).reshape((3, 3))[:, 0]
    else:
        return encoding.mario.state[:, 0]


def in_bound(state, bound):
    minx, miny, maxx, maxy = bound
    x, y = state[0:2]

    return x >= minx and y >= miny and x <= maxx and y <= maxy


def a_star(layout, simulation, init_pos, end_pos, actions, interval=5, config=None):
    """
    A* search for path-finding
    :param layout: 2D numpy array layout
    :param simulation: Physics simulation object
    :param init_pos: 3D vector of the initial position
    :param end_pos: 3D vector of the target position for search
    :param actions: Possible actions
    :param interval: Frame interval between two actions
    :return: Action sequence list
    """
    epsilon = 0.001 if config is None or "epsilon" not in config else config["epsilon"]
    empty_action = "remains" if config is None or "empty_action" not in config else config["empty_action"]

    bound = -1, -1, layout.shape[0], layout.shape[1]

    simulation.mario.state[0:3, 0] = init_pos
    init_state = encode_state(simulation)
    end_state = None

    state_pre = {init_state: None}
    state_preaction_map = {}
    cost = {init_state: 0}
    reversed_action_path = []

    frontier_queue = pqdict.minpq({init_state: heuristic(get_state_pos(init_state), end_pos)})

    expansion = 0
    greatest_x = 0
    max_q = l2_distance(init_pos, end_pos) * 10
    pruned_num = 0

    while frontier_queue and not end_state:

        frontier = frontier_queue.pop()
        expansion += 1

        # Expand frontier
        for act in actions:
            simulation = decode_state(frontier, simulation)
            simulation.advance_frame(act)

            next_cost = l2_distance(get_state_pos(frontier), get_state_pos(simulation)) + cost[frontier] + 1

            # Downsample actions
            for i in range(interval - 1):
                mid_state = encode_state(simulation)
                simulation.advance_frame(empty_action)
                next_cost += l2_distance(get_state_pos(mid_state), get_state_pos(simulation))

            next_state = encode_state(simulation)

            if in_bound(next_state, bound) and (next_state not in cost or next_cost < cost[next_state]):

                cost[next_state] = next_cost
                state_pre[next_state] = frontier
                state_preaction_map[next_state] = act

                h = heuristic(get_state_pos(next_state), end_pos) + next_cost
                if h < max_q:
                    frontier_queue[next_state] = h
                else:
                    pruned_num += 1
                    print pruned_num

                # Reach the end and exit
                if l1_distance(get_state_pos(next_state), end_pos) <= 0.5:
                    end_state = next_state
                    break

    # No solution found
    if not end_state:
        return []

    # Generate action sequences
    node = end_state
    while node in state_preaction_map:
        reversed_action_path.extend(itertools.repeat(empty_action, interval - 1))

        reversed_action_path.append(state_preaction_map[node])

        node = state_pre[node]

    return list(reversed(reversed_action_path))
