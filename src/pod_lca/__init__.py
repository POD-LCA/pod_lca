
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

import os

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

seattle = 'USA_WA_Seattle-Tacoma.Intl.AP.727930_TMY3.epw'
SEATTLE = os.path.abspath(os.path.join(DATA, 'operational_dataset', 'weather_files', seattle))

from . import units
from . import visualizer
from . import utilities
from .lca_modules import location
from .lca_modules import uncertainty
from .lca_modules import impacts
from .lca_modules import electricity
from .lca_modules import transportation
from .lca_modules import materials_screening
from .lca_modules import eol
from .lca_modules import building
from .lca_modules import dynamic_radiative_forcing
from .lca_modules import operational

import sys
sys.modules['pod_lca.location'] = location
sys.modules['pod_lca.impacts'] = impacts
sys.modules['pod_lca.uncertainty'] = uncertainty
sys.modules['pod_lca.electricity'] = electricity
sys.modules['pod_lca.materials_screening'] = materials_screening
sys.modules['pod_lca.building'] = building
sys.modules['pod_lca.eol'] = eol
sys.modules['pod_lca.transportation'] = transportation
sys.modules['pod_lca.dynamic_radiative_forcing'] = dynamic_radiative_forcing
sys.modules['pod_lca.operational'] = operational

__all__ = [ "building", "dynamic_radiative_forcing",  "electricity", "eol", "impacts", "location", "materials_screening", "transportation",  "uncertainty", "units", "utilities", "visualizer"]
