import os
HOME = os.path.dirname(os.path.abspath(__file__))

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu";"mhtaba@uw.edu"
__version__ = "0.1.0"


from .projectManager import *
from .model import *
from .databaseManager import *
from .calculator import *
from .visualizer import *
