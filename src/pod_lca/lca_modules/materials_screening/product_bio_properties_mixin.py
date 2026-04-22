__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu, kiun@uw.edu"
__version__ = "0.1.0"

from ...units import KILOGRAM
from ...units import Quantity as Q
from ...utilities import log


class ProductBioPropertiesMixin:

    # ========================
    # Setters
    # ========================
    def set_moisture_content(self, moisture_content):
        """Set moisture content of the product. This is used to calculate dry density and dry mass for biogenic carbon storage calculation.

        Parameters
        ----------
        moisture_content : float
            Moisture content of the product (between 0 and 1).

        Raises
        ------
        ValueError
            Moisture content should be between 0 and 1.
        """
        if isinstance(moisture_content, (float, int)):
            if 0 <= moisture_content <= 1:
                self.moisture_content = moisture_content
            else:
                raise ValueError("Moisture content should be between 0 and 1.")
        else:
            log("Moisture content should be a numerical value.", "Warn")

        self.unit_carbon_storage.update_biogenic_carbon_content()

        return self

    # ========================
    # Getters
    # ========================
    def get_moisture_content(self):
        """Get moisture content of the product.

        Returns
        -------
        float
            Moisture content of the product (between 0 and 1).
        """
        return self.moisture_content
    
    def get_dry_density(self):
        """Get dry density of the product.

        Returns
        -------
        float
            Dry density of the product (mass per unit measurement of product).
        """
        if self.get_density():
            return Q(self.get_density() / (1 + self.get_moisture_content()), self.get_density_unit())
        else:
            return Q(0.0, KILOGRAM / self.inventories_declared_unit)
    
    def get_dry_mass(self):
        """Get dry mass of the product. This is used for biogenic carbon storage calculation.

        Returns
        -------
        float
            Dry mass of the product.
        """   
        if self.get_unit().get_qty_measured() == "mass":
            wet_mass = self.get_qty()
            if wet_mass:
                unit = self.get_unit()
        else:
            wet_mass = self.get_weight()
            if wet_mass:
                unit = self.get_weight_unit()

        if wet_mass:
            return Q(wet_mass / (1 + self.get_moisture_content()), unit) 
        else:
            return Q(0.0, KILOGRAM) 
    