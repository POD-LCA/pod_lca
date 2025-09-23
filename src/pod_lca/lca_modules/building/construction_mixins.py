
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import Impacts
from ..impacts import TranportationModeImpactsDatabase


class ConstructionMixins:
    """ Methods for calculation of A5 impacts
    """

    # ================================
    # Inventory Records Methods
    # ================================ 
    def get_construction_impacts(self):
        """ Get A5 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            A5 impacts of the building.
        """
        impacts = Impacts.from_parent(self)

        for transportaion_leg in self.get_transportation_manager().get_transportation_legs():
            impacts += transportaion_leg.get_impacts()

        return impacts

    def get_construction_emissions(self):
        """ Get A5 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions
            A4-A5 emissions of the building.
        """
        emissions = Emissions.from_parent(self)

        for transportaion_leg in self.get_transportation_manager().get_transportation_legs():
            emissions += transportaion_leg.get_emissions()

        return emissions


if __name__ == '__main__':
    pass
