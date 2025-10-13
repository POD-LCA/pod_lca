__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from ..operational import find_constructions
from pod_lca.lca_modules.building_envelope.construction import Construction


class Wall(Construction):
    def __init__(self):
        super().__init__()
        self.__type__ = 'Wall'