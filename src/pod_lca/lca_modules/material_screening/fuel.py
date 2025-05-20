
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Product
from ..electricity import ElectricitySupply
from ..impacts import CarbonStorage
from ..impacts import Emissions
from ..impacts import Impacts
from ..uncertainty import DataDistribution
from ...utilities import config


class Fuel(Product):
    """ Fuel product object, inheriting from the product object.

    Attributes
    ----------
    is_material : bool
        True
    is_energy : bool
        True
    """

    def __init__(self):
        super().__init__()
        self.is_material = True
        self.is_energy = True

    def __str__(self):
        return f"Fuel(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"

class Electricity(Fuel):
    """ Electricity product object, inheriting from the Fuel object.

    Attributes
    ----------
    electricity_supplier: ElectricitySupply Obj
        Electricity supplier
    year : int
        Year of electricity consumption
    spatial_resolution: str
        Spatial resolution considered for electricity data: 'National'. 'Regional', 'Local'
    scenario: str
        Cambium scenario for prediction of electricity technology futures.
    """

    def __init__(self):
        super().__init__()
        self.electricity_supplier = None
        self.year = None
        self.spatial_resolution = None
        self.scenario = None

    @classmethod
    def new(cls, id, name, model, stage, qty, unit):
        item = cls()

        item.set_id(id)
        item.set_name(name)
        item.set_model(model)
        item.set_life_cycle_stage(stage)
        item.set_qty(qty)
        item.set_unit(unit)
        item.set_weight_unit(unit)
        item.impacts = Impacts.from_parent(item)
        item.emissions = Emissions.from_parent(item)
        item.carbon_stroage = CarbonStorage.from_parent(item)

        electricity_supplier = ElectricitySupply.from_location(model.get_project().get_location())
        item.set_supplier(electricity_supplier)

        return item

    def update_inventory_records(self):
        """ Sets impacts quantities, based on database item asigned to the product/process 
            and the product/process quantity.
            If no database entry is asigned, impacts are not updated.

        Raises
        ------
        ImportError : Incompatible units of Master object and database entry.
        """
        if not self.get_supplier() is None:
            supplier = self.get_supplier()
            
            declared_unit = supplier.get_unit()
            unit_impacts = supplier.get_impacts()
            unit_emissions = supplier.get_emissions()

            conversion_factor = declared_unit.get_conversion_factor(self.get_unit())

            impacts = {category: unit_impacts.get_record(category) * conversion_factor * self.qty for category in config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']}
            self.get_impacts().update_qty(impacts)

            emissions = {category: unit_emissions.get_record(category) * conversion_factor * self.qty for category in config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES']}
            self.get_emissions().update_qty(emissions)
                 
    def set_supplier(self, supplier):
        """ Set electricity supplier.
        
        Parameters
        ----------
        supplier : ElectricitySupply Obj.
            Electricity supply
        """
        self.electricity_supplier = supplier
        self.update_inventory_records()

        return self

    def set_year(self, year):
        """ Set the year of electricity consumption.
        
        Parameters
        ----------
        year : int
            Year of electricity consumption.
        """
        self.get_supplier().set_year(year)
        self.update_inventory_records()

        self.year = year

        return self
    
    def set_spatial_resolution(self, spatial_resolution):
        """ Set the spatial resolution of the electricity supply.
        
        Parameters
        ----------
        spatial_resolution : str
            Spatial resolution of the electricity supply: 'National', 'Regional', 'Local'.
        """
        self.get_supplier().set_spatial_resolution(spatial_resolution)
        self.update_inventory_records()

        self.spatial_resolution = spatial_resolution

        return self
    
    def set_scenario(self, scenario):
        """ Set scenario name. This will be used with cambium data.
        
        Parameters
        ----------
        scenario : str
            Electricity consmuption scenario considered: e.g., 'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'.
        """
        if scenario in ['MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035']:
            self.get_supplier().set_scenario(scenario)
            self.update_inventory_records()
            self.scenario = scenario
        else:
            raise ValueError(f"Scenario {scenario} is not a valid scenario. Valid scenarios are: 'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'.")

        return self
    
    def get_supplier(self):
        """ Get the electricity supplier.
        
        Returns
        -------
        ElectricitySupply Obj.
            Electricity supplier.
        """
        return self.electricity_supplier
    
    def get_year(self):
        """ Get the year of electricity consumption.
        
        Returns
        -------
        int
            Year of electricity consumption.
        """
        return self.year
    
    def get_spatial_resolution(self):
        """ Get the spatial resolution of the electricity supply.
    
        Parameters
        ----------
        str
            Spatial resolution of the electricity supply: 'National', 'Regional', 'Local'.
        """
        return self.spatial_resolution

    def get_scenario(self):
        """ Get scenario name. This will what used with cambium data.
        
        Parameters
        ----------
        str
            Electricity consmuption scenario considered: e.g., 'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'.
        """
        return self.scenario

    def get_data_distribution(self, attr):
        """ Get data_distribution object corresponding to the given attribute.

        Parameters
        ----------
        attr : str.
            Attribute to which the distribution correspond.

        Returns
        -------
        DataDistribution Obj.
            Data distribution.        
        """ 
        if attr == 'impacts':

            supplier = self.get_supplier()
            impact_distribution, weights = supplier.get_impact_distribution() # this is a sampling of unit impacts

            declared_unit = supplier.get_unit()
            conversion_factor = declared_unit.get_conversion_factor(self.get_unit())

            impact_distributions = []
            for category in config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']:
                data = []
                for impact, weight in zip(impact_distribution, weights):
                    data.extend([impact.get_record(category) * conversion_factor * self.get_qty()] * int(weight))

                impact_distributions.append(DataDistribution.from_data(data, is_cts=True, name=category, set_dist=False))

            return impact_distributions

        else:
            return self.data_distributions[attr]


if __name__ == '__main__':
    pass
