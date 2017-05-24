"""Super Mario Bros simulation in Minecraft
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


from momentum_handler import *
from simulatables import *
from simulation import *
from configuration import *
from layout_loader import *
from malmo_setup import *
from renderer import *
from keypoller import *


# Initialize the phyics configurations by converting constants from hex-strings to floating point numbers
init_phyx_const()
