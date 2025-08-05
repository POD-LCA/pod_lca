
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from ..electricity import ElectricitySupply
from ..transportation import TransportMode
from ...units import UNITS_MAP
from ...utilities import config
from ...utilities import DataImporter


class ElectricTransportMode(TransportMode):
    """ Transportation mode using electricity.

    Attributes
    ----------
    location : ~pod_lca.location.Location
        Location where the electricity consumption occurs.
    year : int
        The year of electricity consumption.
    electricity_consumption : float
        Electricity consumption by the transportation mode.
    electricity_consumption_units : ~pod_lca.units.Unit
        Unit corresponding to electricity consumption.
    """

    def __init__(self):
        super().__init__()
        self.location = None
        self.year = None
        self.electricity_consumption = None
        self.electricity_consumption_units = None

    # ================================
    # Getters
    # ================================
    def set_location(self, location):
        """ Set the location of electricity consumption (i.e., where the vehcile is charged).
        
        Parameters
        ----------
        location : ~pod_lca.location.Location
            Location of electricity consumption.
        """
        self.location = location

        return self  

    # ================================
    # Getters
    # ================================
    def get_location(self):
        """ Get the location of electricity consumption.
        
        Returns
        -------
        ~pod_lca.location.Location
            Location of electricity consumption.
        """        
        return self.location
    
    def get_electricity_consumption(self):
        """ Retrieve the electricity consumption of the transportation mode.

        Returns
        -------
        :class:`float`
            Electricity consumption.
        :class:`~pod_lca.units.Unit`
            Corresponding unit of measurement.
        """
        if self.electricity_consumption is None:
            dataset = DataImporter.csv_to_pandas(config['file_paths']['transportation']['ELECTRIC_VEHICLES'])
            row_id = dataset.index[(dataset['mode_name'] == self.get_name()) & (dataset['efficiency'] == self.get_efficiency())]

            unit_data = dataset.iloc[row_id[0]]
            
            self.electricity_consumption = unit_data['electricity_consumption']
            self.electricity_consumption_unit = UNITS_MAP[unit_data['electricity_unit']]

            self.declared_qty = unit_data['qty']
            self.declared_unit = UNITS_MAP[unit_data['unit']]

        return self.electricity_consumption, self.electricity_consumption_unit
    
    def get_electricity_inventories(self):
        """ Get electricity impacts and emission for the transportation mode.
                
        Note
        ----
        1. Uses 'National' average electricity consumption, at the 'MidCase' scenario for the calculation of the electricity impacts.

        Returns
        -------
        :class:`~pod_lca.impacts.Impacts`
            Unit electricity impacts.
        :class:`~pod_lca.impacts.Emissions`
            Unit electricity emissions.
        :class:`~pod_lca.units.Unit`
            Corresponding electricity supply unit.
        """
        electricity_supply = ElectricitySupply.from_location(self.get_location())
        electricity_supply.set_geographical_scope('National') # Default to National average
        electricity_supply.set_scenario('MidCase')

        return electricity_supply.get_unit_impacts(), electricity_supply.get_unit_emissions(), electricity_supply.get_declared_unit()

    # ================================
    # Methods
    # ================================
    def set_inventory_records(self):
        """ Set unit inventory records of impacts and emissions for the transportation mode.
        """
        if (self.get_name() is not None) and (self.get_efficiency() is not None) and (self.get_parent() is not None):
            electricity_consumption, electricity_consumption_unit = self.get_electricity_consumption()
            electricity_unit_impacts, electricity_unit_emissions, electricity_supply_unit = self.get_electricity_inventories()

            conversion_factor = electricity_supply_unit.convert_to(electricity_consumption_unit)

            impacts = electricity_unit_impacts * conversion_factor * electricity_consumption
            self.unit_impacts.update_qty(impacts.get_record_dict())

            emissions = electricity_unit_emissions * conversion_factor * electricity_consumption
            self.unit_emissions.update_qty(emissions.get_record_dict())

        return self
    
    
if __name__ == '__main__':
    pass
