
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Records
from ...units import KG_CARBON_DIOXIDE
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
    def set_mineral_carbon(self, qty, unit=KG_CARBON_DIOXIDE):
        """ Set accelerated carbonation uptake to the 'Mineral C' entry.
        
        Parameters
        ----------
        qty : float
            Quantity of accelerated carbonation uptake.
        unit : Unit Obj
            Unit of accelerated carbonation uptake.
        """
        key = config['setup']['impacts']['ACCELERATED_CARBONATION_INVENTORY']
        if key in self.record_attr_dict:
            if self.get_parent().get_mineral_carbonation_potential():
                mineral_carbon_unit = UNITS_MAP[self.record_attr_dict[key]]
                input_unit = unit
                conversion_factor = input_unit.get_conversion_factor(mineral_carbon_unit)
                
                setattr(self, key, qty * conversion_factor)
            else:
                raise Warning(f"Product {self.get_parent().get_name()} does not have accelerated carbonation potential. Product.set_mineral_carbonation_potential(True) to override.")

        return self


if __name__ == '__main__':
    pass
