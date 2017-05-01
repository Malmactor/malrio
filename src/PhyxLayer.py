"""Physics abstraction layer for simulating Super Mario physics in Minecraft
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np


def clamp(value, lower_bound, upper_bound):
    return lower_bound if value < lower_bound else (upper_bound if value > upper_bound else value)


def l2_normalize(vec):
    return vec / np.linalg.norm(vec)


def seg_aabb_collision_resolution(box_center, radius, start, direction, padding=(0, 0), config=None):
    """
    :param box_center: Center vector of the box, shape of 2x1
    :param radius: Half length of the box sides, shape of 2x1
    :param start: Start position of the segment, shape of 2x1
    :param direction: Direction vector of the segment from the start position to the end, shape of 2x1
    :param padding: Box padding size along two axes
    :param config: Global configurations
    :return: None if no collision, else a dict with four fields: time, normal, delta, position

    Resolve the collision between a segment and a axis-aligned bounding box. The segment is defined as 
    (start + t * direction)
    """
    dtype = "float16" if config is None else config["dtype"]

    sign_vec = np.sign(direction)

    near_time_vec = (box_center - sign_vec * (radius + padding) - start) / direction
    far_time_vec = (box_center + sign_vec * (radius + padding) - start) / direction

    # The segment bypassed the box
    if near_time_vec[0] > far_time_vec[1] or near_time_vec[1] > far_time_vec[0]:
        return None

    near_time = near_time_vec[0] if near_time_vec[0] > near_time_vec[1] else near_time_vec[1]
    far_time = far_time_vec[0] if far_time_vec[0] < far_time_vec[1] else far_time_vec[1]

    # The box is behind or in front of the segment
    if near_time >= 1 or far_time <= 0:
        return None

    # If the segment starts outside, hit time is the near time. Otherwise, its hit time is 0
    collision = dict()
    collision["time"] = clamp(near_time, 0, 1)
    if near_time_vec[0] > near_time_vec[1]:
        collision["normal"] = np.array([-sign_vec[0], 0], dtype=dtype)
    else:
        collision["normal"] = np.array([0, -sign_vec[1]], dtype=dtype)

    collision["resolved_part"] = collision["time"] * direction
    collision["position"] = start + collision["resolved_part"]

    return collision


class RigidEntity:
    def __init__(self, x=0, y=0, z=0, config=None):
        self.config = config

        self.dtype = "float16" if config is None else config["dtype"]
        self.delta_t = 1.0 if config is None else config["delta_t"]
        self.delta_mat = np.identity(3, self.dtype)
        self.delta_mat[1, 0] = self.delta_t
        self.delta_mat[2, 1] = self.delta_t
        self.delta_mat[2, 0] = self.delta_t ** 2 / 2.0

        self.state = np.zeros([3, 3], dtype=self.dtype)
        self.state[:, 0] = [x, y, z]
        self.prev_state = self.state

    def __str__(self):
        return ' '.join(map(lambda num: str(num), self.state[:, 0]))

    def __getattr__(self, item):
        mapping = {"x": self.state[0, 0], "y": self.state[1, 0], "z": self.state[2, 0]}
        if item in mapping:
            return mapping[item]
        else:
            raise AttributeError("object has no attribute \'{:}\'".format(str(item)))

    def update(self):
        self.prev_state = self.state
        self.state = np.dot(self.state, self.delta_mat)

    def reaction(self, op):
        op(self.state)

    def displacement_difference(self):
        return (self.state - self.prev_state)[:, 1]

    def get_displacement(self):
        return self.state[:, 0]


class CollidableAABB:
    def __init__(self, center, radius, config=None):
        self.config = config

        self.dtype = "float16" if config is None else config["dtype"]
        self.center = center
        self.radius = radius

    def collide(self, collidable_rigid):
        collision = dict()

        velocity = collidable_rigid.displacement_difference[0:2]

        # static collision resolution
        if np.all(velocity == 0):
            collision["position"] = collidable_rigid.get_displacement()

