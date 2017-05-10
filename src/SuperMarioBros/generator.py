"""Randomized Prim's Minimum Spanning Tree Algorithm for Maze Generation."""


from __future__ import print_function
import sys
import numpy as np


class Point:

    def __init__(self, r, c, parent=None):
        self.r = r
        self.c = c
        self.parent = parent

    def opposite(self):
        if self.r > self.parent.r:
            return Point(self.r+1, self.c, self)
        if self.r < self.parent.r:
            return Point(self.r-1, self.c, self)
        if self.c > self.parent.c:
            return Point(self.r, self.c+1, self)
        if self.c < self.parent.c:
            return Point(self.r, self.c-1, self)
        return None


class Prim:
    def __init__(self, r, c, n, transpose):
        """
        Note:
            1. the output map may not have size (r, c) due to padding and scaling
            2. generate() may return Null if unsovable
            3. You need to set transpose = True for Malrio
        r: num of rows
        c: num of colomns
        n: map scaling factor
        transpose: if need transpose for Malrio
        """
        self.r = r
        self.c = c
        self.n = n # scale factor
        self.transpose = transpose

    def generate(self):
        """
        0 - air
        1 - block
        2 - lava
        3 - end point
        """

        maze_r = self.r
        maze_c = self.c
        n = self.n

        # build maze and initialize with only walls and lavas
        maze = np.random.randint(2, size=(maze_r, maze_c))+1

        # set start point at (0, 2) in final layout
        start_x, start_y = maze_r-1, 0
        maze[start_x][start_y] = 0
        start = Point(start_x, start_y)

        # iterate through direct neighbors of node
        frontier = list()
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x*y == 0 and x+y != 0:
                    if start.r+x >= 0 and start.r+x < maze_r and start.c+y >= 0 and start.c+y < maze_c:
                        frontier.append(Point(start.r+x, start.c+y, start))

        last = None
        while frontier:
            # pick current node at random
            current = frontier.pop(np.random.random_integers(len(frontier))-1)
            opposite = current.opposite()
            # if both node and its opposite are walls
            if opposite.r >= 0 and opposite.r < maze_r and opposite.c >= 0 and opposite.c < maze_c:
                if maze[current.r][current.c] in [1, 2] and maze[opposite.r][opposite.c] in [1, 2]:
                    # open path between the nodes
                    maze[current.r][current.c] = 0
                    maze[opposite.r][opposite.c] = 0

                    # store last node in order to mark it later
                    last = opposite
                    # iterate through direct neighbors of node, same as earlier
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if x*y == 0 and x+y != 0:
                                if opposite.r+x >= 0 and opposite.r+x < maze_r and opposite.c+y >= 0 and opposite.c+y < maze_c:
                                    frontier.append(Point(opposite.r+x, opposite.c+y, opposite))

        # if algorithm has resolved, mark end node
        if last:
            # scale the map
            maze = maze.repeat(n,axis=0).repeat(n,axis=1)
            maze[last.r*n][last.c*n] = 3
            # add ground
            ground = np.random.randint(2, size=(1, maze_c*n))+1
            ground[0][0] = 1
            maze = np.vstack([maze, ground, ground])
            # transpose
            if self.transpose:
                maze = np.copy(np.transpose(maze)[::-1])
            self.maze = maze
        else:
            self.maze = None

        return self.maze


def print_maze(maze):
    if maze is not None:
        r, c = maze.shape
        for x in range(r):
            for y in range(c):
                print(maze[x][y], end='')
            print('', end='\n')
    else:
        print('unsovable')


if __name__ == '__main__':
    p = Prim(5, 18, 1, transpose=False)
    p.generate()
    print_maze(p.maze)
