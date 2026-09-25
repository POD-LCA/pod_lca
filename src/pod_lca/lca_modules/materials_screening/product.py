__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

import gc
import math
from copy import copy
from numpy import bool_ as np_bool

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
from ...units import UNITS_MAP
from ...utilities import config
from ...utilities import DataImporter
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
    eol_material : str
        End-of-life product corresponding to the material.
    waste_obj : ~pod_lca.lca_modules.eol.waste.Waste
        End-of-life waste product corresponding to the material.
    bio_based : bool
        True if the material is bio-based.
    bio_percentage : float
        Percentage of biogenic content in the bio-based material (0.00 - 1.00).
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

    def set_waste_product(self, expiry_year=None):
        """ Set the end-of-life waste product of the material.

        Parameters
        ----------
        expiry_year : int
            Year when the product becomes waste. If None, set to production year.
        """
        from ..eol.waste import Waste

        eol_mix_data = DataImporter.csv_to_pandas(config['file_paths']['eol']['EOL_DEFAULT_MIXES'])
            
        eol_material = self.get_eol_material()
        waste_qty = self.get_weight()
        waste_unit = self.get_weight_unit()

        if waste_qty is None:
            waste_qty = 0.0
            waste_unit = KILOGRAM
            log(" Cannot determine waste quantity in mass.", level='Warn')

        if eol_mix_data['Material'].isin([eol_material]).any():
            eol_mix = eol_mix_data[eol_mix_data['Material']== eol_material].drop(labels='Material', axis=1).to_dict(orient='records')[0] 
        elif  eol_mix_data['Material'].isin([config['setup']['eol']['EOL_DEFAULT_KEY']]).any():
            eol_mix = eol_mix_data[eol_mix_data['Material']== config['setup']['eol']['EOL_DEFAULT_KEY']].drop(labels='Material', axis=1).to_dict(orient='records')[0]
        else:
            log("A mix doesnt exist", 0)

        bio_based = self.get_bio_based() if isinstance(self.get_bio_based(), (bool, np_bool)) else False

        self.waste_obj = Waste.new(self, 
                            database_item=eol_material, 
                            qty=waste_qty, 
                            unit=waste_unit, 
                            process_mix=eol_mix,
                            bio_based=bio_based)

        self.waste_obj.set_production_year(expiry_year if expiry_year is not None else self.get_production_year())

        del eol_mix_data
        gc.collect()

        return self
    
    def set_bio_based(self, bio_based, bio_percentage=None):
        """ Set the bio-based nature of the material.
        
        Parameters
        ----------
        bio_based : bool
            True if the material is bio-based. 
        bio_percentage : float
            Percentage of biogenic content in the bio-based material (0 - 100). If None, set to 1.0 if bio_based is True, else 0.0.
        
        Raises
        ------
        ValueError
            If bio_based is not a boolean or bio_percentage is not between 0.00 and 1.00.
        """
        if isinstance(bio_based, (bool, np_bool)):
            self.bio_based = bio_based
        else:
            raise ValueError("Bio-based nature needs to be a boolean.")
        
        if bio_percentage is None:
            if self.bio_based:
                self.bio_percentage = 100
            else:
                self.bio_percentage = 0.0
        else:
            if not (0.0 <= bio_percentage <= 100):
                raise ValueError("Biogenic content percentage needs to be between 000 and 100.")
            self.bio_percentage = bio_percentage

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

    def get_bio_based(self):
        """ Get the bio-based nature of the material.
        
        Returns
        -------
        bool
            True if the material is bio-based.   
        """
        return self.bio_based
    
    def get_bio_percentage(self):
        """ Get the percentage of biogenic content in the bio-based material.
        
        Returns
        -------
        float
            Percentage of biogenic content in the bio-based material (0 - 100).   
        """
        return self.bio_percentage
    
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


    def get_eol_process_impact_database(self):
        """ Get the end-of-life process impact database giving the C2-C4 impacts of the building materials.

        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            End-of-life process impact database object.
        """
        return self.get_project().get_eol_process_impact_database()
    
    def get_waste_product(self):
        """ Set the end-of-life waste product of the material.

        Returns
        -------
        ~pod_lca.eol.Waste
            End-of-life waste object corresponding to the material.
        """
        return self.waste_obj
    
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
