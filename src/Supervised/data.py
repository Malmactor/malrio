import numpy as np

__author__ = "Chang Gao, Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

action_remapping = {
    "remains": 0,
    "left_nojump": 1,
    "right_nojump": 2,
    "left_jump": 3,
    "right_jump": 4,
    "nolr_jump": 5,
    "no_key": 6
}

# def translate_path(action_path):
#     ret = np.array([])
#     for i in action_path:
#         ret = np.append(ret, action_remapping[i])
#     return ret
#
#
# def store(action_path, layout, layout_name='layout.txt', path_name='path.txt'):
#     """
#     store action_path and map
#     :param layout: 2D numpy array layout (transposed)
#     :param action_path: A list of action_path
#     """
#
#     # np.save(layout_name, layout)
#     # np.save(path_name, action_path)
#
#     with open(layout_name,'a') as layout_file:
#         np.savetxt(layout_file, layout, fmt='%i', newline=" ")
#         layout_file.write("\n")
#
#     with open(path_name,'a') as path_file:
#         np.savetxt(path_file, translate_path(action_path), fmt='%i', newline=" ")
#         path_file.write("\n")
#
#
# def read(filepath, reshape=None):
#     readlist = []
#     with open(filepath,'r') as layout_file:
#         for line in layout_file:
#             flatarray = np.fromstring(line, dtype=int, sep=' ')
#             if reshape:
#                 flatarray = np.reshape(flatarray, reshape)
#             readlist.append(flatarray)
#     print readlist


def store_cropped(crop_x, crop_y, render, pos_act_pairs, map_name, path_name, config):
    """
    change position-action pairs into grouped croppedarea-action pairs and store
    :param crop_x, crop_y: crop size
    :param render: crop perception render
    :param pos_act_pairs: position-action pairs, grouped in intervals
    :param map_name, path_name: path to store file
    """
    count = 0
    interval = config["interval"]
    for positions, rawactions in pos_act_pairs:
        maps = np.zeros((interval, crop_x, crop_y, 4), dtype=config["store_dtype"])
        actions = np.zeros((interval), dtype=config["store_dtype"])
        al_actions = []
        for i in range(interval):
            maps[i,:,:,:] = render.crop_and_sample(positions[i])
            actions[i] = action_remapping[rawactions[i]]

        with open(map_name,'a') as map_file:
            np.savetxt(map_file, maps.flatten(), newline=" ")
            map_file.write("\n")

        with open(path_name,'a') as path_file:
            count += len(al_actions)
            np.savetxt(path_file, actions, newline=" ")
            path_file.write("\n")
    print(count)

def read_cropped(filepath, reshape=None, config=None):
    dtype = "float16" if config is None or "store_dtype" not in config else config["store_dtype"]
    readlist = []
    with open(filepath,'r') as layout_file:
        for line in layout_file:
            flatarray = np.fromstring(line, dtype, sep=' ')
            if reshape:
                flatarray = np.reshape(flatarray, reshape)
            readlist.append(flatarray)
    print readlist


if __name__ == '__main__':
    read_cropped("input_map.txt", (5, 60, 60,4))
    read_cropped("input_action.txt")
