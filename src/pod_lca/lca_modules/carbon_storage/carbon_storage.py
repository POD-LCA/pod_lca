__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Records
from ...utilities import config
from ...units import Unit, UNITS_MAP, KG_CARBON_DIOXIDE, KG_CARBON
from numpy import bool_ as np_bool
from ..carbon_storage import get_dry_mass, get_biogenic_carbon_content, get_biogenic_carbon_dioxide_content




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
        self.mineral_carbon_storage_source = None 
        self.mineral_carbon_storage_qty = None 
        self.mineral_carbonation_potential = None
        self.dry_density = None
        self.dry_mass = None
        self.moisture_content = None
        self.biogenic_carbon_percentage = None
        self.biogenic_carbon_storage_potential = None
        self.biogenic_carbon_storage_source = None

    
    # ====== Setters ======

    def set_mineral_carbon_storage_source(self, source=None):
        """Set the source for mineral carbon storage.
        Parameters
        ----------
        source : str
            Source for mineral carbon storage ('from_database' or 'custom')."""
        if source == None:
            source = "from_database" 
        self.mineral_carbon_storage_source = source

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

    def set_mineral_carbon_storage_qty(self, qty, unit=KG_CARBON_DIOXIDE, per=None):
        """Set accelerated carbonation uptake to the 'Mineral C' entry.

        Parameters
        ----------
        qty : float
            Quantity of accelerated carbonation uptake.
        unit : ~pod_lca.units.Unit
            Unit of accelerated carbonation uptake.
        per : dict or ~pod_lca.units.Unit
            Parent quantity for which the mineral carbon storage qty is declared.
            If dict, {'per': {'qty': (:class:`int` or :class:`float`), 'unit': (:class:`~pod_lca.units.Unit`)}}
            If Unit object only, the quantity is taken as 1.0;
            If None, taken as per unit of parent objects declared unit.
        """
        key = config["setup"]["impacts"]["ACCELERATED_CARBONATION_INVENTORY"]
        parent = self.get_parent()
        if key in parent.unit_carbon_storage.record_attr_dict:
            if self.get_mineral_carbonation_potential():
                mineral_carbon_unit = UNITS_MAP[parent.unit_carbon_storage.record_attr_dict[key]]
                input_unit = unit
                conversion_factor_1 = input_unit.convert_to(mineral_carbon_unit)

                if per is None:
                    conversion_factor_2 = 1.0 / (parent.qty*(parent.unit.convert_to(parent.inventories_declared_unit)))
                elif isinstance(per, Unit):
                    conversion_factor_2 = per.convert_to(parent.inventories_declared_unit) * parent.inventories_declared_qty
                elif isinstance(per, dict):
                    conversion_factor_2 = (
                        per["unit"].convert_to(parent.inventories_declared_unit)
                        * parent.inventories_declared_qty
                        / per["qty"]
                    )
                else:
                    raise TypeError

                #setattr(parent.unit_carbon_storage, key, qty * conversion_factor_1 * conversion_factor_2)
                self.update_qty({key: qty * conversion_factor_1 * conversion_factor_2})
            else:
                raise Warning(
                    f"Product {parent.get_name()} does not have accelerated carbonation potential. Product.set_mineral_carbonation_potential(True) to override."
                )
                
        return self
    
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

    def set_biogenic_carbon_storage_source(self, source=None):
        """Set the source for biogenic carbon storage.
        Parameters
        ----------
        source : str
            Source for biogenic carbon storage ('from_database' or 'custom')."""
        if source == None:
            source = "from_database"

        self.biogenic_carbon_storage_source = source

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


    def set_biogenic_carbon_storage_qty(self, qty, unit=KG_CARBON_DIOXIDE, per=None):
        """Set the quantity of biogenic carbon storage.
        Parameters
        ----------
        qty : float
            Quantity of biogenic carbon storage.
        unit : ~pod_lca.units.Unit
            Unit of biogenic carbon storage.
        per : dict or ~pod_lca.units.Unit
            Parent quantity for which the biogenic carbon storage is declared.
            If dict, {'per': {'qty': (:class:`int` or :class:`float`), 'unit': (:class:`~pod_lca.units.Unit`)}}
            If Unit object only, the quantity is taken as 1.0;
            If None, taken as per unit of parent objects declared unit.
        """
        key = config["setup"]["impacts"]["BIOGENIC_CARBON_STORAGE_INVENTORY"]
        parent = self.get_parent()
        if key in parent.unit_carbon_storage.record_attr_dict:
            if self.get_biogenic_carbon_storage_potential():
                biogenic_carbon_unit = UNITS_MAP[parent.unit_carbon_storage.record_attr_dict[key]]
                input_unit = unit
                conversion_factor_1 = input_unit.convert_to(biogenic_carbon_unit)

                if per is None:
                    conversion_factor_2 = 1.0 / (parent.qty*(parent.unit.convert_to(parent.inventories_declared_unit)))
                elif isinstance(per, Unit):
                    conversion_factor_2 = per.convert_to(parent.inventories_declared_unit) / parent.qty
                elif isinstance(per, dict):
                    conversion_factor_2 = (
                        per["unit"].convert_to(parent.inventories_declared_unit)
                        / parent.qty
                        / per["qty"]
                    )
                else:
                    raise TypeError

                #setattr(parent.unit_carbon_storage, key, qty * conversion_factor_1 * conversion_factor_2)
                self.update_qty({key: qty * conversion_factor_1 * conversion_factor_2})
            else:
                raise Warning(
                    f"Product {parent.get_name()} does not have biogenic carbon storage potential. Product.set_biogenic_carbon_storage_potential(True) to override."
                )
            
        return self
    
    # ====== Getters ======
    
    def get_mineral_carbon_storage_source(self):
        """Get the source for mineral carbon storage.
        Returns
        -------
        str
            Source for mineral carbon storage ('from_database' or 'custom').
        """
        if self.mineral_carbon_storage_source is not None:
            return self.mineral_carbon_storage_source
        else:
            self.mineral_carbon_storage_source = "from_database"
            return self.mineral_carbon_storage_source

    def get_mineral_carbon_storage_qty(self):
        """Get the quantity of mineral carbon storage.

        Returns
        -------
        float
            Quantity of mineral carbon storage.
        """
        return self.get_record('Mineral C')

    def get_mineral_carbonation_potential(self):
        """Set mineral carbonation potential of the product.

        Returns
        -------
        bool
            Mineral carbonation potential of the product.
        """
        if self.mineral_carbonation_potential is not None:
            return self.mineral_carbonation_potential

        entry_name = self.parent.get_impact_database_entry()
        if entry_name is None:
            return None

        db = self.parent.get_impact_database()
        entry = db.get_data_entry(entry_name)
        header = config["setup"]["impacts"]["ACCELERATED_CARBONATION_POTENTIAL_DATABASE_HEADER"]
        return entry[header]
    
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
        if self.dry_mass is not None:
            return self.dry_mass

        parent = self.get_parent()

        if parent.unit is None:
            return None   
              
        moisture_content = self.get_moisture_content()
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
    
    def get_biogenic_carbon_composition(self):
        """Get biogenic carbon composition of the product. This is used for biogenic carbon storage calculation.

        Returns
        -------
        float
            Biogenic carbon composition of the product (between 0 and 1).
        """
        if self.biogenic_carbon_percentage is not None:
            return self.biogenic_carbon_percentage

        entry_name = self.parent.get_impact_database_entry()
        if entry_name is None:
            return None

        db = self.parent.get_impact_database()
        entry = db.get_data_entry(entry_name)
        pct = entry["%C (dry mass basis)"]
        return pct

    def get_biogenic_carbon_storage_potential(self):
        """Set biogenic carbon storage potential of the product.

        Returns
        -------
        bool
            Biogenic carbon storage potential of the product.
        """
        if self.biogenic_carbon_storage_potential is not None:
            return self.biogenic_carbon_storage_potential

        entry_name = self.parent.get_impact_database_entry()
        if entry_name is None:
            return None

        db = self.parent.get_impact_database()
        entry = db.get_data_entry(entry_name)
        header = config["setup"]["impacts"]["BIOGENIC_CARBON_STORAGE_POTENTIAL_DATABASE_HEADER"]
        return entry[header]
    
    def get_biogenic_carbon_storage_source(self):
        """Get the source for biogenic carbon storage.
        Returns
        -------
        str
            Source for biogenic carbon storage ('from_database' or 'custom').
        """
        if self.biogenic_carbon_storage_source is not None:
            return self.biogenic_carbon_storage_source
        
        else:
            self.biogenic_carbon_storage_source = "from_database"
            return self.biogenic_carbon_storage_source
    
    def get_biogenic_carbon_storage_qty(self, unit=KG_CARBON):
        """Get the quantity of biogenic carbon storage.

        Returns
        -------
        float
            Quantity of biogenic carbon storage.
        """
        if self.get_biogenic_carbon_storage_source() == "from_database":
            parent = self.get_parent()
            database_entry = parent.get_impact_database_entry()
            database = parent.get_impact_database()
            default_unit_C_storage = database.get_data_entry(database_entry, 'Biogenic C')
            
            conversion_factor = parent.unit.convert_to(parent.inventories_declared_unit)
            default_C_storage = default_unit_C_storage * conversion_factor 
            if unit == KG_CARBON:
                return default_C_storage 
            elif unit == KG_CARBON_DIOXIDE:   
               default_CO2_storage = get_biogenic_carbon_dioxide_content(default_C_storage) 
               return default_CO2_storage

        else:
            carbon_storage_C = self.get_record('Biogenic C') 
            if unit == KG_CARBON:
                return carbon_storage_C   
            elif unit == KG_CARBON_DIOXIDE:
                carbon_storage_CO2 = get_biogenic_carbon_dioxide_content(carbon_storage_C)
                return carbon_storage_CO2


if __name__ == "__main__":
    pass
