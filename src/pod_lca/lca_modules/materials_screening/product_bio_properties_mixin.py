__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu, kiun@uw.edu"
__version__ = "0.1.0"

from numpy import isnan


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
            raise TypeError("Moisture content should be a numerical value.")

        return self
    
    def set_dry_density(self, dry_density=None):
        """Set dry density of the product. This is used to calculate dry mass for biogenic carbon storage calculation.

        Parameters
        ----------
        dry_density : float
            Dry density of the product (mass per unit measurement of product).
        """
        self.dry_density = dry_density
        return self
    
    def set_dry_mass(self, dry_mass=None):
        """Set dry mass of the product. This is used for biogenic carbon storage calculation.

        Parameters
        ----------
        dry_mass : float
            Dry mass of the product.
        """
        self.dry_mass = dry_mass
        return self

    # ========================
    # Getters
    # ========================
    def get_moisture_content(self):
        """Get moisture content of the product. This is used to calculate dry density and dry mass for biogenic carbon storage calculation.

        Returns
        -------
        float
            Moisture content of the product (between 0 and 1).
        """
        # If user or database has already set it, use it
        if self.moisture_content is not None:
            return self.moisture_content

        # Otherwise pull from the database entry
        entry_name = self.parent.get_impact_database_entry()
        if entry_name is None:
            return None

        db = self.parent.get_impact_database()
        entry = db.get_data_entry(entry_name)
        pct = entry["%H2O (mass % moisture)"]

        return pct
    
    def get_dry_density(self):
        """Get dry density of the product. This is used to calculate dry mass for biogenic carbon storage calculation.

        Returns
        -------
        float
            Dry density of the product (mass per unit measurement of product).
        """
        if self.dry_density is not None:
            return self.dry_density
        
        moisture_content = self.get_moisture_content()
        density = self.parent.get_density()
        if moisture_content is not None:
            self.dry_density = density * (1 - moisture_content) if density is not None else None
        else:
            self.dry_density = density if density is not None else None
        return self.dry_density
    
    def get_dry_mass(self):
        """Get dry mass of the product. This is used for biogenic carbon storage calculation.

        Returns
        -------
        float
            Dry mass of the product.
        """
        if self.dry_mass is not None and not isnan(self.dry_mass):
            return self.dry_mass

        parent = self.get_parent()

        if parent.unit is None:
            return None   
              
        try:     
            moisture_content = self.get_moisture_content()
            if isnan(moisture_content):
                moisture_content = None
        except:
            moisture_content = None 

        if parent.unit.get_qty_measured() == "mass":
            if moisture_content is not None:
                self.dry_mass = parent.get_qty() * (1 - moisture_content)
            else:
                self.dry_mass = parent.get_qty()
        else:
            actual_mass = parent.get_weight()
            if (actual_mass is not None) and (moisture_content is not None):
                self.dry_mass = actual_mass * (1 - moisture_content)
            elif actual_mass is not None:
                self.dry_mass = actual_mass
            else:
                return "Error: Unable to calculate dry mass."
        return self.dry_mass
    