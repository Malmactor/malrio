import numpy as np

action_remapping = {
    "remains": 0,
    "left": 1,
    "right": 2,
    "press_jump": 3
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

    with open('path.txt','a') as path_file:
        np.savetxt(path_file, translate_path(action_path), fmt='%i', newline=" ")
