__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from numpy import bool_ as np_bool

from . import Master
from . import ProductBioPropertiesMixin
from . import ProductElectricityMixins
from . import ProductTransportationMixins
from ..impacts import UniformEmissionProfile
from ...units import CUBIC_METER
from ...units import KG_CARBON_DIOXIDE
from ...units import KILOGRAM
from ...utilities import config


class Product(Master, ProductElectricityMixins, ProductTransportationMixins, ProductBioPropertiesMixin):
    """Product object, inheriting from the Master object, represent a product.

    Attributes
    ----------
    production_year : int
        The year the product was produced.
    electricity : dict
        Dictionary containing A3 electricity impacts of the production of the material. Keys as follows; \n
        - `'default'`: contains unit electricity impacts retrieved from the database;
        - `'custom'`: contains custom electricity impacts retrieved from electricity sub-package.
        - `'_current'`: indicates which of the above is in use for impacts.
        - `'_tag'`: prefix used in the database to identify grouped impacts of electricity.
    weight : float
        Mass of the product.
    weight_unit : str
        Unit of measurement of mass.
    density : float
        The mass of product in weight units per unit of product's unit of measurement. Default is 1.0.
    sctg_code : str
        Standard Classification of Transported Goods (SCTG) code.
    transport_legs : list of ~pod_lca.transportation.TransportLeg
        Transportation leg corresponding to the product.
    mineral_carbonation_potential : bool
        Mineral carbonation potential of the product.
    is_material : bool
        True, if the product is a material.
    is_fuel : bool
        True, of the product is an energy source.
    """

    def __init__(self):
        super().__init__()
        self.is_material = True
        self.production_year = None
        self.weight = 0.0
        self.weight_unit = None
        self.density = None
        self.density_unit = None
        
        # electricity mixin
        self.electricity = {"default": None, "custom": None, "_current": None, "_tag": None}

        # transportation mixin
        self.sctg_code = None
        self.transport_legs = None

        # bio properties mixin
        self.dry_density = None
        self.dry_mass = None
        self.moisture_content = None

    def __str__(self):
        return f"Product(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"

    # ================================
    # Setters
    # ================================
    def set_qty(self, qty):
        """Update the qty of the product.

        Parameters
        ----------
        qty : float
            Product quantity.
        """
        super().set_qty(qty)

        return self

    def set_unit(self, unit, force_set=False):
        """Set unit of measurement for the product.
            If the unit of measurement is of mass dimensions, same unit is set as weight unit of the product.

        Parameters
        ----------
        unit : ~pod_lca.units.Unit
            Unit of measurement.
        """
        super().set_unit(unit, force_set)

        return self

    def set_production_year(self, year):
        """Set the year of production for the item.

        Parameters
        ----------
        year : int or str
            Year of production.
        """
        if isinstance(year, str):
            year = int(year)

        self.production_year = year

        if self.emissions is not None:
            pulse = UniformEmissionProfile.unit_pulse(at=year)
            self.get_emissions().set_temporal_emission_profile(pulse)

        if self.get_transportation() is not None:
            for leg in self.get_transportation():
                leg.get_emissions().set_temporal_emission_profile(pulse)

        if self.electricity["custom"] is not None:
            self.electricity["custom"].set_year(year)

        return self

    def set_density_unit(self, unit):
        """Set unit of measurement for the mass of the product.

        Parameters
        ----------
        unit : ~pod_lca.units.Unit
            Unit of measurement. of mass.
        """
        self.density_unit = unit

        return self

    def set_density(self, density=None, density_unit=CUBIC_METER / KILOGRAM):
        """Set density of the product.
            Density is defined here as mass per unit measurement of product (not necessarily volume)

        Parameters
        ----------
        density : str or float
            Denisty of product (mass per unit mesurement of product).
        density_unit : ~pod_lca.units.unit
            Unit of measurement of density.

        Raises
        ------
        TypeError
            Density must be a numerical value.
        """
        if isinstance(density, str):
            try:
                self.density = float(density)
                self.density_unit = density_unit
            except:
                raise TypeError(f"Density of {self.get_name()} should be a numerical value.")
        elif isinstance(density, (float, int)):
            self.density = density
            self.density_unit = density_unit
        elif density is None:
            database = self.get_project().get_impact_database()
            if self.get_impact_database_entry() is not None:
                unit_inventories = database.get_data_entry(self.get_impact_database_entry())
                if database.get_density_unit_key() is not None:
                    self.density_unit = unit_inventories[database.get_density_unit_key()]
                    self.density = unit_inventories[database.get_density_key()]
        else:
            raise ValueError("Density input not recognized.")

        return self

    # ================================
    # Getters
    # ================================
    def get_production_year(self):
        """Get the year of production for the item.

        Returns
        -------
        year : int
            Year of production.
        """
        return self.production_year

    def get_weight(self):
        """Retrieve the mass of the product.

        Returns
        -------
        int or float
            Mass of the product.
        """
        if self.get_unit().get_qty_measured() == "mass":
            return self.get_qty()
        else:
            if self.get_density() is None:
                return None
            else:
                declared_unit = self.inventories_declared_unit
                conversion_factor = self.get_unit().convert_to(declared_unit)
                return self.get_qty() * conversion_factor * self.get_density()

    def get_weight_unit(self):
        """Retrieve the unit of measurement of mass of the product.
            This is used for the definition of density of the product.

        Returns
        -------
        ~pod_lca.units.Unit
            Unit of measurement of mass of the product.
        """
        if self.get_unit().get_qty_measured() == "mass":
            return self.get_unit()
        else:
            return self.inventories_declared_unit * self.get_density_unit()

    def get_density(self):
        """Retrieve density of the product.
            Density is defined here as mass per unit measurement of product (not necessarily volume)

        Returns
        -------
        float
            Denisty of product (mass per unit mesurement of product).
        """
        return self.density

    def get_density_unit(self):
        """Retrieve density unit of the product.

        Returns
        -------
        ~pod_lca.units.Unit
            Unit of measurement of the denisty of product.
        """
        return self.density_unit

    def get_eol_manager(self):
        """Return the place where end-of-life transport dataset reside.

        Returns
        -------
        ~pod_lca.materials_screening.Project
            End-of-life transport data for materials screening project is at project level.
        """
        return self.get_project()

    def get_impacts(self, lc_stage=None):
        """Retrieve the impacts of the product.

        Parameters
        ----------
        lc_stage : {None, 'A1', 'A3'}
            Life cycle stage for which the impact value is requested. Default, None.

        Returns
        -------
        ~pod_lca.impacts.Impacts
            Impacts of the product/process.
        """
        if lc_stage is None:
            return super().get_impacts()
        else:
            impacts = super().get_impacts()
            self.update_inventory_records()

            carbonation_effects_impact_cat = config["setup"]["impacts"]["CARBONATION_EFFECTS_IMPACT_CATEGORY"]
            biogenic_carbon_effect = self.get_carbon_storage().get_biogenic_carbon_storage_qty(KG_CARBON_DIOXIDE)

            base_impact = impacts.get_record(carbonation_effects_impact_cat)
            
            if (self.get_life_cycle_stage() == "A1"):
                if (lc_stage == "A1"):
                    adjusted_impact = base_impact - biogenic_carbon_effect
                elif (lc_stage == "A3") and (self.get_model()):
                    adjusted_impact = biogenic_carbon_effect
            elif (self.get_life_cycle_stage() == lc_stage):
                adjusted_impact = base_impact
            else:
                return None

            impacts.update_qty({carbonation_effects_impact_cat: adjusted_impact})

            return impacts
    # ================================
    # Methods
    # ================================
    def update_inventory_records(self):
        """Set inventory quantities, based on database item asigned to the product/process and the product/process quantity. If no database entry is asigned, impacts are not updated.

        Raises
        ------
        ValueError
            Mineral carbonation potential not recognized.
        """
        if self.get_impact_database_entry() is not None:
            super().update_inventory_records()
            self.update_electricity_records()
            
        return self


class Fuel(Product):
    """Fuel product.

    Attributes
    ----------
    is_material : bool
        True
    is_energy : bool
        True
    """

    def __init__(self):
        super().__init__()
        self.is_material = True
        self.is_energy = True

    def __str__(self):
        return f"Fuel(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"


if __name__ == "__main__":
    pass
