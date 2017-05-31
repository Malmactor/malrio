"""Randomized Prim's Minimum Spanning Tree Algorithm for Maze Generation."""


__author__ = "Chang Gao, Liyan Chen, Bruce Tan"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import sys
import numpy as np


def make_simple_layout(config):
    """
    Make a simple Mario Map
    :param config: Global configuration{
        :param layout_area: layout size (x-axis, y-axis)
        :param layout_inv: if transpose the map or not, default is True
    }
    """
    maze_c = config["layout_area"][0]
    maze_r = config["layout_area"][1]
    transpose = True if config is None or "layout_inv" not in config else config["layout_inv"]
    init_pos = (1, 3)
    end_pos = (maze_c-1, 3)
    maze = None

    # build maze and initialize with only walls and lavas
    maze = np.zeros((maze_r, maze_c))
    maze[-2:] = np.ones((1, maze_c))
    # maze[-2:] = np.random.randint(2, size=(1, maze_c))+1
    maze[maze_r-2][0] = 1
    maze[maze_r-2][maze_c-1] = 1
    maze[maze_r-3][maze_c-1] = 3


    # generate lavas
    i = 2
    while i < maze_c-2:
        raml = np.random.randint(10)
        if raml == 0:
            maze[-2:, i:i+2] = 2
            i += 2
        i += 1

    # generate blocks from ground
    maxb = min(int(maze_r/3), 4) # from 1/3 lower part
    if maxb > 1:
        i = 2
        while i < maze_c-4 :
            if maze[maze_r-2][i] != 2 and maze[maze_r-2][i+1] != 2 :
                ramh = np.random.randint(maxb)
                if ramh > 0:
                    maze[-2-ramh:-2, i:i+2] = 1
                    i += 1
            i += 1


    # generate blocks in air
    maxb = int(maze_r/2) # from 1/2 lower part
    i = 2
    while i < maze_c-2:
        raml = np.random.randint(1+max(int(maze_c/8), 8))
        ramh = np.random.randint(maxb)
        if ramh > 0:
            maze[ramh, i:i+raml] = 1
            i += raml + 3
        i += 1

    if transpose:
        maze = np.copy(np.transpose(maze[::-1]))
    return maze


