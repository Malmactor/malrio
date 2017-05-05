import numpy as np
import pqdict

from SuperMarioBros.layout_loader import layout_fromdefault


def l1_distance(a, b):
    return np.sum(np.abs(a - np.array(b)))


def pad_layout(layout):
    return np.pad(layout, (1, 1), 'constant', constant_values=1)


class Astar:
    def __init__(self, layout=layout_fromdefault(), target=3):
        self.layout = pad_layout(layout) # map
        self.target = target # end point
        self.start = tuple(np.array([1, 3]))
        self.end = tuple(np.argwhere(self.layout == target).flatten())

    def path(self):
        r, c = self.layout.shape

        # TODO: use actoin (base on state matrix) + domain (possible induced state matrix)
        # instead of directions. For each loop in the heap, pop top state, calc all possible
        # induced state, then push them into the heap. Notice that final position could be
        # a range (rough position), since we use float.

        directions = [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1])]
        path = []

        path_pre = {self.start: None}
        cost = {self.start: 0}
        frontier_queue = pqdict.minpq({0: [self.start]})

        while frontier_queue:
            priority = frontier_queue.top()
            frontier = frontier_queue[priority][0]
            del frontier_queue[priority][0]
            if not frontier_queue[priority]:
                del frontier_queue[priority]

            if frontier == self.end:
                break

            for dir_neighbor in directions:
                next_node = tuple(frontier + dir_neighbor)
                next_cost = cost[frontier] + 1
                if self.layout[next_node] in [0, 3, 4] and (next_node not in cost or next_cost < cost[next_node]):
                    cost[next_node] = next_cost
                    path_pre[next_node] = frontier
                    heuristic = next_cost + l1_distance(next_node, self.end)
                    # print(next_node)
                    if heuristic in frontier_queue:
                        frontier_queue[heuristic].append(next_node)
                    else:
                        frontier_queue[heuristic] = [next_node]

        node = self.end
        while node is not None:
            path.insert(0, (node[0]-1, node[1]-1)) # cancel the padding offset
            node = path_pre[node]
        return path



# def take_steps(maze, path, scope=5, decay=0.9):
#     visited = np.zeros(maze.shape, "float16")
#
#     center = path[0]
#     path = path[1:]
#     channel = 5
#     radius = scope // 2
#     direction_map = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}
#
#     scope_map = np.zeros((len(path), scope, scope, channel), dtype='float16')
#     visited_map = np.zeros((len(path), scope, scope, 1), dtype='float16')
#     action_label = np.zeros((len(path), 4), dtype='int8')
#
#     idx = 0
#     for next_point in path:
#         visited *= decay
#         visited[center] = 1.0
#
#         cropped_map = maze[center[0] - radius: center[0] + radius + 1, center[1] - radius: center[1] + radius + 1]
#         visited_map[idx, :, :, 0] = visited[center[0] - radius: center[0] + radius + 1,
#                                     center[1] - radius: center[1] + radius + 1]
#
#         for c in range(channel):
#             scope_map[idx, :, :, c][cropped_map == c] = 1.0
#         scope_map[idx, :, :, 0][cropped_map == 3] = 1.0
#         scope_map[idx, :, :, 0][cropped_map == 4] = 1.0
#
#         direction = next_point - np.array(center)
#         action_label[idx, direction_map[tuple(direction)]] = 1.0
#
#         center = next_point
#         idx += 1
#
#     perceptions = np.concatenate((scope_map, visited_map), axis=3)
#
#     return perceptions, action_label
#
#
# def generate_samples(num_sample, size=1000, scope=49, decay=0.9):
#     input_tensor = np.zeros((0, scope, scope, 6))
#     labels = np.zeros((0, 4))
#
#     gen = generator.Prim(size, size)
#
#     for _ in range(num_sample):
#         maze = pad_maze(gen.generate(), scope)
#         path = solver(maze)
#         perceptions, action_label = take_steps(maze, path, scope, decay)
#         input_tensor = np.concatenate((input_tensor, perceptions), axis=0)
#         labels = np.concatenate((labels, action_label), axis=0)
#
#         if _ % 20 == 0:
#             print("{} mazes generated".format(_))
#
#     return input_tensor, labels
#

if __name__ == '__main__':
    solver = Astar()
    print solver.path()
    # inputs, labels = generate_samples(100)
    # np.save("inputs.npy", inputs)
    # np.save("labels.npy", labels)
