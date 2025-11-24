
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import Impacts
from ..impacts import UniformEmissionProfile
from ..materials_screening import Electricity
from ...units import Unit


class ConstructionMixins:
    """ Methods for calculation of A5 impacts
    """

    def set_construction_energy_product(self, energy_use_qty, energy_use_unit):
        """ Set energy product used in the construction of the building.
        
        Parameters
        ----------
        energy_use_qty : float or int
            Total energy usage in construction.
        energy_use_unit: ~pod_lca.units.Unit
            Unit of measurement corresponding to construction energy use.
        """
        if not isinstance(energy_use_qty, (float, int)):
            raise TypeError("Energy use quantity must be a number.")

        if not isinstance(energy_use_unit, Unit):
            raise TypeError("Energy use unit should be a pod_lca.units.Unit object.")
        elif not (energy_use_unit.get_qty_measured() == 'energy'):
            raise TypeError("Energy use unit should be a measure of energy.")

        self.construction_energy_product = Electricity.new(id=0,
                                                           name='construction electricity', 
                                                           model=self, 
                                                           stage='A5', 
                                                           qty=energy_use_qty, 
                                                           unit=energy_use_unit, 
                                                           year=self.get_built_year())

        return self
    
    def get_construction_energy_product(self):
        """ Get the construction energy product.
        
        Returns
        -------
        ~pod_lca.materials_screening.Electricity
            Electricity product for construction energy usage
        """
        return self.construction_energy_product

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

        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                impacts += material.get_construction_impacts()

        # building level impacts
        impacts += self.construction_energy_product.get_impacts() 

        return impacts

    def get_construction_emissions(self):
        """ Get A5 impacts of the building.
                
        Returns
        -------
        ~pod_lca.impacts.Emissions
            A4-A5 emissions of the building.
        """
        emissions = Emissions.from_parent(self)

        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                emissions += material.get_construction_emissions()

        # building level emission
        emissions += self.construction_energy_product.get_emissions()

        pulse = UniformEmissionProfile.unit_pulse(at=self.get_built_year())
        emissions.set_temporal_emission_profile(pulse)

        return emissions


if __name__ == '__main__':
    pass
