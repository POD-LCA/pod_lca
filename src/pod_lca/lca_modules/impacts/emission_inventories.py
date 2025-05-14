
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
    """
    record_type = "Emissions"
    record_attr_dict = config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES']

    def __init__(self):
        super().__init__()
        self.year = None

    def set_year(self, year):
        """ Set year of the emission.
        
        Parameters
        ----------
        year : int
            Year of the emission occuring.
        """
        self.year = year

        return self
    
    def get_year(self):
        """ Set year of the emission.
        
        Returns
        -------
        int
            Year of the emission occuring.
        """
        return self.year


if __name__ == '__main__':
    pass
