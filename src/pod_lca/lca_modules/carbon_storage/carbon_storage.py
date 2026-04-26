__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu, kiun@uw.edu"
__version__ = "0.1.0"

from numpy import bool_ as np_bool

from ..carbon_storage import get_biogenic_carbon_content
from ..impacts import Records
from ...units import KG_CARBON
from ...units import KG_CARBON_DIOXIDE
from ...units import KILOGRAM
from ...units import Quantity as Q
from ...units import UNITS_MAP
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
        self.mineral_carbonation_potential = False
        self.biogenic_carbon_storage_potential = False
        self.biogenic_carbon_percentage = 0.0
        
    # ========================
    # Setters
    # ========================
    def set_mineral_carbonation_potential(self, potential):
        """Set mineral carbonation potential of the product.

        Parameters
        ----------
        potential : bool
            Mineral carbonation potential of the product.
        """
        if isinstance(potential, (bool, np_bool)):
            self.mineral_carbonation_potential = potential
        else:
            raise ValueError("Mineral carbonation potential needs to be a boolean.")

        return self

    def set_biogenic_carbon_storage_potential(self, potential):
        """Set biogenic carbon storage potential of the product.

        Parameters
        ----------
        potential : bool
            Biogenic carbon storage potential of the product. (Boolean indicating whether product contains biogenic carbon)
        """
        if isinstance(potential, (bool, np_bool)):
            self.biogenic_carbon_storage_potential = potential
        else:
            raise ValueError("Biogenic carbon storage potential needs to be a boolean.")

        return self
    
    def set_biogenic_carbon_composition(self, percent):
        """
        Set the percent carbon (%C dry mass basis) for biogenic carbon composition.
        pct should be a float (e.g., 52.3 means 52.3%).
        """
        if percent is None:
            self.biogenic_carbon_percentage = None
        elif isinstance(percent, (float, int)):
            self.biogenic_carbon_percentage = percent
        elif isinstance(percent, str):
            percent_str = percent.replace('%', '')
            self.biogenic_carbon_percentage = float(percent_str) / 100.0
        else:
            raise TypeError("Carbon percentage must be numerical.")
        
        self.update_biogenic_carbon_content()
                        
    # ========================
    # Getters
    # ========================
    def get_mineral_carbonation_potential(self):
        """Get mineral carbonation potential of the product.

        Returns
        -------
        bool
            Mineral carbonation potential of the product.
        """
        return self.mineral_carbonation_potential 

    def get_biogenic_carbon_storage_potential(self):
        """Get biogenic carbon storage potential of the product.

        Returns
        -------
        bool
            Biogenic carbon storage potential of the product.
        """
        return self.biogenic_carbon_storage_potential

    def get_biogenic_carbon_composition(self):
        """Get biogenic carbon composition of the product.

        Returns
        -------
        float
            Biogenic carbon composition of the product (between 0 and 1).
        """
        return self.biogenic_carbon_percentage
    
    def get_mineral_carbon_storage_qty(self, unit=KG_CARBON_DIOXIDE):
        """Get the quantity of mineral carbon storage.

        Returns
        -------
        float
            Quantity of mineral carbon storage.
        """
        if self.get_mineral_carbonation_potential():
            key = config["setup"]["impacts"]["ACCELERATED_CARBONATION_INVENTORY"]
            mineral_carbon_unit = UNITS_MAP[self.record_attr_dict[key]]

            conversion_factor = mineral_carbon_unit.convert_to(unit)

            return self.get_record(key) * conversion_factor
        
        else:
            return 0.0

    def get_biogenic_carbon_storage_qty(self, unit=KG_CARBON):
        """Get the quantity of biogenic carbon storage.

        Returns
        -------
        float
            Quantity of biogenic carbon storage.
        """
        if self.get_biogenic_carbon_storage_potential():
            key = config["setup"]["impacts"]["BIOGENIC_CARBON_STORAGE_INVENTORY"]
            biogenic_carbon_unit = UNITS_MAP[self.record_attr_dict[key]]

            conversion_factor = biogenic_carbon_unit.convert_to(unit)

            return self.get_record(key) * conversion_factor
        
        else:
            return 0.0

    # ========================
    # Methods
    # ========================
    def update_biogenic_carbon_content(self):
        """ Update the biogenic carbon content in the record.
            Bigoenic carbon content recalculated based on dry mass and carbon composition.
        """
        if self.get_biogenic_carbon_storage_potential():
            parent = self.get_parent()

            unit_dry_mass = parent.get_dry_density() * Q(1, parent.inventories_declared_unit)
            carbon_content = get_biogenic_carbon_content(
                carbon_composition=self.get_biogenic_carbon_composition(),
                dry_mass=unit_dry_mass)
            
            key = config["setup"]["impacts"]["BIOGENIC_CARBON_STORAGE_INVENTORY"]
            bio_carbon_unit = UNITS_MAP[self.record_attr_dict[key]]

            if bio_carbon_unit == KG_CARBON:
                self.update_qty({key:  carbon_content.convert_to(KILOGRAM).value})
            else:
                raise ValueError("Carbon content unit not recognized")


if __name__ == "__main__":
    pass
