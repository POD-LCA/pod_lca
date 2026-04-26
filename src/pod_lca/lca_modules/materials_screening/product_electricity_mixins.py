__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Electricity
from ..carbon_storage import CarbonStorage
from ..impacts import Emissions
from ..impacts import Impacts
from ...units import UNITS_MAP
from ...utilities import config
from ...utilities import log


class ProductElectricityMixins:

    # ================================
    # Setters
    # ================================
    def set_electricity_product(self):
        """Set electricity product for the item from database and location. This is done only if the database seperates electricity data (i.e., quantity, unit, and inventories). The electricity data in the database should be prefixed with one of **'Electricity_'**, **'electricity_'**, **'elec_'**, or **'Elec_'**."""
        if self.get_impact_database_entry() is not None:
            database = self.get_impact_database()
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
                electricity_by_location = Electricity.new(
                    id=None,
                    name=self.get_name() + "_electricity",
                    model=self.get_model(),
                    stage=None,
                    qty=electricity_qty,
                    unit=electricity_unit,
                    year=self.get_production_year()
                )
                self.electricity["custom"] = electricity_by_location

                # electricity from database
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
                self.electricity["default"] = electiricity_from_data

            # set default electricity source
            self.set_electricity_source()

        return self

    def set_electricity_source(self, source="default"):
        """Set the source of electricity inventories.

        Parameters
        ----------
        source : {'default', 'custom'}
            Source of electricity inventories data. Default 'default'.
        """
        if source in [key for key in self.electricity if not key.startswith("_")]:
            if self.electricity["default"] is not None:
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

    def set_electricity_scenario(self, scenario=None):
        """Set the electricity scenario for the electricity.
        This forced the electricity source to be "custom" if scenario is provided, and revet to "default" if scenario is None.

        Parameters
        ----------
        scenario : {'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'}
            Electricity scenario for the electricity by location data.
        """
        current_source = self.get_electricity_source()

        if scenario is None:
            if current_source == "custom":
                self.set_electricity_source("default")
                self.electricity["custom"].set_scenario(config["setup"]["electricity"]["DEFAULT_SCENARIO"])
        else:
            if current_source == "default":
                self.set_electricity_source("custom")
            self.electricity["custom"].set_scenario(scenario)
        
        return self
    
    def set_electricity_year(self, year):
        """Set the year for the electricity.
        This forced the electricity source to be "custom" if year is provided, and revet to "default" if year is None.

        Parameters
        ----------
        year : int
            Year for the electricity by location data.
        """
        current_source = self.get_electricity_source()

        if year is None:
            if current_source == "custom":
                self.set_electricity_source("default")
                self.electricity["custom"].set_year(self.get_production_year())
        else:
            if current_source == "default":
                self.set_electricity_source("custom")
            self.electricity["custom"].set_year(year)
        
        return self
    
    def set_electricity_location_regional(self, state):
        """Set the location for the electricity, at the regional level.
        This forced the electricity source to be "custom" if location is provided, and revet to "default" if location is None.

        Parameters
        ----------
        location : str
            Location for the electricity by location data.
        """
        current_source = self.get_electricity_source()

        if state is None:
            if current_source == "custom":
                self.set_electricity_source("default")
                self.electricity["custom"].set_geographical_scope(config["setup"]["electricity"]["DEFAULT_REIGIONAL_RESOLUTION"])
                self.electricity["custom"].set_location(location_obj=self.get_model().get_location())
        else:
            if current_source == "default":
                self.set_electricity_source("custom")
            
            self.electricity["custom"].set_geographical_scope("Regional")
            self.electricity["custom"].set_location(state=state)
        
        return self

    def set_electricity_location_local(self, zip_code):
        """Set the location for the electricity, at local level.
        This forced the electricity source to be "custom" if location is provided, and revet to "default" if location is None.

        Parameters
        ----------
        location : str
            Location for the electricity by location data.
        """
        current_source = self.get_electricity_source()

        if zip_code is None:
            if current_source == "custom":
                self.set_electricity_source("default")
                self.electricity["custom"].set_geographical_scope(config["setup"]["electricity"]["DEFAULT_REIGIONAL_RESOLUTION"])
                self.electricity["custom"].set_location(location_obj=self.get_model().get_location())
        else:
            if current_source == "default":
                self.set_electricity_source("custom")
            
            self.electricity["custom"].set_geographical_scope("Local")
            self.electricity["custom"].set_location(zip_code=zip_code)
        
        return self
    
    def set_electricity_database_tag(self):
        """Find the tag used to identify electricity data in the database."""
        if self.get_impact_database_entry() is not None:
            database = self.get_impact_database()
            data_set = database.get_data_entry(self.get_impact_database_entry())

            electricity_tag = None
            for key in ["Electricity_", "electricity_", "elec_", "Elec_"]:
                if key + database.get_qty_key() in data_set:
                    electricity_tag = key
                    self.electricity["_tag"] = electricity_tag
                    break

        return self
    
    # ================================
    # Getters
    # ================================

    def get_electricity(self):
        """Get the electricity product of the item.

        Returns
        -------
        ~pod_lca.electricity.Electricity
            Electricity used in the production of the item.
        """
        if self.get_electricity_source() in self.electricity:
            return self.electricity[self.get_electricity_source()]
        else:
            return None

    def get_electricity_source(self):
        """Get the source of electricity inventories.

        Returns
        -------
        str
            Source of electricity inventories data.
        """
        return self.electricity["_current"]

    def get_electricity_scenario(self):
        """Get the electricity scenario for the electricity by location data.

        Returns
        -------
        str
            Electricity scenario for the electricity by location data.
        """
        current_source = self.get_electricity_source()

        if current_source == "custom":
            return self.electricity["custom"].get_scenario()
        else:
            return None
        
    def get_electricity_year(self):
        """Get the year for the electricity by location data.

        Returns
        -------
        int
            Year for the electricity by location data.
        """
        current_source = self.get_electricity_source()

        if current_source == "custom":
            return self.electricity["custom"].get_year()
        else:
            return None
        
    def get_electricity_location_regional(self):
        """Get the location for the electricity by location data.

        Returns
        -------
        str
            Location for the electricity by location data.
        """
        current_source = self.get_electricity_source()

        if current_source == "custom":
            return self.electricity["custom"].get_location().get_state()
        else:
            return None

    def get_electricity_location_local(self):
        """Get the location for the electricity by location data.

        Returns
        -------
        str
            Location for the electricity by location data.
        """
        current_source = self.get_electricity_source()

        if current_source == "custom":
            return self.electricity["custom"].get_location().get_zip()
        else:
            return None

    def get_electricity_database_tag(self):
        """Find the tag used to identify electricity data in the database.

        Returns
        -------
        str
            Tag used to identify electricity data in the database.
        """
        if self.electricity["_tag"] is None:
            self.set_electricity_database_tag()
            
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

    # ================================
    # Methods
    # ================================
    def update_electricity_records(self):
        """Set electricity objects from database and location. This is done only if the database seperates electricity data (i.e., quantity, unit, and inventories). The electricity data in the database should be prefixed with one of **'Electricity_'**, **'electricity_'**, **'elec_'**, or **'Elec_'**.

        Raises
        ------
        KeyError
            Inventory type not recognized.
        """
        if self.electricity["default"] is None:
            self.set_electricity_product()
        
        if self.get_impact_database_entry() is not None:
            database = self.get_impact_database()
            electricity_tag = self.get_electricity_database_tag()

            if electricity_tag is not None:
                electricity_qty = self.get_electricity_qty()
                self.electricity["custom"].set_qty(electricity_qty)
                self.electricity["default"].set_qty(electricity_qty)

            if self.get_electricity_source() is None:
                self.electricity["_current"] = "default"
            elif self.get_electricity_source() == "custom":
                for record_type in database.__class__.DATA_IMPORTS:
                    method_name = "get_" + str(record_type)
                    product_record = getattr(self, record_type)
                    product_record -= getattr(self.electricity["default"], method_name)()
                    product_record += getattr(self.electricity["custom"], method_name)()

        return self
    
if __name__ == "__main__":
    pass
