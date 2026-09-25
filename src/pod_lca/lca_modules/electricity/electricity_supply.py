__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from numpy import round as np_round

from . import CambiumData
from . import ElectricityProducer
from ..impacts import ElectricityImpactsDatabase
from ..impacts import Emissions
from ..impacts import Impacts
from ...units import UNITS_MAP
from ...units import WATT_HOUR
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class ElectricitySupply:
    """Electricity supplier manages the distribution of electricity from the electricity producers to the consumers.

    Attributes
    ----------
    name : str
        The name of the electricity supply authority.
    geographical_scope : {'National', 'Regional', 'Local'}
        Geographical scope of the electricity supply. \n
        - `'National'`: US average
        - `'Regional'`: FERC region
        - `'Local'`: Balancing Authority.
    location : ~pod_lca.location.Location
        The location of the electricity supply authority.
    consumption_mix : dict
        The consumption mix of the electricity supply authority: {**technology**: :class:`str`}.
    year : int
        The year of the electricity supply authority.
    impacts : ~pod_lca.impacts.Impacts
        The impacts of the electricity supply authority.

    Notes
    -----
    1. Location, regionality, and year determines the consumption mix.
    2. Location and regionality determines the impact by technology.
    """

    def __init__(self):
        self.name = None
        self.geographical_scope = config["setup"]["electricity"]["DEFAULT_REIGIONAL_RESOLUTION"]
        self.location = None
        self.consumption_mix = {}
        self.electricity_producers = {}
        self.year = None
        self.scenario = config["setup"]["electricity"]["DEFAULT_SCENARIO"]
        self.unit_impacts = None
        self.unit_emissions = None
        self.declared_unit = UNITS_MAP[config["setup"]["electricity"]["DEFAULT_DECLARED_UNIT"]]

        self.impact_database_national = None
        self.impact_database_regional = None

    def __str__(self):
        str = "=" * 75 + "\n" + f"Electricity Supply: {self.get_name()}\n" + "=" * 75 + "\n"
        str += f"Year: {self.get_year()}\n"
        str += f"Gographical scope: {self.get_geographical_scope()}\n"

        str += "-" * 75 + "\n" + "Tecnology Mix:\n"
        str += f"Scenario (cambium): {self.get_scenario()}\n"

        if self.get_geographical_scope() == "National":
            if self.get_location() is None:
                str += f"Country: {config['setup']['electricity']['DEFAULT_COUNTRY']}\n"
            else:
                str += f"Country: {self.get_location().get_country()}\n"
        elif self.get_geographical_scope() == "Regional":
            if self.get_location().get_cambium_gea_region() is not None:
                str += f"GEA Region: {self.get_location().get_cambium_gea_region()[0]}\n"
            else:
                str += f"GEA Region: {self.get_location().get_cambium_gea_region()}\n"
        elif self.get_geographical_scope() == "Local":
            if self.get_location().get_reeds_balancing_area() is not None:
                str += f"ReEDS BA: {self.get_location().get_reeds_balancing_area()[0]}\n"
            else:
                str += f"ReEDS BA: {self.get_location().get_reeds_balancing_area()}\n"

        str += "-" * 75 + "\n" + "Impacts per technology:\n"
        if self.get_geographical_scope() == "National":
            if self.get_location() is None:
                str += f"Country: {config['setup']['electricity']['DEFAULT_COUNTRY']}\n"
            else:
                str += f"Country: {self.get_location().get_country()}\n"
        elif self.get_geographical_scope() == "Regional":
            if self.get_location().get_ferc_region() is not None:
                str += f"FERC Region: {self.get_location().get_ferc_region()[0]}\n"
            else:
                str += f"FERC Region: {self.get_location().get_ferc_region()}\n"
        elif self.get_geographical_scope() == "Local":
            if self.get_location().get_ferc_region() is not None:
                str += f"FERC Region: {self.get_location().get_ferc_region()[0]}\n"
            else:
                str += f"FERC Region: {self.get_location().get_ferc_region()}\n"

        return str

    # ========================
    # Constructors
    # ========================
    @classmethod
    def from_location(cls, location, year=None):
        """Create a new Electricity supplier for the given location.

        Parameters
        ----------
        location : ~pod_lca.location.Location
            The location of the electricity supply authority.
        year : int
            Year of electricity consumption.

        Returns
        -------
        ~pod_lca.electricity.ElectricitySupply
            Electricity supplier for the given location.
        """
        elec_supp_authority = cls()
        elec_supp_authority.unit_impacts = Impacts.from_parent(elec_supp_authority)
        elec_supp_authority.unit_emissions = Emissions.from_parent(elec_supp_authority)

        elec_supp_authority.set_location(location)
        if year is None:
            elec_supp_authority.set_year(config["setup"]["electricity"]["DEFAULT_YEAR"])
        else:
            elec_supp_authority.set_year(year)

        if location is None:
            elec_supp_authority.set_geographical_scope(config["setup"]["electricity"]["DEFAULT_REIGIONAL_RESOLUTION"])
        else:
            elec_supp_authority.set_geographical_scope(location.get_regionality())

        return elec_supp_authority

    # ================================
    # Setters
    # ================================
    def set_name(self, name):
        """Set the name of the electricity supply authority.

        Parameters
        ----------
        name : str
            The name of the electricity supply authority.
        """
        self.name = name

        return self

    def set_geographical_scope(self, geographical_scope):
        """Set the geographical cope of the electricity supply authority.

        Parameters
        ----------
        geographical_scope : {'National'. 'Regional', 'Local'}
            Geographical scope of the electricity supply. \n
            - `'National'`: US average
            - `'Regional'`: FERC region
            - `'Local'`: Balancing Authority.
        """
        location_resolution = (
            self.get_location().get_regionality()
            if self.get_location() is not None
            else config["setup"]["electricity"]["DEFAULT_REIGIONAL_RESOLUTION"]
        )
        if (
            (location_resolution == "National") and (geographical_scope == "Local" or geographical_scope == "Regional")
        ) or ((location_resolution == "Regional") and (geographical_scope == "Local")):
            log("Spatial resolution of electricity supply cannot be finer than that of location.", "Warn")
            return self

        self.geographical_scope = geographical_scope

        return self

    def set_location(self, location):
        """Set the location of the electricity supply authority.

        Parameters
        ----------
        location : ~pod_lca.location.Location
            The location of the electricity supply authority.
        """
        self.location = location

        return self

    def set_consumption_mix(self, consumption_mix):
        """Set the consumption mix of the electricity supply authority.

        Parameters
        ----------
        consumption_mix : dict
            The consumption mix of the electricity supply authority: {**technology**: :class:`str`}.
        """
        self.consumption_mix.clear()
        self.consumption_mix.update(consumption_mix)

        return self

    def set_year(self, year):
        """Set the year of the electricity supply authority.
            Changing the year changes the consumption mix based on Cambium data.

        Parameters
        ----------
        year : int
            The year of the electricity supply authority.
        """
        self.year = year

        return self

    def set_declared_unit(self, unit):
        """Set the declared unit of impacts.

        Parameters
        ----------
        unit : ~pod_lca.units.Unit
            Declared unit.
        """
        self.declared_unit = unit

        return self

    def set_scenario(self, scenario):
        """Set scenario name. This will be used with cambium data.

        Parameters
        ----------
        scenario : {'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'}
            Electricity consmuption scenario considered.
        """
        self.scenario = scenario

        return self

    def set_electricity_producers(self, geographical_scope):
        """Set the electricity producers for a given technology mix and corresponding impact data.

        Parameters
        ----------
        geographical_scope : {'National'. 'Regional', 'Local'}
            Geographical scope of the electricity supply. \n
            - `'National'`: US average
            - `'Regional'`: FERC region
            - `'Local'`: Balancing Authority.

        Raises
        ------
        KeyError
            FERC region not found for location.
        ValueError
            Geographical scope of electricity supply is not recognized.
        """
        # Get regionalised impact data
        if geographical_scope == "National":
            if self.impact_database_national is None:
                self.impact_database_national = ElectricityImpactsDatabase.new(
                    "Electricity - National", geographical_scope
                )
                self.impact_database_national.set_data(
                    config["file_paths"]["electricity"]["ELECTRICITY_IMPACT_NATIONAL_DATA"]
                )
            impact_database = self.impact_database_national
            region = (
                self.get_location().get_country_code()
                if self.get_location() is not None
                else config["setup"]["electricity"]["DEFAULT_COUNTRY_CODE"]
            )

        elif (geographical_scope == "Regional") or (geographical_scope == "Local"):
            if self.impact_database_regional is None:
                self.impact_database_regional = ElectricityImpactsDatabase.new(
                    "Electricity - Regional", geographical_scope
                )
                self.impact_database_regional.set_data(
                    config["file_paths"]["electricity"]["ELECTRICITY_IMPACT_REGIONAL_DATA"]
                )
            impact_database = self.impact_database_regional

            if self.get_location().get_ferc_region() is None:
                self.get_location().set_ferc_region()

            region = self.get_location().get_ferc_region()
            if len(region) == 0:
                raise KeyError(f"FERC region not found for location: {self.get_location().get_zip()}.")
            elif len(region) == 1:
                region = region[0]
            else:
                region = self.pick_region(region, impact_database)

        else:
            raise ValueError("Geographical scope of electricity supply is not recognized.")

        # set producesrs and inventories
        for key in self.get_consumption_mix().keys():
            if key in self.electricity_producers:
                producer = self.electricity_producers[key]
            else:
                producer = ElectricityProducer.from_technology_year(key, self.get_year())
                self.electricity_producers[key] = producer

            data_dict = impact_database.get_data_entry(region, key)
            declared_qty = data_dict[impact_database.get_qty_key()]
            if not declared_qty == 1:
                raise ValueError("Declared quantity should be one for unit impacts.")

            impact_data_dict = {
                cat: impact 
                for cat, impact in data_dict.items() 
                if cat in producer.get_unit_impacts().get_categories()
            }
            producer.get_unit_impacts().update_qty(impact_data_dict)

            emissions_data_dict = {
                cat: emission
                for cat, emission in data_dict.items()
                if cat in producer.get_unit_emissions().get_categories()
            }
            producer.get_unit_emissions().update_qty(emissions_data_dict)

        return self

    # ================================
    # Getters
    # ================================
    def get_name(self):
        """Get the name of the electricity supply authority.

        Returns
        -------
        str
            The name of the electricity supply authority.
        """
        return self.name

    def get_geographical_scope(self):
        """Get the set geographical scope of the electricity supply authority.

        Returns
        -------
        str
            The geographical scope of the electricity supply.
        """
        return self.geographical_scope

    def get_location(self):
        """Get the location of the electricity supply authority.

        Returns
        -------
        ~pod_lca.location.Location
            The location of the electricity supply authority.
        """
        return self.location

    def get_consumption_mix(self):
        """Get the consumption mix of the electricity supply authority.

        Returns
        -------
        dict
            The consumption mix of the electricity supply authority: {**technology**: :class:`str`}.
        """
        return self.consumption_mix

    def get_year(self):
        """Get the year of the electricity supply authority.

        Returns
        -------
        int
            The year of the electricity supply authority.
        """
        return self.year

    def get_unit_impacts(self):
        """Get the impacts of the electricity supply authority.

        Returns
        -------
        ~pod_lca.impacts.Impacts
            The impacts of the electricity supply authority.
        """
        self.update_inventory_records()

        return self.unit_impacts

    def get_unit_emissions(self):
        """Get the emissions of the electricity supply authority.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            The emissions of the electricity supply authority.
        """
        self.update_inventory_records()

        return self.unit_emissions

    def get_scenario(self):
        """Get the elecetricity consumption scenario."""
        return self.scenario

    def get_declared_unit(self):
        """Get the declared unit of the impacts.

        Returns
        -------
        ~pod_lca.units.Unit
            Declared unit
        """
        return self.declared_unit

    # ================================
    # Methods
    # ================================
    def pick_region(
        self, regions, impact_database, impact_category=config["setup"]["impacts"]["PRIMARY_IMPACT_CATEGORY"]
    ):
        """Pick the region with the highest impact from a list of regions.

        Parameters
        ----------
        regions : list of str
            List of regions to choose from.
        impact_data : pandas.DataFrame
            DataFrame containing impact data for the regions.
        impact_category : str
            The impact category to consider for the selection.

        Returns
        -------
        str
            The region with the highest impact.
        """
        consumption_mix = self.get_consumption_mix()

        impact_dict = {}
        for region in regions:
            impact_dict[region] = 0
            for technology, percentage in consumption_mix.items():
                data_entry = impact_database.get_data_entry(region, technology)
                conversion_factor = data_entry[impact_database.get_unit_key()].convert_to(WATT_HOUR)
                impact = data_entry[impact_category] * conversion_factor / data_entry[impact_database.get_qty_key()]
                impact_dict[region] += impact * percentage

        region_selected = max(impact_dict, key=impact_dict.get)

        log(
            f"Of {regions} considered, {region_selected} is picked as the most conservative, considering {impact_category} impact.",
            "Info",
        )

        return region_selected

    def update_inventory_records(self):
        """Set the impacts of the electricity supply authority."""
        temporal_data = CambiumData.from_geographical_scope(self.get_geographical_scope(), self.get_location())
        energy_mix = temporal_data.get_mix(
            self.get_year(),
            DataImporter.csv_to_list(
                config["file_paths"]["electricity"]["ELECTRICITY_TECHNOLOGIES"], "electricity technology"
            ),
            self.get_scenario(),
        )
        self.set_consumption_mix(energy_mix)
        self.set_electricity_producers(self.get_geographical_scope())

        temporal_data.delete_data()

        self.unit_impacts.clear_qty()
        self.unit_emissions.clear_qty()
        supply_unit = self.get_declared_unit()
        for technology, percentage in self.get_consumption_mix().items():
            if percentage > 0.0:
                if technology in self.electricity_producers:
                    production_unit = self.electricity_producers[technology].get_declared_unit()
                    conversion_factor = production_unit.convert_to(supply_unit)

                    self.unit_impacts += (
                        self.electricity_producers[technology].get_unit_impacts() * conversion_factor * percentage
                    )
                    self.unit_emissions += (
                        self.electricity_producers[technology].get_unit_emissions() * conversion_factor * percentage
                    )

        return self
    
    def get_inventories_in_bulk_for_years(self, years):
        """ Get inventories for a range of years.

        Parameters
        ----------
        years : list of int
            Years of electricity consumption.

        Returns
        -------
        ~pandas.DataFrame
            DataFrame of impacts by year.      
        ~pandas.DataFrame
            DataFrame of emissions by year.  
        """
        technologies = DataImporter.csv_to_list(config["file_paths"]["electricity"]["ELECTRICITY_TECHNOLOGIES"], "electricity technology")
        impact_headers = list(config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"].keys())
        emission_headers = list(config["setup"]["INVENTORY_ITEMS"]["EMISSION_INVENTORIES"].keys())
        inventory_headers = impact_headers + emission_headers

        geographical_scope = self.get_geographical_scope()
        location = self.get_location()

        # get energy production mix
        temporal_data = CambiumData.from_geographical_scope(geographical_scope, location)
        energy_mix = temporal_data.get_mix_in_bulk_years(
            years,
            technologies,
            self.get_scenario(),
        )

        # get impacts by production technology
        if  geographical_scope == "National":
            impact_data_df = DataImporter.csv_to_pandas(config["file_paths"]["electricity"]["ELECTRICITY_IMPACT_NATIONAL_DATA"])
        elif (geographical_scope == "Regional") or (geographical_scope == "Local"):
            impact_data_df = DataImporter.csv_to_pandas(config["file_paths"]["electricity"]["ELECTRICITY_IMPACT_REGIONAL_DATA"])

            region = location.get_ferc_region()
            if len(region) == 0:
                raise KeyError(f"FERC region not found for location: {location.get_zip()}.")
            elif len(region) == 1:
                region = region[0]
            else:
                region = self.pick_region(region, self.impact_database_regional)

            impact_data_df = impact_data_df[impact_data_df['Region'] == region].drop("Region", axis=1)

        # unit conversions
        impact_data_df['Conversion factor'] = 0.0
        supply_unit = self.get_declared_unit()
        for index, row in impact_data_df.iterrows():
            production_unit = UNITS_MAP[row["Unit"]]
            impact_data_df.at[index, 'Conversion factor'] = production_unit.convert_to(supply_unit) / row["Qty"]
        
        # make impact matrix
        impact_data_df.set_index('Technology Type', inplace=True)
        inventories_df = impact_data_df.reindex(columns=inventory_headers, fill_value=0.0)

        impact_matrix = inventories_df.loc[technologies, impact_headers].mul(impact_data_df['Conversion factor'], axis=0)
        emission_matrix = inventories_df.loc[technologies, emission_headers].mul(impact_data_df['Conversion factor'], axis=0)

        return energy_mix.dot(impact_matrix), energy_mix.dot(emission_matrix)

    def get_impact_distribution(self):
        """Get the distribution of the electricity supply authority.

        Returns
        -------
        :class:`list` of :class:`~pod_lca.impacts.Impacts`
            Impact objects representing the distribution of the impacts.
        :class:`list` of :class:`int`
            List of weights for each impact object in the distribution.

        Raises
        ------
        ValueError
            Geographical scope of electricity supply is not recognized.
        """
        year = self.get_year()

        # impacts by technology
        if self.impact_database_national is None:
            self.impact_database_national = ElectricityImpactsDatabase.new("Electricity - National", " National")
            self.impact_database_national.set_data(
                config["file_paths"]["electricity"]["ELECTRICITY_IMPACT_NATIONAL_DATA"]
            )
        impact_database = self.impact_database_national
        country_code = (
            self.get_location().get_country_code()
            if self.get_location() is not None
            else config["setup"]["electricity"]["DEFAULT_COUNTRY_CODE"]
        )

        # set regionality
        regions_map = DataImporter.json_to_dict(config["file_paths"]["electricity"]["CAMBIUM_REGIONS_MAP"])
        if self.get_geographical_scope() == "National":
            geographical_scope = "Regional"
            regions_list = list(regions_map[country_code].keys())

        elif self.get_geographical_scope() == "Regional":
            geographical_scope = "Local"
            region = self.get_location().get_cambium_gea_region() if self.get_location() is not None else None
            regions_list = regions_map[country_code][region]

        elif self.get_geographical_scope() == "Local":
            log("Data on impact data variability available at local level.", "info")
            return [self.get_unit_impacts()]
        else:
            raise ValueError("Geographical scope of electricity supply is not recognized.")

        # create data points
        impact_distribution = []
        electricity_loads = []
        for region in regions_list:
            temporal_data = CambiumData.from_geographical_scope(geographical_scope, region)
            energy_mix = temporal_data.get_mix(
                year,
                DataImporter.csv_to_list(
                    config["file_paths"]["electricity"]["ELECTRICITY_TECHNOLOGIES"], "electricity technology"
                ),
                self.get_scenario(),
            )
            electricity_load = temporal_data.get_load(year, self.get_scenario())
            temporal_data.delete_data()

            impact_obj = Impacts.from_parent(self)
            for technology, percentage in energy_mix.items():
                data_dict = impact_database.get_data_entry(country_code, technology)
                impact_data_dict = {
                    cat: impact for cat, impact in data_dict.items() if cat in impact_obj.get_categories()
                }
                tmp_impact_obj = Impacts.from_dict(impact_data_dict)
                impact_obj += tmp_impact_obj * percentage

            impact_distribution.append(impact_obj)
            electricity_loads.append(electricity_load)

        weights = np_round((electricity_loads / sum(electricity_loads)) * 100)

        return impact_distribution, weights


if __name__ == "__main__":
    pass
