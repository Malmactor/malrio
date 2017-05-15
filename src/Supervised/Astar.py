"""
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


import numpy as np
import pqdict


def get_start_end(maze):
    r, c = maze.shape
    start = np.argwhere(maze == 3).flatten()
    end = np.argwhere(maze == 4).flatten()
    return tuple(start), tuple(end)


def l1_distance(a, b):
    return np.sum(np.abs(a - np.array(b)))


def solver(maze):
    r, c = maze.shape
    start, end = get_start_end(maze)
    directions = [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1])]
    path = []

    path_pre = {start: None}
    cost = {start: 0}
    frontier_queue = pqdict.minpq({0: [start]})

    while frontier_queue:
        priority = frontier_queue.top()
        frontier = frontier_queue[priority][0]
        del frontier_queue[priority][0]
        if not frontier_queue[priority]:
            del frontier_queue[priority]

        if frontier == end:
            break

        for dir_neighbor in directions:
            next_node = tuple(frontier + dir_neighbor)
            next_cost = cost[frontier] + 1
            if maze[next_node] in [0, 3, 4] and (next_node not in cost or next_cost < cost[next_node]):
                cost[next_node] = next_cost
                path_pre[next_node] = frontier
                heuristic = next_cost + l1_distance(next_node, end)
                # print(next_node)
                if heuristic in frontier_queue:
                    frontier_queue[heuristic].append(next_node)
                else:
                    frontier_queue[heuristic] = [next_node]

    node = end
    while node is not None:
        path.insert(0, node)
        node = path_pre[node]
    return path