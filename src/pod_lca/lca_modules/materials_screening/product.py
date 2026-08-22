__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

import math
from copy import copy

from . import Master
from . import ProductBioPropertiesMixin
from . import ProductElectricityMixins
from . import ProductTransportationMixins
from ..impacts import UniformEmissionProfile
from ...units import CUBIC_METER
from ...units import KG_CARBON_DIOXIDE
from ...units import KILOGRAM
from ...units import METER
from ...units import Quantity
from ...units import Unit
from ...utilities import log
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
        self.electricity_combo = None

        # transportation mixin
        self.sctg_code = None
        self.transport_legs = None
        self.transportation_combo = None

        # bio properties mixin
        self.dry_density = None
        self.dry_mass = None
        self.moisture_content = 0.0

        # cache
        self._cache_impacts = {"A1": None, "A3": None, None: None}
        self._cache_is_computed = {"A1": False, "A3": False, None: False}
        self._last_params = {"A1": False, "A3": False, None: False}

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


    def set_impact_database_entry(self, database_item):
        """Sets the database (impacts) entry corresponding to the item.
            This method will also update the corresponding impact quanitities.

        Parameters
        ----------
        database_item : str
            The name of the database item which gives the item impacts.
        """
        super().set_impact_database_entry(database_item)

        if database_item is None:
            self.reset_electricity()

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
            if math.isnan(density):
                density = None
            self.density = density
            self.density_unit = density_unit
        elif density is None:
            database = self.get_impact_database()
            if self.get_impact_database_entry() is not None:
                unit_inventories = database.get_data_entry(self.get_impact_database_entry())
                if database.get_density_unit_key() is not None:
                    self.set_density(density=unit_inventories[database.get_density_key()],
                                     density_unit=unit_inventories[database.get_density_unit_key()])
        else:
            raise ValueError("Density input not recognized.")
        
        self.unit_carbon_storage.update_biogenic_carbon_content()

        return self

    def set_thickness(self, thickness=None, thickness_unit=METER):
        """Set thickness of the product.

        Parameters
        ----------
        thickness : str or float
            Thickness of product.
        thickness_unit : ~pod_lca.units.unit
            Unit of measurement of thickness.

        Raises
        ------
        TypeError
            Thickness must be a numerical value.
        """
        if isinstance(thickness, str):
            try:
                self.thickness = float(thickness)
                self.thickness_unit = thickness_unit
            except:
                raise TypeError(f"Thickness of {self.get_name()} should be a numerical value.")
        elif isinstance(thickness, (float, int)):
            if math.isnan(thickness):
                thickness = None
            self.thickness = thickness
            self.thickness_unit = thickness_unit
        else:
            raise ValueError("Thickness input not recognized.")

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
            return Quantity(self.get_qty(), self.get_unit())
        else:
            if self.get_density() is None:
                return None
            else:
                test_unit_mult, factor = (self.unit * self.get_density_unit()).simplify()
                test_unit_div, factor = (self.unit / self.get_density_unit()).simplify()
                if (test_unit_mult).get_qty_measured() == "mass":
                    val = self.get_qty() * self.get_density() * factor
                    unit = test_unit_mult
                    return Quantity(val, unit)
                elif (test_unit_div).get_qty_measured() == "mass":
                    val = (self.get_qty() / self.get_density()) * factor
                    unit = test_unit_div * factor
                    return Quantity(val, unit)
                else:
                    return None

    def get_thickness(self):
        """Retrieve thickness of the product.

        Returns
        -------
        float
            Thickness of product.
        """
        return self.thickness
    
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
    
    def get_thickness_unit(self):
        """Retrieve thickness unit of the product.

        Returns
        -------
        ~pod_lca.units.Unit
            Unit of measurement of the thickness of product.
        """
        return self.thickness_unit

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
        # check for cached result
        current_params = self.get_cache_key()
        if (self._last_params[lc_stage] == current_params) and self._cache_is_computed[lc_stage]:
            log("Returning cached result.", "Info")
            return self._cache_impacts[lc_stage]

        # update inventory records and impacts
        if lc_stage is None:
            impacts = super().get_impacts()

            self._cache_impacts[lc_stage] = copy(impacts)
            self._cache_is_computed[lc_stage] = True
            self._last_params[lc_stage] = current_params

            return impacts
        else:
            impacts = super().get_impacts()

            all_carbon_storage_effects_impact_cat = config["setup"]["impacts"]["ALL_CARBON_STORAGE_EFFECTS_IMPACT_CATEGORY"]
            bio_carbon_storage_effects_impact_cat = config["setup"]["impacts"]["BIOGENIC_CARBON_STORAGE_EFFECTS_IMPACT_CATEGORY"]

            base_impact = impacts.get_record(all_carbon_storage_effects_impact_cat)

            biogenic_carbon_effect = self.get_carbon_storage().get_biogenic_carbon_storage_qty(KG_CARBON_DIOXIDE) 

            if (self.get_life_cycle_stage() == "A1"):
                if (lc_stage == "A1"):
                    adjusted_impact = base_impact - biogenic_carbon_effect
                    adjusted_impact_biogenic = -biogenic_carbon_effect

                elif (lc_stage == "A3") and (self.get_model()):
                    adjusted_impact = biogenic_carbon_effect
                    adjusted_impact_biogenic = biogenic_carbon_effect

                    for impact in impacts.get_categories(): 
                        if impact not in [all_carbon_storage_effects_impact_cat, bio_carbon_storage_effects_impact_cat]:
                            impacts.update_qty({impact: 0.0})

            elif (self.get_life_cycle_stage() == lc_stage):
                adjusted_impact = base_impact
                adjusted_impact_biogenic = 0.0

            else:
                self._cache_impacts[lc_stage] = None
                self._cache_is_computed[lc_stage] = True
                self._last_params[lc_stage] = current_params
                return None

            impacts.update_qty({all_carbon_storage_effects_impact_cat: adjusted_impact}) 
            impacts.update_qty({bio_carbon_storage_effects_impact_cat: adjusted_impact_biogenic})

            self._cache_impacts[lc_stage] = copy(impacts)
            self._cache_is_computed[lc_stage] = True
            self._last_params[lc_stage] = current_params

            return impacts

    def get_carbon_storage(self):
        """Retrieve the carbon storage of the product/process.

        Returns
        -------
        ~pod_lca.impacts.CarbonStorage
            Carbon storage of the product/process.
        """
        current_params = self.get_cache_key()
        if not ((self._last_params["A1"] == current_params) and self._cache_is_computed["A1"]):
            self.update_inventory_records()

        return self.carbon_storage

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

    # ================================
    # Cache Methods
    # ================================
    def get_cache_key(self):
        return (
            self.get_qty(),
            self.get_unit().standard_notation if self.get_unit() else None,
            self.get_impact_database_entry(),
            self.get_life_cycle_stage(),
            self.get_electricity_source(),
            self.get_electricity_scenario(),
            self.get_electricity_year(),
            self.get_electricity_geographical_scope(),
            self.get_electricity_location_regional(),
            self.get_electricity_location_local(),
            self.get_moisture_content(),
            self.get_dry_density() if (self.get_impact_database_entry() and isinstance(self.inventories_declared_unit, Unit)) else None,
            self.unit_carbon_storage.get_mineral_carbonation_potential(),
            self.unit_carbon_storage.get_biogenic_carbon_storage_potential(),
            self.unit_carbon_storage.get_biogenic_carbon_composition(),
            self.unit_carbon_storage.get_mineral_carbon_storage_qty(),
        )
    

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
