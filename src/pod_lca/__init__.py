import os

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


seattle = 'USA_WA_Seattle-Tacoma.Intl.AP.727930_TMY3.epw'
SEATTLE = os.path.abspath(os.path.join(DATA, 'operational_dataset', 'weather_files', seattle))