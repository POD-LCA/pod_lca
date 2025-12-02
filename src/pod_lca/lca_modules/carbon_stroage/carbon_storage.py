__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Records
from ...utilities import config


class CarbonStorage(Records):
    """CarbonStorage object keep record of the carbon storage records created by a product or a process.

    Attributes
    ----------
    parent : ~pod_lca.materials_screening.Master
        The product or process object to which this carbon storage record belong.
    <category> : float
        Carbon storage categories are dynamically set based on the class variable 'record_attr_dict'.
        Currently, this is set to the CARBON_STORAGE in the config file.
    """

    record_type = "Carbon Storage"
    record_attr_dict = config["setup"]["INVENTORY_ITEMS"]["CARBON_STORAGE"]

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    pass
