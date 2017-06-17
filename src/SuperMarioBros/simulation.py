"""Running world simulations of Super Mario Bros
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import copy
import itertools as it

from momentum_handler import *
from simulatables import *


def layout_tobb(layout, config=None):
    maxx, maxy = layout.shape

    id2block = {0: 'air', 1: 'brick_block', 2: 'lava',
                3: 'red_mushroom'} if config is None or "id2block" not in config else config["id2block"]
    block2id = dict(map(lambda item: (item[1], item[0]), id2block.items()))
    block_radius = (0.5, 0.5) if config is None or "block_radius" not in config else config["block_radius"]
    pos2bb = {}

    for x in range(maxx):
        for y in range(maxy):
            if layout[x, y] in (block2id['brick_block'], block2id['lava']):
                pos2bb[(x, y)] = CollidableAABB((x, y), block_radius, config)

    return pos2bb


def collision_proposal(mario, pos2bb, config=None,xdist=2):
    """
    Propose potential collision box around mario
    :param mario: CollidableRigid instance
    :param pos2bb: Position-to-boundingbox mapping
    :param config: Global configuration
    :return: List of potential collision boxes
    """
    minx, miny, maxx, maxy = -xdist, -1, xdist, 1

    center = mario.get_center()

    return list(map(lambda pos: pos2bb[pos],
                    filter(lambda pos: pos in pos2bb,
                           map(lambda d: tuple((center + d).astype("int")),
                               it.product(xrange(minx, maxx), xrange(miny, maxy))))))


def hit_edge_reaction(collision):
    """
    Give corresponding handler to each edge hit.
    Normal line indexed directions: 0: right, 1: left, 2: up, 3: down
    :param collision: Collision dict
    :return: Hit handler
    """
    directions = np.array([[1.0, -1.0, 0.0, 0.0], [0.0, 0.0, 1.0, -1.0]])
    edge2action = {0: hit_sides, 1: hit_sides, 2: hit_ground, 3: hit_ceiling}

    return edge2action[np.argmax(np.dot(collision['hit']['normal'], directions))]


def compensate_gravity(mario, surrounding_bb, config=None):
    # If mario has gravity, it doesn't need compensation
    if abs(mario.state[1, 2]) < config["greater_eps"]:
        # Create a hypothesis of ground hitting test
        hypothetical_mario = copy.deepcopy(mario)
        hypothetical_mario.state[1, 2] = -0.05
        hypothetical_mario.state[1, 1] = -0.05
        hypothetical_mario.update()

        return any(map(lambda bb: bb.collide(hypothetical_mario)['hit'] is not None, surrounding_bb))


class MarioSimulation:
    def __init__(self, layout, config=None):
        """
        Instantiate physics engine objects
        :param layout: Two-dimensional numpy array layout
        :param config: Global configuration
        """
            
        self.layout = layout
        self.config = config

        init_pos = np.array([2, 3, 0]) if config is None or "init_pos" not in config else config["init_pos"]
        mario_bb = np.array([0.5, 1]) if config is None or "mario_bb" not in config else config["mario_bb"]

        self.mario = CollidableRigid(init_pos, mario_bb, config)
        self.brick_bb = layout_tobb(layout, config)

        # Start with gravity
        self.mario.reaction(give_gravity)

    def advance_frame(self, action):
        """
        Update physics engine object states for next frame
        :param action: agent action for current frame
        :return: None
        """
        if(self.mario.state[0][0] <= 0.5):
            return
        # Advance a time step
        self.mario.update()

        # Locate blocks for collision detections
        bb_to_check = collision_proposal(self.mario, self.brick_bb, self.config)
        gravity = compensate_gravity(self.mario, bb_to_check, self.config)

        if not bb_to_check or gravity:
            self.mario.reaction(give_gravity)
        
        # Resolve collisions
        collisions = list(filter(lambda pair: pair[1]['hit'] is not None,
                                 map(lambda bb: (bb.get_center(), bb.collide(self.mario)), bb_to_check)))

        if collisions:
            closest_collision = min(collisions, key=lambda pair: pair[1]['hit']['time'])

            self.mario.reaction(collision_resolved, closest_collision[1]["hit"]["delta"])
            # self.mario.reaction(collision_resolved, closest_collision[1]["position"])

            # Process momentum change
            self.mario.reaction(hit_edge_reaction(closest_collision[1]))

        # Grab an action from input and simulate the force
        print(action)
        self.mario.reaction(action_mapping[action])

        if collisions:
            return closest_collision

    def get_renderable(self):
        return self.mario
    
    def next_none_time(self, ori):
        if(self.mario.state[0][0] <= 0.5):
            return ori
        ll = []
        for bb in self.brick_bb:
            if bb[0] == int(self.mario.state[0][0]):
                if bb[1] < int(self.mario.state[1][0]):
                    ll.append(bb)
        ll = sorted(ll,key=lambda x:x[1],reverse=True)
        block_below = ll[0]
        print self.mario.state, block_below
        if self.mario.state[1][0] - block_below[1] > 1.05:
                print "self", self.mario.state, block_below
                print "END"
                return 0
        return ori
            
