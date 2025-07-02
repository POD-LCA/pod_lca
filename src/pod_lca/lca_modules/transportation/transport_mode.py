
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import Impacts
from ...units import KILOGRAM
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class TransportMode:
    """ Initialize the TransportMode object.

    Attributes
    ----------
    mode_name: str
        The name of the transportation mode (e.g., 'Truck', 'Rail').
    efficiency: int
        The efficiency level (e.g., 1, 2, 3).
    fuel_type: str
        The fuel type used
    electricity consumption: float
        Electriciity consumption if an electric vehicle
    limitations: list,
        a list of limitations for the transportation mode.
    faf_mode: int
        FAF mode code for the transportation mode.
    cfs_mode: int
        CFS mode code for the transportation mode.
    """

    def __init__(self):
        self.parent = None
        self.mode_name = None
        self.efficiency = None
        self.fuel_type = None
        self.unit_impacts = None
        self.unit_emissions = None
        self.inventories_declared_unit = None
        self.inventories_declared_qty = None
        self.electricity_consumption = None
        self.limitations = []
        self.faf_mode = None
        self.cfs_mode = None

    def __str__(self):
        """ String representation of the TransportMode object.
        """
        str = "="*75 + "\n" + f"Transportation Mode: {self.get_name()}\n" + "="*75 + "\n"

        return str

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, mode_name, efficiency="Median", fuel_type="Regular"):
        """ Create a new transportation mode.

        Parameters
        ----------
        mode_name: str
            the name of the transportation mode (e.g., 'Truck', 'Rail').
        efficiency: int
            the efficiency level (e.g., 1, 2, 3).
        project: ProjectLogisticManager Obj. 
            an object representing the project.
        fuel_type: str
            the type of fuel used (default is "Regular").

        Returns
        -------
        TransportMode
            An instance of the TransportMode class with the specified parameters.
        """
        mode = cls()
        mode.set_name(mode_name)
        mode.set_efficiency(efficiency)
        mode.set_fuel_type(fuel_type)

        mode.unit_impacts = Impacts.from_parent(mode)
        mode.unit_emissions = Emissions.from_parent(mode)

        return mode

    # ================================
    # Setters
    # ================================
    def set_parent(self, parent):
        """ Set the parent transportation link.
        
        Parameters
        ----------
        parent : LogisticLink Obj.
            The transportation link to which this mode belong.
        """
        self.parent = parent

        return self
    
    def set_name(self, mode_name:(str)):
        """ Set the name of the transportation mode.

        Parameters
        ----------
        mode_name: str
            The name of the transportation mode.
        """
        self.mode_name = mode_name
        self.set_inventory_records()

        return self

    def set_efficiency(self, efficiency:(str)):
        """ Set the efficiency of the transportation mode.

        Parameters
        ----------
        efficiency: str
            the efficiency level (e.g., 'Low', 'Medium', 'High').
        """
        self.efficiency = efficiency
        self.set_inventory_records()

        return self

    def set_fuel_type(self, fuel_type:(str)):
        """ Set the fuel type of the transportation mode.

        Parameters
        ----------
        fuel_type: str
            The type of fuel used (e.g., 'Regular', 'Premium').
        """
        self.fuel_type = fuel_type
        self.set_inventory_records()

        return self

    def set_faf_mode(self):
        """ Set the FAF mode code for the transportation mode.
        """
        faf_modes_mapping = DataImporter.json_to_dict(config['file_paths']['transportation']['FAF_MODE_CODE'])
        if self.mode_name in faf_modes_mapping:
            self.faf_mode = faf_modes_mapping[self.mode_name]
        else:
            log(f"FAF mode mapping failed.", "Warn")

        return self

    def set_cfs_mode(self):
        """ Set the CFS mode code for the transportation mode.
        """
        cfs_modes_mapping = DataImporter.json_to_dict(config['file_paths']['transportation']['CFS_MODE_CODE'])
        if self.mode_name in cfs_modes_mapping:
            self.cfs_mode = cfs_modes_mapping[self.mode_name]
        else:
            log(f"CFS mode mapping failed.", "Warn")

        return self

    # ================================
    # Getters
    # ================================
    def get_parent(self):
        """ Set the parent transportation link.
        
        Returns
        ----------
        LogisticLink Obj.
            The transportation link to which this mode belong.
        """
        return self.parent
    
    def get_name (self):
        """ Retrieve the name of the transportation mode.
        """
        return self.mode_name

    def get_efficiency (self):
        """ Retrieve the efficiency of the transportation mode.
        """
        return self.efficiency

    def get_faf_mode (self):
        """ Retrieve the FAF mode code of the transportation mode.
        """
        if self.faf_mode is None:
            self.set_faf_mode()

        return self.faf_mode

    def get_cfs_mode (self):
        """ Retrieve the CFS mode code of the transportation mode.
        """
        if self.cfs_mode is None:
            self.set_cfs_mode()

        return self.cfs_mode

    def get_fuel_type (self):
        """ Retrieve the fuel type of the transportation mode.
        """
        return self.fuel_type

    def get_electricity_consumption (self):
        """ Retrieve the electricity consumption of the transportation mode.
        """
        return self.electricity_consumption
    
    def get_unit_impacts(self):
        """ Get unit impacts from the transportation mode.
        """
        return self.unit_impacts
    
    def get_unit_emissions(self):
        """ Get unit emissions from the transportation mode.
        """
        return self.unit_emissions
    
    def get_inventories_declared_unit(self):
        """ Get the declared unit of the transportation mode.
        """
        return self.inventories_declared_unit
    
    def get_inventories_declared_qty(self):
        """ Get the declared qty of the transportation mode.
        """
        return self.inventories_declared_qty
            
    # ================================
    # Methods
    # ================================
    def set_inventory_records(self):
        """ Set unit impacts of the transportation mode.
        """
        if (self.get_name() is not None) and (self.get_fuel_type() is not None) and (self.get_efficiency() is not None) and (self.get_parent() is not None):

            database = self.get_parent().get_project().get_database()

            unit_inventories = database.get_data_entry(self)
            self.inventories_declared_unit = unit_inventories[database.get_unit_key()]
            self.inventories_declared_qty = unit_inventories[database.get_qty_key()]

            impacts = {key: unit_inventories[key] for key in self.unit_impacts.record_attr_dict}
            self.unit_impacts.update_qty(impacts)

            emissions = {key: unit_inventories[key] for key in self.unit_emissions.record_attr_dict}
            self.unit_emissions.update_qty(emissions)

        return self


if __name__ == '__main__':
    pass
