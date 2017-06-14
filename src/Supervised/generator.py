"""Randomized Prim's Minimum Spanning Tree Algorithm for Maze Generation."""


__author__ = "Chang Gao, Liyan Chen, Bruce Tan"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import sys
import numpy as np
from random import randint


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
    # maze_c = 160
    # maze_r = 15
    transpose = True if config is None or "layout_inv" not in config else config["layout_inv"]
    init_pos = (1, 3)
    end_pos = (maze_c-1, 3)
    lava_len = 7
    maze = None
    maze_blk = np.zeros((maze_c,1))

    # build maze and initialize with only walls and lavas
    maze = np.zeros((maze_r, maze_c))
    maze[-2:] = np.ones((1, maze_c))
    # maze[-2:] = np.random.randint(2, size=(1, maze_c))+1
    maze[maze_r-2][0] = 1
    maze[maze_r-2][maze_c-1] = 1
    maze[maze_r-3][maze_c-1] = 3


    # generate lavas

    goon = True
    i = 3
    while i < maze_c-2:
        raml = 0
        if raml == 0:
            lava_len = randint(2,14)
            maze[-2:, i:i+lava_len] = 2
            j = i + randint(0,2)
            while(j < i+lava_len):
                # print(j)
                ra = np.random.randint(3)
                ra2 = randint(1,3)
                if(j+ra2 > i+lava_len ):
                    break
                maze[(maze_r - 4)-ra, j:j+ra2] = 1
                # print(np.copy(np.transpose(maze[::-1])))
                j += ra2 + randint(2,4)
            i += lava_len + randint(2,4)
        i += 1

    # generate blocks from ground
    maxb = min(int(maze_r/3), 4) # from 1/3 lower part
    if maxb > 1:
        i = 3
        while i < maze_c-10 :
            if maze[maze_r-2][i] != 2 and maze[maze_r-2][i+1] != 2 :
                if randint(0,1) == 0:
                    ramh = np.random.randint(maxb)
                    if ramh > 0:
                        maze[-2-ramh:-2, i:i+2] = 1
                        # i += 1
                else:
                    height = randint(4,6)
                    for j in range(i,i+height):
                        if(j == i+height-1):
                            k = j-i 
                        elif(j == i):
                            k = height -1
                        else:
                            k =  (j - i)
                        maze[-2-k:-2,j] = 1
                        maze[maze_r-2:maze_r,j] = 1
                    i+= height
            i += 1

    #mountain
    # i=3
    # while i < maze_c-14:
    #     if randint(0,10) == 0 and maze[maze_r-2][i] != 2:
    #         height = randint(4,6)
    #         for j in range(i,i+height):
    #             if(j == i+height-1):
    #                 k = j-i + 1
    #             else:
    #                 k =  (j - i)
    #             maze[-2-k:-2,j] = 1
    #             maze[maze_r-2:maze_r,j] = 1
    #         i+= height

    #     i+=1
    

    # generate blocks in air
    # maxb = int(maze_r/2) # from 1/2 lower part
    # i = 3
    # while i < maze_c-2:
    #     raml = np.random.randint(1+max(int(maze_c/8), 8))
    #     ramh = np.random.randint(maxb)
    #     if ramh > 0:
    #         maze[ramh, i:i+raml] = 1
    #         i += raml + 3
    #     i += 1

    np.set_printoptions(threshold=np.nan)
    
    print maze
    if transpose:
        maze = np.copy(np.transpose(maze[::-1]))
    
    return maze



if __name__ == '__main__':
    print make_simple_layout(None)
