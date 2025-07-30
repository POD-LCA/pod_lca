
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import Impacts
from ...units import UNITS_MAP
from ...utilities import config


class ElectricityProducer:
    """
    Electricity generation facility (i.e., power station)

    Attributes
    ----------
    name : str
        Name of the power station / facility.
    technology : str
        Power generation technology.
    year : int
        Year of power generation.
    unit_impacts : ~pod_lca.impacts.Impacts
        Impacts per declared unit of power generation.
    unit_emissions : ~pod_lca.impacts.Emissions
        Emissions per declared unit of power generation.    
    declared_unit : ~pod_lca.units.Unit
        Unit of power generation for which the impacts and emissions are declared.
    """

    def __init__(self):
        self.name = None
        self.technology = None
        self.year = None
        self.unit_impacts = None
        self.unit_emissions = None
        self.declared_unit = UNITS_MAP[config['setup']['electricity']['DEFAULT_DECLARED_UNIT']]

    @classmethod
    def from_technology_year(cls, technology, year):
        """ Create a new ElectricityProducer object with the given location 
        
        Parameters
        ----------
        technology : str
            Power generation technology.
        year : int
            Year of power generation.
        
        Returns
        -------
        ~pod_lca.electricity.ElectricityProducer
            A new ElectricityProducer object with the given location.
        """
        elec_producer = cls()

        elec_producer.set_technology(technology)
        elec_producer.set_year(year)

        elec_producer.unit_impacts = Impacts.from_parent(elec_producer)
        elec_producer.unit_emissions = Emissions.from_parent(elec_producer)

        return elec_producer
    
    # ================================
    # Setters
    # ================================
    def set_name(self, name):
        """ Set the name of the electricity producer.
        
        Parameters
        ----------
        name : str
            The name of the electricity producer.
        """
        self.name = name

        return self
    
    def set_technology(self, technology):
        """ Set the power generation technology.
        
        Parameters
        ----------
        technology : str
            Power generation technology.
        """
        self.technology = technology

        return self
    
    def set_year(self, year):
        """ Set the year of the power generation.
        
        Parameters
        ----------
        year : int
            Year of power generation.
        """
        self.year = year

        return self
    
    def set_unit_impacts(self, impacts):
        """ Set the impacts of the electricity producer, per unit of power generation.
        
        Parameters
        ----------
        impacts : ~pod_lca.impacts.Impacts
            Impacts per declared unit of power generation.
        """
        self.unit_impacts = impacts

        return self
    
    def set_unit_emissions(self, emissions):
        """ Set the emissions of the electricity producer, per unit of power generation.
        
        Parameters
        ----------
        emissions : ~pod_lca.impacts.Emissions
            Emissions per declared unit of power generation.
        """
        self.unit_emissions = emissions

        return self
    
    def set_declared_unit(self, unit):
        """ Set the declared unit of impacts.
    
        Parameters
        ----------
        unit : ~pod_lca.units.Unit
            Declared unit.
        """
        self.declared_unit = unit

        return self
    
    # ================================
    # Getters
    # ================================
    def get_name(self):
        """ Get the name of the electricity producer.
        
        Returns
        -------
        str
            The name of the electricity producer.
        """
        return self.name
    
    def get_technology(self):
        """ Get the power generation technology.
        
        Returns
        -------
        str
            Power generation technology.
        """
        return self.technology
    
    def get_year(self):
        """ Get the year of the power generation.
        
        Returns
        -------
        int
            The year of the electricity producer.
        """
        return self.year
    
    def get_unit_impacts(self):
        """ Get the impacts of the electricity producer.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            Impacts per declared unit of power generation.
        """
        return self.unit_impacts
    
    def get_unit_emissions(self):
        """ Get the emissions of the electricity producer.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions
            Emissions per declared unit of power generation.
        """
        return self.unit_emissions

    def get_declared_unit(self):
        """ Set the declared unit of impacts.
    
        Returns
        -------
        ~pod_lca.units.Unit
            Declared unit.
        """
        return self.declared_unit


if __name__ == '__main__':
    pass
