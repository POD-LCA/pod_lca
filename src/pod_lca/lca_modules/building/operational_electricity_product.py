
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..electricity import ElectricitySupply
from ...units import KILO
from ...units import WATT


class OperationalElectricityProduct:
    """ Operational electricity product to manage resulting impacts/emissions from operational energy usage.
    """


    def __init__(self):
        self.name = None
        self.building = None
        self.unit = None
        self.electricity_supplier = None
        self.impacts = {'heating': [], 'lighting': [], 'cooling': []}
        self.emissions = {'heating': [], 'lighting': [], 'cooling': []}

        self._inventories_uptodate = False
        
    # ================================
    # Constructors
    # ================================ 
    @classmethod
    def create(cls, building, unit=None):
        """ Create an operation electricity product
        
        Parameters
        ----------
        building: ~pod_lca.building.Building
            Building in which operational electricity consumed.
        units: ~pod_lca.units.Unit
            Unit of measurement of electricity consumption.
        """
        item = cls()

        item.set_name('operational energy')
        item.set_building(building)
        item.set_unit(unit=KILO * WATT if unit is None else unit)
        item.impacts = None
        item.emissions = None

        electricity_supplier = ElectricitySupply.from_location(building.get_location(), building.get_built_year())
        item.set_supplier(electricity_supplier)

        return item

    # ================================
    # Setters
    # ================================    
    def set_name(self, name):
        """ Set name of the product/process.
        
        Parameters
        ----------
        name : str
            Name of the product/process.
        """
        self.name = name

        return self

    def set_building(self, building):
        """ Set the building of the assembly.
        
        Parameters
        ----------
        building : ~pod_lca.building.Building
            Building to which the assembly belong.
        """
        self.building = building

        return self
    
    def set_unit(self, unit):
        """ Set unit of measurement for the product/process.
        
        Parameters
        ----------
        unit : ~pod_lca.units.Unit
            Unit of measurement.

        Raises
        ------
        ValueError
            Incompatible units.
        """
        self.unit = unit

        return self

    def set_decarbonization_scenario(self, scenario):
        """ Set scenario name. This will be used with cambium data.
    
        Parameters
        ----------
        scenario : {'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'}
            Electricity consmuption scenario considered.
        """
        self.electricity_supplier.set_decarbonization_scenario(scenario)

        self._inventories_uptodate = False

        return self
    
    # ================================
    # Getters
    # ================================ 
    def get_name(self):
        """ Retrieve the name of the product/process.

        Returns
        -------
        str
            Name of the product/process.
        """
        return self.name
        
    def get_unit(self):
        """ Retrieve the unit of measurement of the product/process.

        Returns
        -------
        ~pod_lca.units.Units
            Unit of measurement of the product/process.
        """
        return self.unit
    
    def get_building(self):
        """ Get the building of the assembly.
        
        Returns
        -------
        ~pod_lca.building.Building
            Building to which the assembly belong.
        """
        return self.building

    def get_decarbonization_scenario(self):
        """ Set scenario name. This will be used with cambium data.
    
        Returns
        -------
        str 
            Electricity consmuption scenario considered. {'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'}
        """
        return self.electricity_supplier.get_decarbonization_scenario()
    
    def get_impacts(self, category=None):
        """ Get impacts by functional category.

        Parameters
        ----------
        category : {'heating', 'lighting', 'cooling', None}
            Category of operational energy.

        Returns
        -------
        list of ~pod_lca.impacts.Impacts
            List of impact objects.
        """
        if category is None:
            return [item for sublist in self.impacts.values() for item in sublist]
        else:
            return self.impacts[category]

    def get_emissions(self, category=None):
        """ Get emissions by functional category.

        Parameters
        ----------
        category : {'heating', 'lighting', 'cooling', None}
            Category of operational energy.

        Returns
        -------
        list of ~pod_lca.impacts.Emissions
            List of impact objects.
        """
        if category is None:
            return [item for sublist in self.emissions.values() for item in sublist]
        else:
            return self.emissions[category]
        
    # ================================
    # Methods
    # ================================
    def update_inventory_records(self):
        """ Set the impacts and emissions of the operational energy consmuption.
        """
        building = self.get_building()
        if building.energy_plus_results == None:
            building.run_operational_energy_model()

        annual_electricity_usage = building.get_operational_electricity_usasge(summed_at='year', 
                                                                               group_by_category=True,
                                                                               group_by_zone=False,
                                                                               unit=self.get_unit())

        electricity_declared_unit = self.electricity_supplier.get_declared_unit()
        conversion_factor = electricity_declared_unit.convert_to(self.get_unit())
        for year in range(building.get_built_year(), building.get_built_year() + self.get_life_span() + 1):
            self.electricity_supplier.set_year(year)
            
            self.impacts['heating'].append(self.electricity_supplier.get_impacts() * conversion_factor * annual_electricity_usage['year']['heating'])
            self.impacts['lighting'].append(self.electricity_supplier.get_impacts() * conversion_factor * annual_electricity_usage['year']['lighting'])
            self.impacts['cooling'].append(self.electricity_supplier.get_impacts() * conversion_factor * annual_electricity_usage['year']['cooling'])
            
            self.emissions['heating'].append(self.electricity_supplier.get_emissions() * conversion_factor * annual_electricity_usage['year']['heating'])
            self.emissions['lighting'].append(self.electricity_supplier.get_emissions() * conversion_factor * annual_electricity_usage['year']['lighting'])
            self.emissions['cooling'].append(self.electricity_supplier.get_emissions() * conversion_factor * annual_electricity_usage['year']['cooling'])

        self._inventories_uptodate = True

        return self

if __name__ == '__main__':
    pass