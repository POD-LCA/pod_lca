
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from math import ceil

from . import Material
from ..impacts import Emissions
from ..impacts import Impacts


class UseMixins:
    """ Methods for calculation of B1-B7 impacts
    """
    
    # ================================
    # Inventory Records Methods
    # ================================ 
    def get_replacement_impacts(self):
        """ Get B6 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            B6 impacts of the building.
        """
        impacts = Impacts.from_parent(self)

        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                replacements = material.get_replacement_materials()
                if replacements is not None:
                    for replacement in replacements:
                        replacement_impact = (replacement.get_product_impacts() + 
                                              replacement.get_transportation_impacts() + 
                                              replacement.get_eol_impacts() + 
                                              replacement.get_construction_impacts())
                                            # construction scope: equipment electricity currently at project level, not material level
                        impacts += replacement_impact

        return impacts

    def get_replacement_emissions(self):
        """ Get B6 emissions of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions
            B6 emissions of the building.
        """
        emissions = Emissions.from_parent(self)

        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                replacements = material.get_replacement_materials()
                if replacements is not None:
                    for replacement in replacements:
                        replacement_emissions = (replacement.get_product_emissions() + 
                                                 replacement.get_transportation_emissions() + 
                                                 replacement.get_eol_emissions() + 
                                                 replacement.get_construction_emissions())
                                                 # construction scope: equipment electricity currently at project level, not material level
                        emissions += replacement_emissions

        return emissions


if __name__ == '__main__':
    pass
