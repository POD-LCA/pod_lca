__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from numpy import bool_ as np_bool

from . import Master
from . import Electricity
from ..impacts import CarbonStorage
from ..impacts import Emissions
from ..impacts import Impacts
from ...units import CUBIC_METER
from ...units import KG_CARBON_DIOXIDE
from ...units import KILOMETER
from ...units import KILOGRAM
from ...units import Unit
from ...units import UNITS_MAP
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class Product(Master):
    """Product object, inheriting from the Master object, represent a product.

    Attributes
    ----------
    production_year : int
        The year the product was produced.
    electricity : dict
        Dictionary containing A3 electricity impacts of the production of the material. Keys as follows; \n
        - `'from_database'`: contains unit electricity impacts retrieved from the database;
        - `'by_location'`: contains corresponding electricity impacts by location, retrieved from electricity sub-package.
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
    mineral_carbonation_potential : bool
        Mineral carbonation potential of the product.
    is_material : bool
        True, if the product is a material.
    is_fuel : bool
        True, of the product is an energy source.
    """

    def __init__(self):
        super().__init__()
        self.production_year = None
        self.electricity = {"from_database": None, "by_location": None, "_current": None, "_tag": None}
        self.weight = 0.0
        self.weight_unit = None
        self.density = None
        self.density_unit = None
        self.mineral_carbonation_potential = None
        self.is_material = True
        self.sctg_code = None

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

    def set_unit(self, unit):
        """Set unit of measurement for the product.
            If the unit of measurement is of mass dimensions, same unit is set as weight unit of the product.

        Parameters
        ----------
        unit : ~pod_lca.units.Unit
            Unit of measurement.
        """
        super().set_unit(unit)

        if unit.get_qty_measured() == "mass":
            self.set_weight_unit(unit)
            self.density = 1.0

        return self

    def set_production_year(self, year):
        """Set the year of production for the item.

        Parameters
        ----------
        year : int
            Year of production.
        """
        self.production_year = year

        if self.electricity["by_location"] is not None:
            self.electricity["by_location"].set_year(year)

        return self

    def set_weight_unit(self, unit):
        """Set unit of measurement for the mass of the product.

        Parameters
        ----------
        unit : ~pod_lca.units.Unit
            Unit of measurement. of mass.
        """
        self.weight_unit = unit

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
            unit_inventories = database.get_data_entry(self.get_impact_database_entry())
            if database.get_density_unit_key() is not None:
                self.density_unit = unit_inventories[database.get_density_unit_key()]
                self.density = unit_inventories[database.get_density_key()]
        else:
            raise ValueError("Density input not recognized.")

        return self

    def set_transportation(
        self,
        travel_dist=None,
        dist_unit=None,
        transport_scenario=None,
        return_trip_factor=None,
        mode_name=None,
        mode_efficiency=None,
    ):
        """Set transport processes the product is subject to.

        Parameters
        ----------
        travel_dist : float
            Transportation distance for goods
        dist_unit : ~pod_lca.units.Unit Obj
            Unit of measurement of distances.
        transportation_scenario : str
            Transportation scenario considered.
        return_trip_factor : float
            Return trip factor.
        mode_name : str
            Name of the transportation mode..
        mode_efficiency : str
            Efficiency of the transportation mode.
        """
        if not self.get_unit().get_qty_measured() == "mass":
            self.set_density()

        if travel_dist is None:
            transport_scenario = "Local" if transport_scenario is None else transport_scenario
            mode_efficiency = "Median" if mode_efficiency is None else mode_efficiency
            mode_name = "Truck" if mode_name is None else mode_name

        dist_unit = KILOMETER if dist_unit is None else dist_unit

        transportation_manager = self.get_model().get_transportation_manager()
        if transportation_manager.get_impact_database() is not None:
            transportation_manager.add_good(
                self,
                travel_dist=travel_dist,
                shipping_dest=self.get_project().get_location(),
                shipping_org=None,
                transport_scenario=transport_scenario,
                distance_unit=dist_unit,
                return_trip_factor=None,
                mode_name=mode_name,
                mode_efficiency=mode_efficiency,
            )

        return self

    def set_electricity_source(self, source="from_database"):
        """Set the source of electricity inventories.

        Parameters
        ----------
        source : {'from_database', 'by_location'}
            Source of electricity inventories data. Default 'from_database'.
        """
        if source in [key for key in self.electricity if not key.startswith("_")]:
            if self.electricity["from_database"] is not None:
                original_source = self.electricity["_current"]
                try:
                    self.electricity["_current"] = source
                    self.get_impacts()
                except:
                    self.electricity["_current"] = original_source
                    log(
                        f"Cannont set electricity data to '{source}'. Electricity source reveted to '{self.electricity['_current']}'.",
                        "Warn",
                    )
        else:
            raise KeyError(f"Source of electricty ({source} not recognized.)")

        return self

    def set_electricity_database_tag(self):
        """Find the tag used to identify electricity data in the database."""
        if self.get_impact_database_entry() is not None:
            database = self.get_project().get_impact_database()
            data_set = database.get_data_entry(self.get_impact_database_entry())

            electricity_tag = None
            for key in ["Electricity_", "electricity_", "elec_", "Elec_"]:
                if key + database.get_qty_key() in data_set:
                    electricity_tag = key
                    self.electricity["_tag"] = electricity_tag
                    break

        return self

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

    def set_mineral_carbon_intensity(self, qty, unit=KG_CARBON_DIOXIDE, per=None):
        """Set accelerated carbonation uptake to the 'Mineral C' entry.

        Parameters
        ----------
        qty : float
            Quantity of accelerated carbonation uptake.
        unit : ~pod_lca.units.Unit
            Unit of accelerated carbonation uptake.
        per : dict or ~pod_lca.units.Unit
            Parent quantity for which the mineral carbon intensity is declared.
            If dict, {'per': {'qty': (:class:`int` or :class:`float`), 'unit': (:class:`~pod_lca.units.Unit`)}}
            If Unit object only, the quantity is taken as 1.0;
            If None, taken as per unit of parent objects declared unit.
        """
        key = config["setup"]["impacts"]["ACCELERATED_CARBONATION_INVENTORY"]
        if key in self.unit_carbon_storage.record_attr_dict:
            if self.get_mineral_carbonation_potential():
                mineral_carbon_unit = UNITS_MAP[self.unit_carbon_storage.record_attr_dict[key]]
                input_unit = unit
                conversion_factor_1 = input_unit.convert_to(mineral_carbon_unit)

                if per is None:
                    conversion_factor_2 = 1.0 * self.inventories_declared_qty
                elif isinstance(per, Unit):
                    conversion_factor_2 = per.convert_to(self.inventories_declared_unit) * self.inventories_declared_qty
                elif isinstance(per, dict):
                    conversion_factor_2 = (
                        per["unit"].convert_to(self.inventories_declared_unit)
                        * self.inventories_declared_qty
                        / per["qty"]
                    )
                else:
                    raise TypeError

                setattr(self.unit_carbon_storage, key, qty * conversion_factor_1 * conversion_factor_2)
            else:
                raise Warning(
                    f"Product {self.get_name()} does not have accelerated carbonation potential. Product.set_mineral_carbonation_potential(True) to override."
                )

        return self

    def set_sctg_code(self, code=None):
        """Set the Standard Classification of Transported Goods (SCTG) code for the material.

        Parameters
        ----------
        code : str
            Standard Classification of Transported Goods (SCTG) code of the material
        """
        if code is None:
            data_material = DataImporter.csv_to_pandas(config["file_paths"]["transportation"]["CFS_SCTG_CODE"])
            if self.get_name() in data_material["material"].values:
                sctg = data_material[data_material["material"] == self.get_name()].iloc[0, 1]
                self.sctg_code = str(sctg)
            else:
                log("Material not found in the dataset", "Warn")
        else:
            self.sctg_code = code

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
        return self.production_yea

    def get_electricity(self):
        """Get the electricity product of the item.

        Returns
        -------
        ~pod_lca.electricity.Electricity
            Electricity used in the production of the item.
        """
        return self.electricity[self.get_electricity_source()]

    def get_electricity_source(self):
        """Get the source of electricity inventories.

        Returns
        -------
        str
            Source of electricity inventories data.
        """
        return self.electricity["_current"]

    def get_electricity_database_tag(self):
        """Find the tag used to identify electricity data in the database.

        Returns
        -------
        str
            Tag used to identify electricity data in the database.
        """
        return self.electricity["_tag"]

    def get_electricity_qty(self):
        """Get electricity quantity used for the production of product quantity.

        Returns
        -------
        float
            Quantity of the electricity
        """
        database = self.get_project().get_impact_database()
        data_set = database.get_data_entry(self.get_impact_database_entry())

        qty = data_set[self.get_electricity_database_tag() + database.get_qty_key()]

        declared_unit = database.get_data_entry(self.get_impact_database_entry())[database.get_unit_key()]
        declared_qty = database.get_data_entry(self.get_impact_database_entry())[database.get_qty_key()]
        conversion_factor = self.get_unit().convert_to(declared_unit)

        return qty * (self.get_qty() * conversion_factor / declared_qty)

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
            return self.get_qty() * self.get_density()

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
            return self.get_unit() * self.get_density_unit()

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

    def get_transportation(self):
        """Retrieve transport processes the product is subject to, if any.

        Returns
        -------
        list of ~pod_lca.transportation.TransportationLeg
            Transportation legs the product is subject to.
        """
        transportation_manager = self.get_model().get_transportation_manager()

        return transportation_manager.get_link(self)

    def get_mineral_carbonation_potential(self):
        """Set mineral carbonation potential of the product.

        Returns
        -------
        bool
            Mineral carbonation potential of the product.
        """
        return self.mineral_carbonation_potential

    def get_sctg_code(self, digits=2):
        """Get the Standard Classification of Transported Goods (SCTG) code for the material.

        Parameters
        ----------
        digits : int
            Significant digits of the Standard Classification of Transported Goods (SCTG) code of the material

        Raises
        ------
        ValueError
            SCTG code length shorter that digits requested.
        """
        if self.sctg_code is not None:
            if digits <= len(str(self.sctg_code)):
                return int(str(self.sctg_code)[:digits])
            else:
                raise ValueError(
                    f"SCTG code length ({len(str(self.sctg_code))}) shorter than digits requested ({digits})."
                )
        else:
            return self.sctg_code

    def get_eol_manager(self):
        """Return the place where end-of-life transport dataset reside.

        Returns
        -------
        ~pod_lca.materials_screening.Project
            End-of-life transport data for materials screening project is at project level.
        """
        return self.get_project()

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
        super().update_inventory_records()
        self.update_electricity_records()

        if self.get_mineral_carbonation_potential() is None and self.get_impact_database_entry() is not None:
            data_entry = self.get_project().get_impact_database().get_data_entry(self.get_impact_database_entry())
            key = config["setup"]["impacts"]["ACCELERATE_CARBONATION_POTENTIAL_DATABASE_HEADER"]
            if key in data_entry.index:
                if isinstance(data_entry[key], (bool, np_bool)):
                    potential = data_entry[key]
                elif isinstance(data_entry[key], str):
                    if data_entry[key].lower() in ["yes", "true"]:
                        potential = True
                    elif data_entry[key].lower() in ["no", "false"]:
                        potential = False
                    else:
                        raise ValueError(f"Mineral carbonation potential {data_entry[key]} not recognized")
                else:
                    raise ValueError(f"Mineral carbonation potential {data_entry[key]} not recognized")

                self.set_mineral_carbonation_potential(potential)

        return self

    def update_electricity_records(self):
        """Set electricity objects from database and location. This is done only if the database seperates electricity data (i.e., quantity, unit, and inventories). The electricity data in the database should be prefixed with one of **'Electricity_'**, **'electricity_'**, **'elec_'**, or **'Elec_'**.

        Raises
        ------
        KeyError
            Inventory type not recognized.
        """
        if self.get_impact_database_entry() is not None:
            if self.get_electricity_database_tag() is None:
                self.set_electricity_database_tag()

            database = self.get_project().get_impact_database()
            data_set = database.get_data_entry(self.get_impact_database_entry())

            electricity_tag = self.get_electricity_database_tag()

            if electricity_tag is not None:
                # electricity quantity and unit
                electricity_qty = self.get_electricity_qty()
                if electricity_qty > 0.0:
                    electricity_unit = UNITS_MAP[data_set[electricity_tag + database.get_unit_key()]]
                else:
                    electricity_unit = UNITS_MAP[config["setup"]["electricity"]["DEFAULT_DECLARED_UNIT"]]

                # electricity by location
                if self.electricity["by_location"] is None:
                    electricity_by_location = Electricity.new(
                        id=None,
                        name=self.get_name() + "_electricity",
                        model=self.get_model(),
                        stage=None,
                        qty=electricity_qty,
                        unit=electricity_unit,
                        year=self.get_project().get_year(),
                    )
                    self.electricity["by_location"] = electricity_by_location

                else:
                    self.electricity["by_location"].set_qty(electricity_qty)
                    self.electricity["by_location"].set_unit(electricity_unit)
                    if self.get_project().get_year() is not None:
                        self.electricity["by_location"].set_year(self.get_project().get_year())

                # electricity from database
                if self.electricity["from_database"] is None:
                    database_electricity_qty = data_set[self.get_electricity_database_tag() + database.get_qty_key()]
                    for data_type, DATA_HEADERS_DICT in database.__class__.DATA_IMPORTS.items():
                        record_dict = {}
                        for cat in DATA_HEADERS_DICT:
                            if (database_electricity_qty > 0.0) and (electricity_tag + cat in list(data_set.index)):
                                record_dict[cat] = data_set[electricity_tag + cat] / database_electricity_qty
                            else:
                                record_dict[cat] = 0.0

                        if data_type == "impacts":
                            impacts = Impacts.from_dict(record_dict)
                        elif data_type == "emissions":
                            emissons = Emissions.from_dict(record_dict)
                        elif data_type == "carbon_storage":
                            carbon_storage = CarbonStorage.from_dict(record_dict)
                        else:
                            raise KeyError(f"Record type {data_type} not recognized.")

                    electiricity_from_data = Electricity.from_unit_inventories(
                        name=self.get_name() + "_electricity",
                        qty=electricity_qty,
                        unit=electricity_unit,
                        impacts=impacts,
                        emissions=emissons,
                        carbon_storage=carbon_storage,
                    )
                    self.electricity["from_database"] = electiricity_from_data
                else:
                    self.electricity["from_database"].set_qty(electricity_qty)
                    self.electricity["from_database"].set_unit(electricity_unit)

            if self.get_electricity_source() is None:
                self.electricity["_current"] = "from_database"
            elif self.get_electricity_source() == "by_location":
                for record_type in database.__class__.DATA_IMPORTS:
                    method_name = "get_" + str(record_type)
                    product_record = getattr(self, record_type)
                    product_record -= getattr(self.electricity["from_database"], method_name)()
                    product_record += getattr(self.electricity["by_location"], method_name)()

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
