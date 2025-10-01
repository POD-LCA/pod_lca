
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Material
from ..impacts import Emissions
from ..impacts import Impacts


class OperationalMixins:
    """ Methods for calculation of B6-B7 impacts
    """
    def run_operational_energy_model(self):
        """ Run operational energy model to get operational energy use and emissions.
        
        Returns
        -------
        None
        """
        pass
    
    # ================================
    # Inventory Records Methods
    # ================================ 
    def get_operational_impacts(self):
        """ Get B6 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            B6 impacts of the building.
        """
        impacts = Impacts.from_parent(self)

        # TODO: add operational energy impacts here

        return impacts

    def get_operational_emissions(self):
        """ Get B6 emissions of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions
            B6 emissions of the building.
        """
        emissions = Emissions.from_parent(self)

        # TODO: add operational energy emissions here

        return emissions


if __name__ == '__main__':
    pass
