
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Records
from ...utilities import config

    
class Emissions(Records):
    """ Emissions object keep record of the emissions created by a product or a process.

    Attributes
    ----------
    parent : Master Obj.
        The product or process object to which this emissions record belong.
    <emission_name> : float
        Emission names are dynamically set based on the class variable 'record_attr_dict'.
        Currently, this is set to the EMISSION_INVENTORIES in the config file.
    year : int
        The year of the emission(s).
    function : 
        Function describing the dynamic emission.
    duration : float
        Duration of emission, in years.
    methane_bio_oxidation : float
        Percentage of biogenic methane oxidating to CO2.
    """
    record_type = "Emissions"
    record_attr_dict = config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES']

    def __init__(self):
        super().__init__()
        self.start_year = None
        self.function = 'pulse'
        self.duration = None
        self.methane_bio_oxidation = 0.5

    def set_start_year(self, year):
        """ Set year of the emission.
        
        Parameters
        ----------
        year : int
            Year of the emission occuring.
        """
        self.year = year

        return self
    
    def set_function(self, func):
        """ Set the dyanamic emissions function.
        """
        self.function = func
        # TODO: add setting scipy functions

    def set_duration(self, duration):
        """ Set the duration of emissions.
        
        Parameters
        ----------
        duration : float
            Duration of emission, in years.
        """
        self.duration = duration

        return self
    
    def get_year(self):
        """ Set year of the emission.
        
        Returns
        -------
        int
            Year of the emission occuring.
        """
        return self.year

    def get_function(self):
        """ Get the dyanamic emissions function.
        """
        return self.function

    def get_duration(self):
        """ Get the duration of emissions.
        
        Returns
        -------
        float
            Duration of emission, in years.
        """
        return self.duration
    

if __name__ == '__main__':
    pass
