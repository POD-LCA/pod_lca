
from lca_modules.electricity.data_sources import NATIONAL_DATA, REGIONAL_DATA, LOCAL_DATA
from lca_modules.electricity.electricity_technologies import ELECTRICITY_TECHNOLOGIES
from lca_modules.electricity.processs_cambium import CambiumData
from lca_modules.impacts.impacts import Impacts
from utilities.data_imports.csv import CSV_Importer


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class ElectricitySupplyAuthority:
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
    """

    def __init__(self):
        self.name = None
        self.spatial_resolution = None
        self.region_name = None
        self.location = None
        self.generation_mix = None
        self.consumption_mix = None
        self.year = None
        self.impacts = None


    def __str__(self):
        str = "="*75 + "\n" + f"Electricity Supply: {self.get_name()}\n" + "="*75 + "\n"
        str += f"Spatial resolution: {self.get_spatial_resolution()}\n"
        str += f"Region: {self.get_region_name()}\n"
        str += f"Year: {self.get_year()}\n"

        return str

    # TODO: [Q] Is there usefulness to keeping the consumption mix and generation mix data
    #       [Q] Is it prefered to run the calcs here (with mixes and raw impacts from generations) from base level rather than directly getting the impact factors from the tables provided

    @classmethod
    def from_location(cls, location, regional_resolution='National'):
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
            
            Returns
            -------
            ElectricitySupplyAuthority
                A new ElectricitySupplyAuthority object with the given location.
        """

        elec_supp_authority = cls()

        elec_supp_authority.set_location(location)
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
        self.set_impacts(update_region=True)

        return self
    
    def set_region_name(self, name):
        """ Set the name of the region.
        
            Parameters
            ----------
            name : str
                Name of the region based on the regional resolution
        """

        self.region_name = name
        
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
    
    def set_consumption_mix(self, consumption_mix):
        """ Set the consumption mix of the electricity supply authority.
        
            Parameters
            ----------
            consumption_mix : dict
                The consumption mix of the electricity supply authority.
        """

        self.consumption_mix = consumption_mix
        self.set_impacts(update_mix=True)

        return self
    
    def set_year(self, year):
        """ Set the year of the electricity supply authority.
        
            Parameters
            ----------
            year : int
                The year of the electricity supply authority.
        """

        self.year = year
        self.set_impacts(update_year=True)

        return self
    
    def set_impacts(self, update_region=False, update_mix=False, update_year=False):
        """ Set the impacts of the electricity supply authority.
    
        """

        if update_region:
            region_type = self.get_spatial_resolution()

            if region_type== 'National':
                country = self.get_location().get_country()
                country_code = self.get_location().get_country_code()
                df = CSV_Importer.import_as_pandas(NATIONAL_DATA)

                if country_code in df['Country code'].values:
                    impact_data_dict = df[df['Country code'] == country_code].drop(['Country code', 'Country'], axis='columns').squeeze().to_dict()
                else:
                    raise KeyError(f"{country} ({country_code}) not in the dataset provided in file: '{NATIONAL_DATA}.'")
                
                self.set_region_name(country + '(' + country_code + ')')

            elif region_type == 'Regional':
                self.get_location().set_ferc_region() # TODO: make it possible to pass this method as a variable
                region = self.get_location().get_ferc_region()
                df = CSV_Importer.import_as_pandas(REGIONAL_DATA)

                if region in df['Region'].values:
                    impact_data_dict = df[df['Region'] == region].drop('Region', axis='columns').squeeze().to_dict()
                else:
                    raise KeyError(f"{region} not in the dataset provided in file: '{REGIONAL_DATA}.'")
                
                self.set_region_name(region)
                
            elif region_type == 'Local':
                self.get_location().set_balancing_authority() # TODO: make it possible to pass this method as a variable
                area = self.get_location().get_balancing_authority()
                df = CSV_Importer.import_as_pandas(LOCAL_DATA)

                if area in df['Area'].values:
                    impact_data_dict = df[df['Area'] == area].drop('Area', axis='columns').squeeze().to_dict()
                else:
                    raise KeyError(f"{area} not in the dataset provided in file: '{LOCAL_DATA}.'")
                
                self.set_region_name(area)
                
            else:
                raise ValueError("Regional resolution of electricity supply is not recognized.")
        
            impact_obj = Impacts.from_parent(self)
            impact_obj.update_impact_qty(impact_data_dict)

            self.impacts = impact_obj

        if update_mix:
            pass
            # TODO: calculate the impacts based on the consumption year (defaulting values when not set)
            # TODO: generating mix impacts from NETL data

        if update_year: # TODO: test with different years
            region_type = self.get_spatial_resolution()
            year = self.get_year()
            temporal_data = CambiumData.from_regional_resolution(region_type)

            energy_mix = temporal_data.get_mix(year, ELECTRICITY_TECHNOLOGIES) # TODO: setting scenario

            self.set_consumption_mix(energy_mix)

        
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
    
    def get_region_name(self):
        """ Get the name of the region, corresponding to the regional resolution.
        
            Returns
            -------
            str
                Name of the region
        """

        return self.region_name

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

if __name__ == '__main__':
    
    from lca_modules.location.location import Location

    my_factory = Location.from_str("98102")

    electricity_supplier = ElectricitySupplyAuthority.from_location(my_factory, 'National')
    electricity_supplier.set_name("my electricity")
    print(electricity_supplier)

    impacts = electricity_supplier.get_impacts()
    print(impacts)

    electricity_supplier.set_year(2028)
