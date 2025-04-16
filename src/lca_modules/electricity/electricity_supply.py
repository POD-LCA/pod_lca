
from lca_modules.electricity.data_sources import NATIONAL_DATA, REGIONAL_DATA, LOCAL_DATA
from lca_modules.electricity.electricity_technologies import ELECTRICITY_TECHNOLOGIES
from lca_modules.electricity.electricity_producer import ElectricityProducer
from lca_modules.electricity.processs_cambium import CambiumData
from lca_modules.impacts.impacts import Impacts
from utilities.data_imports.csv import CSV_Importer
from utilities.units.common_units import WATT_HOUR   
from utilities.units.metric_prefixes import MEGA


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
    DEFAULT_REIGIONAL_RESOLUTION = 'National'
    DEFAULT_YEAR = 2025
    DEFAULT_SCENARIO = 'MidCase'
    DEFAULT_DECLARED_UNIT = MEGA * WATT_HOUR

    def __init__(self):
        self.name = None
        self.spatial_resolution = self.DEFAULT_REIGIONAL_RESOLUTION
        self.location = None
        self.consumption_mix = None
        self.electricity_producers = {}
        self.year = self.DEFAULT_YEAR
        self.scenario = self.DEFAULT_SCENARIO
        self.impacts = Impacts.from_parent(self)
        self.declared_unit = self.DEFAULT_DECLARED_UNIT

    def __str__(self):
        str = "="*75 + "\n" + f"Electricity Supply: {self.get_name()}\n" + "="*75 + "\n"
        str += f"Spatial resolution: {self.get_spatial_resolution()}\n"
        str += f"Year: {self.get_year()}\n"

        return str

    @classmethod
    def from_location(cls, location, regional_resolution=DEFAULT_REIGIONAL_RESOLUTION, year=DEFAULT_YEAR):
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
        elec_supp_authority.set_spatial_resolution(regional_resolution)
        
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

        self.spatial_resolution = regional_resolution

        # Update consumption mix
        year = self.get_year()
        temporal_data = CambiumData.from_regional_resolution(regional_resolution, self.get_location())

        energy_mix = temporal_data.get_mix(year, ELECTRICITY_TECHNOLOGIES, self.get_scenario())
        self.set_consumption_mix(energy_mix, update_impacts=False)

        temporal_data.delete_data()

        # Get regionalised impact data
        if (regional_resolution== 'National') or (regional_resolution== 'Regional') or (regional_resolution== 'Local'):
            df = CSV_Importer.import_as_pandas(NATIONAL_DATA)
            country = self.get_location().get_country()
            country_code = self.get_location().get_country_code()
            if country_code in df['Country code'].values:
                impact_data = df[df['Country code'] == country_code].drop(['Country code', 'Country'], axis='columns')
            else:
                raise KeyError(f"{country} ({country_code}) not in the dataset provided in file: '{NATIONAL_DATA}.'")                

        elif regional_resolution == 'Regional': # TODO: Are we getting regional and local impact data disagregated by the technology?
            pass
            # self.get_location().set_ferc_region() # TODO: make it possible to pass this method as a variable
            # region = self.get_location().get_ferc_region()
            # df = CSV_Importer.import_as_pandas(REGIONAL_DATA)

            # if region in df['Region'].values:
            #     impact_data_dict = df[df['Region'] == region].drop('Region', axis='columns').squeeze().to_dict()
            # else:
            #     raise KeyError(f"{region} not in the dataset provided in file: '{REGIONAL_DATA}.'")
            
            
        elif regional_resolution == 'Local':
            pass
            # self.get_location().set_balancing_authority() # TODO: make it possible to pass this method as a variable
            # area = self.get_location().get_balancing_authority()
            # df = CSV_Importer.import_as_pandas(LOCAL_DATA)

            # if area in df['Area'].values:
            #     impact_data_dict = df[df['Area'] == area].drop('Area', axis='columns').squeeze().to_dict()
            # else:
            #     raise KeyError(f"{area} not in the dataset provided in file: '{LOCAL_DATA}.'")
            
        else:
            raise ValueError("Regional resolution of electricity supply is not recognized.")
        
        # update producers
        for key in energy_mix.keys():
            if key in self.electricity_producers:
                producer = self.electricity_producers[key]
            else:
                producer = ElectricityProducer.from_technology_year(key, self.get_year())
                self.electricity_producers[key] = producer

            impact_data_dict = impact_data[impact_data['Technology Type'] == key].drop(['Technology Type'], axis='columns').squeeze().to_dict()
             
            impact_obj = Impacts.from_parent(producer)
            impact_obj.update_impact_qty(impact_data_dict)

            producer.set_impacts(impact_obj)

        self.update_impacts()

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

        energy_mix = temporal_data.get_mix(year, ELECTRICITY_TECHNOLOGIES, self.get_scenario())
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

        energy_mix = temporal_data.get_mix(self.get_year(), ELECTRICITY_TECHNOLOGIES, self.get_scenario())
        self.set_consumption_mix(energy_mix, update_impacts=False)

        self.update_impacts()

        temporal_data.delete_data()

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
    def update_impacts(self):
        """ Set the impacts of the electricity supply authority.
        """

        impact_obj = self.get_impacts()
        impact_obj.clear_impact_qty()
        for technology, percentage in self.get_consumption_mix().items():
            if technology in self.electricity_producers:
                impact_obj += self.electricity_producers[technology].get_impacts() * percentage

        # FIXME: update the existing object

        # #TODO: Once the advanced method is implemented, this process will be simplified
        # if update_region:
        #     region_type = self.get_spatial_resolution()

        #     if region_type== 'National':
        #         country = self.get_location().get_country()
        #         country_code = self.get_location().get_country_code()
        #         df = CSV_Importer.import_as_pandas(NATIONAL_DATA)

        #         if country_code in df['Country code'].values:
        #             impact_data_dict = df[df['Country code'] == country_code].drop(['Country code', 'Country'], axis='columns').squeeze().to_dict()
        #         else:
        #             raise KeyError(f"{country} ({country_code}) not in the dataset provided in file: '{NATIONAL_DATA}.'")
                
        #         self.set_region_name(country + '(' + country_code + ')')

        #     elif region_type == 'Regional':
        #         self.get_location().set_ferc_region() # TODO: make it possible to pass this method as a variable
        #         region = self.get_location().get_ferc_region()
        #         df = CSV_Importer.import_as_pandas(REGIONAL_DATA)

        #         if region in df['Region'].values:
        #             impact_data_dict = df[df['Region'] == region].drop('Region', axis='columns').squeeze().to_dict()
        #         else:
        #             raise KeyError(f"{region} not in the dataset provided in file: '{REGIONAL_DATA}.'")
                
        #         self.set_region_name(region)
                
        #     elif region_type == 'Local':
        #         self.get_location().set_balancing_authority() # TODO: make it possible to pass this method as a variable
        #         area = self.get_location().get_balancing_authority()
        #         df = CSV_Importer.import_as_pandas(LOCAL_DATA)

        #         if area in df['Area'].values:
        #             impact_data_dict = df[df['Area'] == area].drop('Area', axis='columns').squeeze().to_dict()
        #         else:
        #             raise KeyError(f"{area} not in the dataset provided in file: '{LOCAL_DATA}.'")
                
        #         self.set_region_name(area)
                
        #     else:
        #         raise ValueError("Regional resolution of electricity supply is not recognized.")
        
        #     impact_obj = Impacts.from_parent(self)
        #     impact_obj.update_impact_qty(impact_data_dict)

        #     self.impacts = impact_obj

        # if update_mix:
        #     pass
        #     # TODO: calculate the impacts based on the consumption year (defaulting values when not set)
        #     # TODO: generating mix impacts from NETL data


        return self

if __name__ == '__main__':
    pass