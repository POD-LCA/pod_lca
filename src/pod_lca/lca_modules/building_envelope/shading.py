from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"




from pod_lca.lca_modules.building_envelope.construction import Construction


class Shading(Construction):
    """Shading construction object based on the 
    ~pod_lca.building_envelope.Construction class. 
    """
    def __init__(self):
        super().__init__()
        self.__type__ = 'Shading'