### layout classes ###
# class Point:
#
#     def __init__(self, r, c, parent=None):
#         self.r = r
#         self.c = c
#         self.parent = parent
#
#     def opposite(self):
#         if self.r > self.parent.r:
#             return Point(self.r+1, self.c, self)
#         if self.r < self.parent.r:
#             return Point(self.r-1, self.c, self)
#         if self.c > self.parent.c:
#             return Point(self.r, self.c+1, self)
#         if self.c < self.parent.c:
#             return Point(self.r, self.c-1, self)
#         return None
#
#
# class Prim:
#     def __init__(self, config):
#         """
#         Note: the output map may not have size (r, c) due to padding and scaling
#         r: num of rows
#         c: num of colomns
#         n: map scaling factor
#         transpose: if need transpose for Malrio
#         """
#         self.r = config["r"]
#         self.c = config["c"]
#         self.n = config["n"]
#         self.transpose = config["transpose"]
#         self.lava = config["lava"]
#         self.init_pos = self.end_pos = (1, 3)
#
#     def generate(self):
#         self.maze = None
#         maze_r = self.r
#         maze_c = self.c
#         n = self.n
#
#         # build maze and initialize with only walls and lavas
#         maze = np.ones((maze_r, maze_c))
#
#         # set start point at (0, 2) in final layout
#         start_x, start_y = maze_r-1, 0
#         maze[start_x][start_y] = 0
#         start = Point(start_x, start_y)
#
#         # iterate through direct neighbors of node
#         frontier = list()
#         for x in range(-1, 2):
#             for y in range(-1, 2):
#                 if x*y == 0 and x+y != 0:
#                     if start.r+x >= 0 and start.r+x < maze_r and start.c+y >= 0 and start.c+y < maze_c:
#                         frontier.append(Point(start.r+x, start.c+y, start))
#
#         last = None
#         while frontier:
#             # pick current node at random
#             current = frontier.pop(np.random.random_integers(len(frontier))-1)
#             opposite = current.opposite()
#             # if both node and its opposite are walls
#             if opposite.r >= 0 and opposite.r < maze_r and opposite.c >= 0 and opposite.c < maze_c:
#                 if maze[current.r][current.c] in [1, 2] and maze[opposite.r][opposite.c] in [1, 2]:
#                     # open path between the nodes
#                     maze[current.r][current.c] = 0
#                     maze[opposite.r][opposite.c] = 0
#
#                     # store last node in order to mark it later
#                     last = opposite
#                     # iterate through direct neighbors of node, same as earlier
#                     for x in range(-1, 2):
#                         for y in range(-1, 2):
#                             if x*y == 0 and x+y != 0:
#                                 if opposite.r+x >= 0 and opposite.r+x < maze_r and opposite.c+y >= 0 and opposite.c+y < maze_c:
#                                     frontier.append(Point(opposite.r+x, opposite.c+y, opposite))
#
#         # if algorithm has resolved, mark end node
#         if last:
#             # scale the map
#             maze = maze.repeat(n,axis=0).repeat(n,axis=1)
#             maze[last.r*n][last.c*n] = 3
#             # add ground
#             if self.lava:
#                 ground = np.ones((1, maze_c*n))
#             else:
#                 ground = np.random.randint(2, size=(1, maze_c*n))+1
#             ground[0][0] = 1
#             maze = np.vstack([maze, ground, ground])
#             end_pos = list(reversed(np.where(maze==3)))
#             self.end_pos = (end_pos[0][0], self.n*maze_r + 1 - end_pos[1][0])
#             # transpose
#             if self.transpose:
#                 maze = np.copy(np.transpose(maze[::-1]))
#             self.maze = maze
#         else:
#             self.maze = None
#
#
# class RandMap:
#     def __init__(self, config):
#         """
#         Note: the output map may not have size (r, c) due to padding and scaling
#         r: num of rows
#         c: num of colomns
#         n: map scaling factor
#         transpose: if need transpose for Malrio
#         """
#         self.r = config["r"]
#         self.c = config["c"]
#         self.transpose = config["transpose"]
#         self.init_pos = (1, 3)
#         self.end_pos = (self.c-1, 3)
#
#     def generate(self):
#         self.maze = None
#         maze_r = self.r
#         maze_c = self.c
#
#         # build maze and initialize with only walls and lavas
#         maze = np.zeros((maze_r, maze_c))
#         maze[-2:] = np.ones((1, maze_c))
#         # maze[-2:] = np.random.randint(2, size=(1, maze_c))+1
#         maze[maze_r-2][0] = 1
#         maze[maze_r-2][maze_c-1] = 1
#         maze[maze_r-3][maze_c-1] = 3
#
#
#         # generate lavas
#         i = 2
#         while i < maze_c-2:
#             raml = np.random.randint(10)
#             if raml == 0:
#                 maze[-2:, i:i+2] = 2
#                 i += 2
#             i += 1
#
#         # generate blocks from ground
#         maxb = min(int(maze_r/3), 4) # from 1/3 lower part
#         if maxb > 1:
#             i = 2
#             while i < maze_c-4 :
#                 if maze[maze_r-2][i] != 2 and maze[maze_r-2][i+1] != 2 :
#                     ramh = np.random.randint(maxb)
#                     if ramh > 0:
#                         maze[-2-ramh:-2, i:i+2] = 1
#                         i += 1
#                 i += 1
#
#
#         # generate blocks in air
#         maxb = int(maze_r/2) # from 1/2 lower part
#         i = 2
#         while i < maze_c-2:
#             raml = np.random.randint(1+max(int(maze_c/8), 8))
#             ramh = np.random.randint(maxb)
#             if ramh > 0:
#                 maze[ramh, i:i+raml] = 1
#                 i += raml + 3
#             i += 1
#
#         if self.transpose:
#             maze = np.copy(np.transpose(maze[::-1]))
#         self.maze = maze
#         # print maze


if __name__ == '__main__':
    print make_simple_layout()
