
from lca_modules.electricity import DEFAULT_YEAR, DEFAULT_SCENARIO, DEFAULT_DECLARED_UNIT, DEFAULT_REIGIONAL_RESOLUTION, DEFAULT_COUNTRY, DEFAULT_COUNTRY_CODE, ELECTRICITY_IMPACT_NATIONAL_DATA, ELECTRICITY_IMPACT_REGIONAL_DATA, CAMBIUM_REGIONS_MAP, ELECTRICITY_TECHNOLOGIES
from lca_modules.electricity.electricity_producer import ElectricityProducer
from lca_modules.electricity.processs_cambium import CambiumData
from lca_modules.impacts.impact_categories import PRIMARY_IMPACT_CATEGORY
from lca_modules.impacts.impacts import Impacts
from utilities.data_imports.csv import CSV_Importer

from numpy import round as np_round


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class ElectricitySupply:
    """ A class to represent an electricity supply authority.
    
        Attributes
        ----------
        name : str
            The name of the electricity supply authority.
        spatial_resolution : str
            Spatial resolution fo the electricity supply.
                'National': US average
                'Regional': FERC region
                'Local': Balancing Authority.
        location : Location Obj.
            The location of the electricity supply authority.
        consumption_mix : dict
            The consumption mix of the electricity supply authority.
        year : int
            The year of the electricity supply authority.
        impacts : Impacts Obj.
            The impacts of the electricity supply authority.

        NOTES
        -----
        1. Location, regionality, and year determines the consumption mix.
        2. location and regionality determines the impact by technology.
    """

    def __init__(self):
        self.name = None
        self.spatial_resolution = DEFAULT_REIGIONAL_RESOLUTION
        self.location = None
        self.consumption_mix = None
        self.electricity_producers = {}
        self.year = DEFAULT_YEAR
        self.scenario = DEFAULT_SCENARIO
        self.impacts = Impacts.from_parent(self)
        self.declared_unit = DEFAULT_DECLARED_UNIT

    def __str__(self):
        str = "="*75 + "\n" + f"Electricity Supply: {self.get_name()}\n" + "="*75 + "\n"
        str += f"Year: {self.get_year()}\n"
        str += f"Spatial resolution: {self.get_spatial_resolution()}\n"

        str += "-"*75 + "\n" + "Tecnology Mix:\n" 
        str += f"Scenario (cambium): {self.get_scenario()}\n"
        
        if self.get_spatial_resolution() == 'National':
            if self.get_location() is None:
                str += f"Country: {DEFAULT_COUNTRY}\n"
            else:
                str += f"Country: {self.get_location().get_country()}\n"
        elif self.get_spatial_resolution() == 'Regional':
            if self.get_location().get_cambium_gea_region() is not None:
                str += f"GEA Region: {self.get_location().get_cambium_gea_region()[0]}\n"
            else:
                str += f"GEA Region: {self.get_location().get_cambium_gea_region()}\n"
        elif self.get_spatial_resolution() == 'Local':
            if self.get_location().get_reeds_balancing_area() is not None:
                str += f"ReEDS BA: {self.get_location().get_reeds_balancing_area()[0]}\n"
            else:
                str += f"ReEDS BA: {self.get_location().get_reeds_balancing_area()}\n"

        str += "-"*75 + "\n" + "Impacts per technology:\n" 
        if self.get_spatial_resolution() == 'National':
            if self.get_location() is None:
                str += f"Country: {DEFAULT_COUNTRY}\n"
            else:
                str += f"Country: {self.get_location().get_country()}\n"
        elif self.get_spatial_resolution() == 'Regional':
            if self.get_location().get_ferc_region() is not None:
                str += f"FERC Region: {self.get_location().get_ferc_region()[0]}\n"
            else:
                str += f"FERC Region: {self.get_location().get_ferc_region()}\n"
        elif self.get_spatial_resolution() == 'Local':
            if self.get_location().get_ferc_region() is not None:
                str += f"FERC Region: {self.get_location().get_ferc_region()[0]}\n"
            else:
                str += f"FERC Region: {self.get_location().get_ferc_region()}\n"

        return str

    # ========================
    # Constructors
    # ========================
    @classmethod
    def from_location(cls, location, year=DEFAULT_YEAR):
        """ Create a new ElectricitySupplyAuthority object with the given location 
        
            Parameters
            ----------
            location : Location Obj.
                The location of the electricity supply authority.
            regional_resolution : str
                Regional resolution fo the electricity supply.
                    'National': US average
                    'Regional': FERC region
                    'Local': Balancing Authority.
            year : int
                Year of electricity consumption.
            
            Returns
            -------
            ElectricitySupplyAuthority
                A new ElectricitySupplyAuthority object with the given location.
        """

        elec_supp_authority = cls()

        elec_supp_authority.set_location(location)
        elec_supp_authority.set_year(year)
        if location is None:
            elec_supp_authority.set_spatial_resolution(DEFAULT_REIGIONAL_RESOLUTION)
        else:
            elec_supp_authority.set_spatial_resolution(location.get_regionality())
        
        return elec_supp_authority
    
    # ================================
    # Setters
    # ================================
    def set_name(self, name):
        """ Set the name of the electricity supply authority.
        
            Parameters
            ----------
            name : str
                The name of the electricity supply authority.
        """

        self.name = name

        return self
    
    def set_spatial_resolution(self, regional_resolution):
        """ Set the set_regional resolution of the electricity supply authority.
        
            Parameters
            ----------
            regional_resolution : str
                Regional resolution fo the electricity supply.
                    'National': US average
                    'Regional': FERC region
                    'Local': Balancing Authority.
        """
        location_resolution = self.get_location().get_regionality() if self.get_location() is not None else DEFAULT_REIGIONAL_RESOLUTION
        if ((location_resolution == 'National') and (regional_resolution == 'Local' or regional_resolution == 'Regional')) or ((location_resolution == 'Regional') and (regional_resolution == 'Local')):
            print ("Spatial resolution of electricity supply cannot be finer than that of location.")
            return self

        self.spatial_resolution = regional_resolution

        # Update consumption mix
        temporal_data = CambiumData.from_regional_resolution(regional_resolution, self.get_location())
        energy_mix = temporal_data.get_mix(self.get_year(), CSV_Importer.csv_to_list(ELECTRICITY_TECHNOLOGIES), self.get_scenario())
        self.set_consumption_mix(energy_mix, update_impacts=False)

        # Update impacts by technology
        self.set_electricity_producers(regional_resolution)

        self.update_impacts()

        temporal_data.delete_data()

        return self
    
    def set_location(self, location):
        """ Set the location of the electricity supply authority.
        
            Parameters
            ----------
            location : Location Obj.
                The location of the electricity supply authority.
        """

        self.location = location

        return self
    
    def set_consumption_mix(self, consumption_mix, update_impacts=True):
        """ Set the consumption mix of the electricity supply authority.
        
            Parameters
            ----------
            consumption_mix : dict
                The consumption mix of the electricity supply authority.
            update_impact : bool
                Update impacts if true.
        """
        self.consumption_mix = consumption_mix

        if update_impacts:
            self.update_impacts()

        return self
    
    def set_year(self, year):
        """ Set the year of the electricity supply authority.
            Changing the year changes the consumption mix based on Cambium data.
        
            Parameters
            ----------
            year : int
                The year of the electricity supply authority.
        """

        self.year = year

        temporal_data = CambiumData.from_regional_resolution(self.get_spatial_resolution(), self.get_location())

        energy_mix = temporal_data.get_mix(year, CSV_Importer.csv_to_list(ELECTRICITY_TECHNOLOGIES), self.get_scenario())
        self.set_consumption_mix(energy_mix, update_impacts=False)

        self.update_impacts()

        temporal_data.delete_data()

        return self
    
    def set_unit(self, unit):
        """ Set the declared unit of impacts.
        
            Parameters
            ----------
            unit : Unit Obj.
                Declared unit.
        """

        self.declared_unit = unit

        return self
    
    def set_scenario(self, scenario):
        """ Set scenario name. This will be used with cambium data.
        
            Parameters
            ----------
            scenario : str
                Electricity consmuption scenario considered: e.g., 'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'.
        """

        temporal_data = CambiumData.from_regional_resolution(self.get_spatial_resolution(), self.get_location())

        energy_mix = temporal_data.get_mix(self.get_year(), CSV_Importer.csv_to_list(ELECTRICITY_TECHNOLOGIES), scenario)
        self.set_consumption_mix(energy_mix, update_impacts=False)

        self.update_impacts()

        temporal_data.delete_data()
        self.scenario = scenario

        return self    

    def set_electricity_producers(self, regional_resolution):
        """ Set the electricity producers for a given technology mix and corresponding impact data.
        
            Parameters
            ----------
            regional_resolution : str
                Regional resolution fo the electricity supply.
                    'National': US average
                    'Regional': FERC region
                    'Local': Balancing Authority.        
        """

        # Get regionalised impact data
        if (regional_resolution== 'National'):
            df = CSV_Importer.import_as_pandas(ELECTRICITY_IMPACT_NATIONAL_DATA)
            country = self.get_location().get_country() if self.get_location() is not None else DEFAULT_COUNTRY
            country_code = self.get_location().get_country_code() if self.get_location() is not None else DEFAULT_COUNTRY_CODE
            if country_code in df['Country code'].values:
                impact_data = df[df['Country code'] == country_code].drop(['Country code', 'Country'], axis='columns')
            else:
                raise KeyError(f"{country} ({country_code}) not in the dataset provided in file: '{ELECTRICITY_IMPACT_NATIONAL_DATA}.'")                

        elif (regional_resolution == 'Regional') or (regional_resolution== 'Local'):
            df = CSV_Importer.import_as_pandas(ELECTRICITY_IMPACT_REGIONAL_DATA)

            if self.get_location().get_ferc_region() is None:
                self.get_location().set_ferc_region()

            region = self.get_location().get_ferc_region()
            if len(region) == 0:
                raise KeyError(f"FERC region not found for location: {self.get_location().get_zip()}.")
            elif len(region) == 1:
                region = region[0]
            else:
                impact_data = df[df['Region'].isin(region)]
                region =self.pick_region(region, impact_data)

            # if self.get_location().get_zip() in ['46779', '39481', '14013', '49006', '27556']:
            #     print(self.get_location().get_zip(), region)
            
            if region in df['Region'].values:
                impact_data = df[df['Region'] == region].drop('Region', axis='columns')
            else:
                raise KeyError(f"{region} not in the dataset provided in file: '{ELECTRICITY_IMPACT_REGIONAL_DATA}.'")
            
        else:
            raise ValueError("Regional resolution of electricity supply is not recognized.")

        # set producesrs and impacts
        for key in self.get_consumption_mix().keys():
            if key in self.electricity_producers:
                producer = self.electricity_producers[key]
            else:
                producer = ElectricityProducer.from_technology_year(key, self.get_year())
                self.electricity_producers[key] = producer

            impact_data_dict = impact_data[impact_data['Technology Type'] == key].drop(['Technology Type'], axis='columns').squeeze().to_dict()
             
            impact_obj = Impacts.from_parent(producer)
            impact_obj.update_impact_qty(impact_data_dict)

            producer.set_impacts(impact_obj)

        return self
    
    # ================================
    # Getters
    # ================================
    def get_name(self):
        """ Get the name of the electricity supply authority.
        
            Returns
            -------
            str
                The name of the electricity supply authority.
        """

        return self.name
    
    def get_spatial_resolution(self):
        """ Get the set regional resolution of the electricity supply authority.
        
            Returns
            -------
            str
                The set_regional_resolution of the electricity supply.
        """

        return self.spatial_resolution

    def get_location(self):
        """ Get the location of the electricity supply authority.
        
            Returns
            -------
            Location Obj.
                The location of the electricity supply authority.
        """

        return self.location
    
    def get_consumption_mix(self):
        """ Get the consumption mix of the electricity supply authority.
        
            Returns
            -------
            dict
                The consumption mix of the electricity supply authority.
        """

        return self.consumption_mix
    
    def get_year(self):
        """ Get the year of the electricity supply authority.
        
            Returns
            -------
            int
                The year of the electricity supply authority.
        """

        return self.year
    
    def get_impacts(self):
        """ Get the impacts of the electricity supply authority.
        
            Returns
            -------
            Impacts Obj.
                The impacts of the electricity supply authority.
        """

        return self.impacts
    
    def get_scenario(self):
        """ Get the elecetricity consumption scenario."""

        return self.scenario
    
    def get_unit(self):
        """ Get the declared unit of the impacts.
        
            Returns
            -------
            Unit Obj.
                Declared unit
        """

        return self.declared_unit
    
    # ================================
    # Methods
    # ================================
    def pick_region(self, regions, impact_data, impact_category=PRIMARY_IMPACT_CATEGORY):
        """ Pick the region with the highest impact from a list of regions.
        
            Parameters
            ----------
            regions : list of str
                List of regions to choose from.
            impact_data : DataFrame
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
        for item in regions:
            impact_dict[item] = 0
            for technology, percentage in consumption_mix.items():
                impact = impact_data[(impact_data['Region'] == item) & (impact_data['Technology Type'] == technology)][impact_category].values[0]
                impact_dict[item] += impact * percentage

        region_selected = max(impact_dict, key=impact_dict.get)

        print(f"Of {regions} considered, {region_selected} is picked as the most concervative, considering {impact_category} impact.")
        
        return region_selected


    def update_impacts(self):
        """ Set the impacts of the electricity supply authority.
        """

        impact_obj = self.get_impacts()
        impact_obj.clear_impact_qty()
        for technology, percentage in self.get_consumption_mix().items():
            if technology in self.electricity_producers:
                impact_obj += self.electricity_producers[technology].get_impacts() * percentage

        return self
    
    def get_impact_distribution(self):
        """ Get the distribution of the electricity supply authority.
        
            Returns
            -------
            list of Impact Obj.
                Impact objects representing the distribution of the impacts.
        """

        year = self.get_year()

        # impacts by technology
        df = CSV_Importer.import_as_pandas(ELECTRICITY_IMPACT_NATIONAL_DATA)
        country_code = self.get_location().get_country_code() if self.get_location() is not None else DEFAULT_COUNTRY_CODE
        if country_code in df['Country code'].values:
            impact_data_by_tech = df[df['Country code'] == country_code].drop(['Country code', 'Country'], axis='columns') 
        
        # set regionality
        regions_map = CSV_Importer.json_to_dict(CAMBIUM_REGIONS_MAP)
        if self.get_spatial_resolution() == 'National':
            regional_resolution = 'Regional'
            regions_list = list(regions_map[country_code].keys())

        elif self.get_spatial_resolution() == 'Regional':
            regional_resolution = 'Local' 
            region = self.get_location().get_cambium_gea_region() if self.get_location() is not None else None
            regions_list = regions_map[country_code][region]

        elif self.get_spatial_resolution() == 'Local':
            print("Data on impact data variability available at local level.")
            return [self.get_impacts()]
        else:
            raise ValueError("Regional resolution of electricity supply is not recognized.")

        # create data points
        impact_distribution = []
        electricity_loads = [] 
        for region in regions_list:
            temporal_data = CambiumData.from_regional_resolution(regional_resolution, region)
            energy_mix = temporal_data.get_mix(year, CSV_Importer.csv_to_list(ELECTRICITY_TECHNOLOGIES), self.get_scenario())
            electricity_load = temporal_data.get_load(year, CSV_Importer.csv_to_list(ELECTRICITY_TECHNOLOGIES), self.get_scenario())
            temporal_data.delete_data()

            impact_obj = Impacts.from_parent(self)
            for technology, percentage in energy_mix.items():
                impact_dict = impact_data_by_tech[impact_data_by_tech['Technology Type'] == technology].drop(['Technology Type'], axis='columns').squeeze().to_dict()
                tmp_impact_obj = Impacts.from_dict(impact_dict) 
                impact_obj += tmp_impact_obj * percentage

            impact_distribution.append(impact_obj)
            electricity_loads.append(electricity_load)

        weights = np_round((electricity_loads / sum(electricity_loads)) * 100)

        return impact_distribution, weights  


if __name__ == '__main__':
    pass
