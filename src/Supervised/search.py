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
    return np.linalg.norm(a-b)


def heuristic(state, target):
    l2_distance(state[0:2], target)


def encode_state(simulation):
    return tuple(simulation.mario.state.flatten())


def decode_state(encoding, simulation):
    dynamics = np.array(encoding).reshape((3, 3))
    simulation.mario.state = dynamics
    return simulation


def in_bound(state, bound):
    minx, miny, maxx, maxy = bound
    x, y = state[0:2, 0]

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

    bound = -2, -2, layout.shape[0], layout.shape[1]

    simulation.mario.state[0:2, 0] = init_pos
    init_state = encode_state(simulation)
    end_state = None

    state_pre = {init_state: None}
    state_preaction_map = {}
    cost = {init_state: 0}
    reversed_action_path = []

    frontier_queue = pqdict.minpq({init_state: heuristic(init_state, end_pos)})

    while frontier_queue:

        frontier = frontier_queue.pop()

        # Reach the end and exit
        if l2_distance(frontier[:, 0], end_pos) < epsilon:
            end_state = frontier
            break

        # Expand frontier
        for act in actions:
            simulation.mario.state = decode_state(frontier)
            simulation.run(act)

            # Downsample actions
            for i in range(interval - 1):
                simulation.run(empty_action)

            next_state = encode_state(simulation)

            next_cost = l2_distance(frontier[:, 0], next_state[:, 0]) + cost[frontier]

            if in_bound(next_state, bound) and (next_state not in cost or next_cost < cost[next_state]):

                cost[next_state] = next_cost
                state_pre[next_state] = frontier
                state_preaction_map[next_state] = act

                h = heuristic(next_state, end_pos) + next_cost
                frontier_queue[next_state] = h

    # No solution found
    if not end_state:
        return []

    # Generate action sequences
    node = end_state
    while node:
        reversed_action_path.extend(itertools.repeat(empty_action, interval - 1))
        reversed_action_path.append(state_preaction_map[end_state])

        node = state_pre[node]

    return reversed(reversed_action_path)
