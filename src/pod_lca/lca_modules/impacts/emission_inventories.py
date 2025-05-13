from lca_modules.impacts.records import Records
from utilities.settings import config

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

    
class Emissions(Records):
    """
    Emissions object keep record of the emissions created by a product or a process.

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


if __name__ == '__main__':
    pass
