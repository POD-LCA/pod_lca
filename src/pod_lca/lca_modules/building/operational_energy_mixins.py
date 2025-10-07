
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from collections import defaultdict

from . import OperationalElectricityProduct
from ..impacts import Emissions
from ..impacts import Impacts

    
class OperationalMixins:
    """ Methods for calculation of B6-B7 impacts
    """

    def set_operational_electricity_product(self, unit=None):
        """ Set the operational electricity product of the building
        """
        self.operational_energy_product = OperationalElectricityProduct.create(self, unit)

    def get_operational_electricity_product(self):
        """ Set the operational electricity product of the building
        """
        return self.operational_energy_product

    def get_operational_electricity_usasge(self, summed_at='year', group_by_category=True, group_by_zone=False, unit=None):
        """ Get the operational electricity demands of the building.

        Parameters
        ----------
        summed_at : {'year', 'month'}
            Freequency at whcih the energy plus results are summed.
        group_by_category : bool
            If true, grouped by category, 'heating', 'lighting', and 'cooling'.
        group_by_zone : bool
            If true, grouped by zone.

        Returns
        -------
        ~pod_lca.impacts.Impacts
            B6 impacts of the building.
        """
        # TODO: unit conversion
        electricity_usage = defaultdict(lambda: defaultdict(float))
        for tk, item in self.energy_plus_results.items():
            
            if summed_at == 'year':
                time = 'year' 
            elif summed_at == 'month':
                time = tk[-2:]
            else:
                raise ValueError('Summed at time not recognized.')
            
            for zone, values in item.items():
                for category in ['heating', 'lighting', 'cooling']:
                    if group_by_category and group_by_zone:
                        name = zone + '-' + category
                    elif group_by_category:
                        name = category
                    elif group_by_zone:
                        name = zone
                    else:
                        name = None

                    if name is None:
                        electricity_usage[time] += values[category]
                    else:
                        electricity_usage[time][name] += values[category]

            return electricity_usage

    def run_operational_energy_model(self):
        """ Run operational energy model to get operational energy use and emissions.
        
        Returns
        -------
        None
        """
        # TODO: run e+ model
        # set_usage in the OperationalElectricityProduct
        self.get_operational_electricity_product()._inventories_uptodate = False

        return self
       
    # ================================
    # Inventory Records Methods
    # ================================ 
    def get_operational_impacts(self, category=None, objs=False):
        """ Get B6 impacts of the building.

        Parameters
        ----------
        category : {'heating', 'lighting', 'cooling', None}
            Category of operational energy.
        objs : bool, optional
            If True, return a list of emissions objects for each material. 
            If False, return a single emissions object for the entire building. Default is False.

        Returns
        -------
        ~pod_lca.impacts.Impacts
            B6 impacts of the building.
        """
        if not self.get_operational_electricity_product()._inventories_uptodate:
            self.get_operational_electricity_product().update_inventory_records()

        if objs:
            return self.get_operational_electricity_product().get_impacts(category)
        else:
            impacts = Impacts.from_parent(self)
            for impact in self.get_operational_electricity_product().get_impacts(category):
                impacts += impact

            return impacts

    def get_operational_emissions(self, category=None, objs=False):
        """ Get B6 emissions of the building.

        Parameters
        ----------
        category : {'heating', 'lighting', 'cooling', None}
            Category of operational energy.
        objs : bool, optional
            If True, return a list of emissions objects for each material. 
            If False, return a single emissions object for the entire building. Default is False.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            B6 emissions of the building.
        """
        if not self.get_operational_electricity_product()._inventories_uptodate:
            self.get_operational_electricity_product().update_inventory_records()

        if objs:
            return self.get_operational_electricity_product().get_emissions(category)
        else:
            emissions = Emissions.from_parent(self)
            for emission in self.get_operational_electricity_product().get_emissions(category):
                emissions += emission

            return emissions


if __name__ == '__main__':
    pass
