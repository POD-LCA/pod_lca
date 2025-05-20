
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Records
from ...units import UNITS_MAP
from ...utilities import config


class CarbonStorage(Records):
    """ CarbonStorage object keep record of the carbon storage records created by a product or a process.

    Attributes
    ----------
    parent : Master Obj.
        The product or process object to which this carbon storage record belong.
    <category> : float
        Carbon storage categories are dynamically set based on the class variable 'record_attr_dict'.
        Currently, this is set to the CARBON_STORAGE in the config file.
    """

    record_type = "Carbon Storage"
    record_attr_dict = config['setup']['INVENTORY_ITEMS']['CARBON_STORAGE']

    def __init__(self):
        super().__init__()

    # ========================
    # Carbon Storage Methods
    # ========================
    def set_mineral_carbon(self, qty, unit='kg CO2'):
        """ Set accelerated carbonation uptake to the 'Mineral C' entry.
        
        Parameters
        ----------
        qty : float
            Quantity of accelerated carbonation uptake.
        unit : str
            Unit of accelerated carbonation uptake.
        """
        key = 'Mineral C'
        if key in self.record_attr_dict:
            mineral_carbon_unit = UNITS_MAP[self.record_attr_dict[key]]
            input_unit = UNITS_MAP[unit]
            conversion_factor = input_unit.get_conversion_factor(mineral_carbon_unit)
            
            setattr(self, key, qty * conversion_factor)

        return self


if __name__ == '__main__':
    pass
