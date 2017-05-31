import numpy as np

__author__ = "Chang Gao"
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

def translate_path(action_path):
    ret = np.array([])
    for i in action_path:
        ret = np.append(ret, action_remapping[i])
    return ret


def store(action_path, layout):
    """
    store action_path and map
    :param layout: 2D numpy array layout (transposed)
    :param action_path: A list of action_path
    """

    with open('layout.txt','a') as layout_file:
        np.savetxt(layout_file, layout, fmt='%i', newline=" ")
        layout_file.write("\n")

    with open('path.txt','a') as path_file:
        np.savetxt(path_file, translate_path(action_path), fmt='%i', newline=" ")
        path_file.write("\n")


def read(filepath, reshape=None):
    readlist = []
    with open(filepath,'r') as layout_file:
        for line in layout_file:
            flatarray = np.fromstring(line, dtype=int, sep=' ')
            if reshape:
                flatarray = np.reshape(flatarray, reshape)
            readlist.append(flatarray)
    print readlist


if __name__ == '__main__':
    read("layout.txt", (30, 10))
    read("path.txt")
