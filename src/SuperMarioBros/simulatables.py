"""Physics abstraction layer components for simulating Super Mario physics in Minecraft
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np


def clamp(value, lower_bound, upper_bound):
    return lower_bound if value < lower_bound else (upper_bound if value > upper_bound else value)


def l2_normalize(vec):
    return vec / np.linalg.norm(vec)


def resolve_collision(collidable_rigid, collision):
    collidable_rigid.state[0:2, 0] -= collision['hit']['delta']


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
    dtype = "float16" if config is None or "dtype" not in config else config["dtype"]
    epsilon = 0.001 if config is None or "epsilon" not in config else config["smaller_eps"]

    if np.any(np.abs(direction) == 0.0):
        norm = direction + epsilon
    else:
        norm = direction

    sign_vec = np.sign(norm)

    near_time_vec = (box_center - sign_vec * (radius + padding) - start) / norm
    far_time_vec = (box_center + sign_vec * (radius + padding) - start) / norm

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
    collision["time"] = clamp(near_time, 0, 1) - config["greater_eps"]
    if near_time_vec[0] > near_time_vec[1]:
        collision["normal"] = np.array([-sign_vec[0], 0], dtype=dtype)
    else:
        collision["normal"] = np.array([0, -sign_vec[1]], dtype=dtype)

    collision["delta"] = (1 - collision["time"]) * norm
    collision["position"] = start + collision["time"] * norm

    return collision


class RigidEntity:
    def __init__(self, center, config=None):
        # A side note on matrix representations for rigid body dynamics:
        # Rows represent spatial dimensions (x, y, z)
        # Columns represent states of Newtonian mechanical dynamics (x, v_x, a_x)
        # Each update follows: x' = x + v_x * dt + a_x * dt ^ 2 / 2, v_x' = v_x + a_x * dt
        self.config = config

        self.dtype = "float16" if config is None or "dtype" not in config else config["dtype"]
        self.delta_t = 1.0 if config is None or "delta_t" not in config else config["delta_t"]
        self.delta_mat = np.identity(3, self.dtype)
        self.delta_mat[1, 0] = self.delta_t
        self.delta_mat[2, 1] = self.delta_t
        self.delta_mat[2, 0] = self.delta_t ** 2 / 2.0

        self.state = np.zeros([3, 3], dtype=self.dtype)
        self.state[:, 0] = center
        self.prev_state = np.copy(self.state)

    def __str__(self):
        return ' '.join(map(lambda num: str(num), self.state[:, 0]))

    def update(self):
        self.prev_state = np.copy(self.state)
        self.state = np.dot(self.state, self.delta_mat)

    def reaction(self, op, *args):
        op(self.state, *args)

    def displacement_difference(self):
        return (self.state - self.prev_state)[:, 0]

    def get_displacement(self):
        return self.state[:, 0]


class CollidableAABB:
    def __init__(self, center, radius, config=None):
        self.config = config

        self.dtype = "float16" if config is None or "dtype" not in config else config["dtype"]
        self.epsilon = 0.001 if config is None or "epsilon" not in config else config["epsilon"]
        self.static_center = center[0:2]
        self.radius = radius[0:2]

    def __str__(self):
        return ' '.join(map(lambda num: str(num), self.static_center[:, 0]))

    def get_center(self):
        return self.static_center

    def static_collide(self, collidable):
        d = collidable.get_center() - self.get_center()
        p = collidable.radius + self.radius - np.abs(d)

        if np.any(p <= 0):
            return None

        collision = dict()

        collision['hit'] = {"time": -1}

        if p[0] < p[1]:
            sign_vec = np.sign(d)
            collision["delta"] = -np.array([p[0] * sign_vec[0], 0], dtype=self.dtype)
            collision["normal"] = np.array([sign_vec[0], 0], dtype=self.dtype)
            collision["position"] = np.array([self.get_center()[0] + self.radius[0] * sign_vec[0],
                                              collidable.get_center()[1]], dtype=self.dtype)
        else:
            sign_vec = np.sign(d)
            collision["delta"] = -np.array([0, p[1] * sign_vec[1]], dtype=self.dtype)
            collision["normal"] = np.array([0, sign_vec[1]], dtype=self.dtype)
            collision["position"] = np.array([collidable.get_center()[0],
                                              self.get_center()[1] + self.radius[1] * sign_vec[1]], dtype=self.dtype)

        return collision

    def collide(self, collidable_rigid):
        collision = dict()

        velocity = collidable_rigid.displacement_difference()[0:2]

        # static collision resolution
        if np.all(np.abs(velocity) <= self.epsilon):
            collision["position"] = collidable_rigid.get_center()
            collision["hit"] = self.static_collide(collidable_rigid)

            if collision["hit"] is None:
                collision["time"] = 1
            else:
                collision["time"] = -self.config["greater_eps"]
                collision["hit"]["time"] = -1

        # call into segment resolution for sweep resolution
        else:
            collision["hit"] = seg_aabb_collision_resolution(self.get_center(), self.radius,
                                                             collidable_rigid.get_center(), velocity,
                                                             collidable_rigid.radius, self.config)

            if collision["hit"]:
                collision["time"] = clamp(collision["hit"]["time"], 0, 1)
                collision["position"] = collidable_rigid.get_center() + velocity * collision["time"]
                norm = l2_normalize(velocity)
                collision["hit"]["position"] += norm * collidable_rigid.radius
            else:
                collision["position"] = collidable_rigid.get_center() + velocity
                collision["time"] = 1

        return collision


class CollidableRigid(RigidEntity, CollidableAABB):
    def __init__(self, center, radius, config=None):
        RigidEntity.__init__(self, center, config)
        CollidableAABB.__init__(self, center, radius, config)

    def get_center(self):
        return self.prev_state[0:2, 0]
