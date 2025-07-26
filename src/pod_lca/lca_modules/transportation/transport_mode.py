
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import Impacts
from ...utilities import log


class TransportMode:
    """ Transportation mode object.

    Attributes
    ----------
    parent : ~pod_lca.transportation.TransportationLeg 
        Transportation leg to which the transportation mode correspond to.
    mode_name: {'Truck', 'E_Truck', 'Rail', 'Barge' 'Ocean', 'Air'}
        The name of the transportation mode.
    efficiency: {'High', 'Median', 'Low'}
        The efficiency level.
    unit_impacts : ~pod_lca.impacts.Impacts Obj.
        Impacts from the transportation mode, per unit of declared quantity.
    unit_emissions : ~pod_lca.impacts.Emissions Obj.
        Emissions from the transportation mode, per unit of declared quantity.
    declared_unit : ~pod_lca.units.Unit Obj.
        The declared unit corresponding to inventories.
    faf_mode: int
        FAF mode code for the transportation mode.
    cfs_mode: int
        CFS mode code for the transportation mode.
    """

    def __init__(self):
        self.parent = None
        self.mode_name = None
        self.efficiency = None
        self.unit_impacts = None
        self.unit_emissions = None
        self.declared_unit = None
        self.faf_mode = None
        self.cfs_mode = None

    def __str__(self):
        str = "="*75 + "\n" + f"Transportation Mode: {self.get_name()}\n" + "="*75 + "\n"

        return str

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, mode_name, efficiency="Median"):
        """ Create a new transportation mode.

        Parameters
        ----------
        mode_name: str
            the name of the transportation mode (e.g., 'Truck', 'Rail').
        efficiency: int
            the efficiency level (e.g., 1, 2, 3).

        Returns
        -------
        TransportMode
            An instance of the TransportMode class with the specified parameters.
        """
        mode = cls()
        mode.set_name(mode_name)
        mode.set_efficiency(efficiency)

        mode.unit_impacts = Impacts.from_parent(mode)
        mode.unit_emissions = Emissions.from_parent(mode)

        return mode

    # ================================
    # Setters
    # ================================
    def set_parent(self, parent):
        """ Set the parent transportation leg.
        
        Parameters
        ----------
        parent : ~pod_lca.transportation.TransportationLeg
            The transportation leg to which this mode belong.
        """
        self.parent = parent

        return self
    
    def set_name(self, mode_name:(str)):
        """ Set the name of the transportation mode.

        Parameters
        ----------
        mode_name: {'Truck', 'E_Truck', 'Rail', 'Barge' 'Ocean', 'Air'}
            The name of the transportation mode.
        """
        self.mode_name = mode_name
        self.set_inventory_records()

        return self

    def set_efficiency(self, efficiency:(str)):
        """ Set the efficiency of the transportation mode.

        Parameters
        ----------
        efficiency: {'High', 'Median', 'Low'}
            the efficiency level.
        """
        self.efficiency = efficiency
        self.set_inventory_records()

        return self

    # ================================
    # Getters
    # ================================
    def get_parent(self):
        """ Set the parent transportation leg.
        
        Returns
        ----------
        ~pod_lca.transportation.TransportationLeg 
            The transportation leg to which this mode belong.
        """
        return self.parent
    
    def get_name (self):
        """ Retrieve the name of the transportation mode.

        Returns
        ----------
        str
            The name of the transportation mode.
        """
        return self.mode_name

    def get_efficiency (self):
        """ Retrieve the efficiency of the transportation mode.

        Returns
        ----------
        str
            the efficiency level.
        """
        return self.efficiency
    
    def get_unit_impacts(self):
        """ Get unit impacts from the transportation mode.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            Impacts from the transportation mode, per declared quantity and unit.
        """
        return self.unit_impacts
    
    def get_unit_emissions(self):
        """ Get unit emissions from the transportation mode.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            Emissions from the transportation mode, per declared quantity and unit.
        """
        return self.unit_emissions
    
    def get_declared_unit(self):
        """ Get the declared unit of the transportation mode.

        Returns
        -------
        ~pod_lca.units.Unit
            The unit corresponding to declared quantity of inventories.    
        """
        return self.declared_unit
    
    def get_impact_database(self):
        """ Get the impact database.

        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            Impacts database
        """
        return self.get_parent().get_impact_database()

    # ================================
    # Methods
    # ================================
    def set_inventory_records(self):
        """ Set unit inventory records of impacts and emissions for the transportation mode.
        """
        if (self.get_name() is not None) and (self.get_efficiency() is not None) and (self.get_parent() is not None):
            database = self.get_impact_database()
            if database is not None:
                inventories = database.get_data_entry(self)
                self.declared_unit = inventories[database.get_unit_key()]
                inventories_declared_qty = inventories[database.get_qty_key()]

                impacts = {key: inventories[key] / inventories_declared_qty for key in self.unit_impacts.record_attr_dict}
                self.unit_impacts.update_qty(impacts)

                emissions = {key: inventories[key] / inventories_declared_qty for key in self.unit_emissions.record_attr_dict}
                self.unit_emissions.update_qty(emissions)

                return self
            else:
                log("No transportation mode impact database set.", "Warn")

                return None

    
if __name__ == '__main__':
    pass
