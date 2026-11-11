__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "Modified BSD License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Impacts
from ..impacts import Emissions


class DemolitionProcess:
    """Class representing the demolition process of a building.

    Attributes
    ----------
    name : str
        Name of the demolition process.
    parent : object
        Parent object associated with the demolition process.
    life_cycle_stage : str
        Life cycle stage of the demolition process.
    """

    def __init__(self):
        self.name = None
        self.parent = None
        self.life_cycle_stage = 'C1'
        self.impacts = Impacts.from_parent(self)
        self.emissions = Emissions.from_parent(self)

    @classmethod
    def new(cls, parent):
        """Create new waste process.

        Parameters
        ----------
        parent : ~pod_lca.eol.Waste
            Waste object for which the waste processing belong.

        Returns
        -------
        ~pod_lca.eol.WasteProcess
            Waste process object.
        """
        demolition_process = cls()

        demolition_process.set_name(parent.get_name() + "- Demolition")
        demolition_process.set_parent(parent)

        return demolition_process

    # ================================
    # Setters
    # ================================
    def set_name(self, name):
        """Set name of the waste process.

        Parameters
        ----------
        name : str
            Name of the waste process.
        """
        self.name = name

        return self
    
    def set_parent(self, parent):
        """Set parent Waste object of the Waste Processing.

        Parameters
        ----------
        parent : ~pod_lca.eol.Waste
            Waste object for which the waste processing belong.
        """
        self.parent = parent

        return self

    # ================================
    # Getters
    # ================================
    def get_name(self):
        """Get name of the waste process.

        Returns
        -------
        str
            Name of the waste process.
        """
        return self.name
    
    def get_parent(self):
        """Get parent Waste object of the Waste Processing.

        Returns
        -------
        ~pod_lca.eol.Waste
            Waste object for which the waste processing belong.
        """
        return self.parent

    def get_impacts(self):
        """Get impacts of the waste process.

        Returns
        -------
        ~pod_lca.impacts.Impacts
            Impacts of the waste process.
        """
        self.update_unit_inventories()
        return self.impacts

    def get_emissions(self):
        """Get emissions of the waste process.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            Emissions of the waste process.
        """
        self.update_unit_inventories()
        return self.emissions

    # ================================
    # Methods
    # ================================
    def update_unit_inventories(self):
        """Set unit impacts of the waste process."""

        parent = self.get_parent()

        demolition_impact_database = parent.get_demolition_impact_database()
        database_entry = demolition_impact_database.get_data_entry(parent.get_impact_database_entry())

        declared_unit = database_entry[demolition_impact_database.get_unit_key()]
        declared_qty = database_entry[demolition_impact_database.get_qty_key()]
        conversion_factor = declared_unit.convert_to(parent.get_unit())

        impacts_data = {
            key: database_entry[key] * conversion_factor * parent.get_qty() / declared_qty
            for key in self.impacts.record_attr_dict
        }
        emissions_data = {
            key: database_entry[key] * conversion_factor * parent.get_qty() / declared_qty
            for key in self.emissions.record_attr_dict
        }

        self.impacts.update_qty(impacts_data)
        self.emissions.update_qty(emissions_data)
    