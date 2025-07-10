
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

    def __init__(self):
        self.name = None
        self.energy_source = None
        self.year = None
        self.unit_impacts = None
        self.unit_emissions = None
        self.declared_unit = UNITS_MAP[config['setup']['electricity']['DEFAULT_DECLARED_UNIT']]

    @classmethod
    def from_technology_year(cls, technology, year):
        """ Create a new ElectricityProducer object with the given location 
        
        Parameters
        ----------
        technology : str.
            The name of the electricity technology.
        year : int
            The year of electricity production.
        
        Returns
        -------
        ElectricityProducer
            A new ElectricityProducer object with the given location.
        """
        elec_producer = cls()

        elec_producer.set_energy_source(technology)
        elec_producer.set_year(year)
        elec_producer.set_invetories()

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
    
    def set_energy_source(self, energy_source):
        """ Set the energy source of the electricity producer.
        
        Parameters
        ----------
        energy_source : str
            The energy source of the electricity producer.
        """
        self.energy_source = energy_source

        return self
    
    def set_year(self, year):
        """ Set the year of the electricity producer.
        
        Parameters
        ----------
        year : int
            The year of the electricity producer.
        """
        self.year = year
        self.set_invetories()

        return self
    
    def set_unit_impacts(self, impacts=None):
        """ Set the impacts of the electricity producer.
        
        Parameters
        ----------
        impacts : dict
            The impacts of the electricity producer.
        """
        self.unit_impacts = impacts

        return self
    
    def set_unit_emissions(self, emissions=None):
        """ Set the emissions of the electricity producer.
        
        Parameters
        ----------
        emissions : dict
            The emissions of the electricity producer.
        """
        if emissions is None:
            emissions = {}
        else:
            self.unit_emissions = emissions

        return self
    
    def set_declared_unit(self, unit):
        """ Set the declared unit of impacts.
    
        Parameters
        ----------
        unit : Unit Obj.
            Declared unit.
        """
        self.declared_unit = unit

        return self
    
    def set_invetories(self):
        """ Set the impacts and emissions inventories of the electricity producer.
        """
        self.set_unit_impacts()
        self.set_unit_emissions()

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
    
    def get_energy_source(self):
        """ Get the energy source of the electricity producer.
        
        Returns
        -------
        str
            The energy source of the electricity producer.
        """
        return self.energy_source
    
    def get_year(self):
        """ Get the year of the electricity producer.
        
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
        dict
            The impacts of the electricity producer.
        """
        return self.unit_impacts
    
    def get_unit_emissions(self):
        """ Get the emissions of the electricity producer.
        
        Returns
        -------
        dict
            The emissions of the electricity producer.
        """
        return self.unit_emissions

    def get_declared_unit(self):
        """ Set the declared unit of impacts.
    
        Returns
        -------
        unit : Unit Obj.
            Declared unit.
        """
        return self.declared_unit


if __name__ == '__main__':
    pass
