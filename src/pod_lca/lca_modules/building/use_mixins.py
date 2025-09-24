
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import Impacts


class UseMixins:
    """ Methods for calculation of B1-B7 impacts
    """

    # ================================
    # Inventory Records Methods
    # ================================ 
    def get_replacement_impacts(self):
        """ Get A5 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            A5 impacts of the building.
        """
        impacts = Impacts.from_parent(self)

        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                material_impact = (material.get_product_impacts() + material.get_transportation_impacts() + material.get_eol_impacts())
                construction_waste_impact = material_impact * material.get_waste_rate()

                impacts += construction_waste_impact

        impacts += self.construction_energy_product.get_impacts()

        return impacts

    def get_replacement_emissions(self):
        """ Get A5 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions
            A4-A5 emissions of the building.
        """
        emissions = Emissions.from_parent(self)

        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                material_emissions = (material.get_product_emissions() + material.get_transportation_emissions() + material.get_eol_emissions())
                construction_waste_emissions = material_emissions * material.get_waste_rate()

                emissions += construction_waste_emissions

        emissions += self.construction_energy_product.get_emissions()

        return emissions
