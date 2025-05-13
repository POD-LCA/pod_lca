
import os

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

HOME = os.path.dirname(os.path.abspath(__file__))

from .LCI_database import *
from .problem import *
from .processess import *
from .linear_algebra import *
