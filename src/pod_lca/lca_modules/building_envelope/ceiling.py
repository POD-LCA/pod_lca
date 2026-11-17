__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "Modified BSD License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building_envelope.construction import Construction
from ...utilities import log


class Ceiling(Construction):
    """Ceiling construction object based on the 
    ~pod_lca.building_envelope.Construction class. 
    """
    construction_type = 'Ceiling'

    def __init__(self):
        super().__init__()


    def set_materials(self):
        """Set the materials of the ceiling construction.
        """
        floor_no = self.parent.floor_no
        total_floors = self.parent.building.no_floors
        if floor_no == total_floors - 1:
            super().set_materials()
        else:
            log("Ceiling construction is not set for floor {} because it is not the top floor.".format(floor_no), "Info")

