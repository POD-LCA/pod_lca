
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
        regional_resolution : str
            Regional resolution fo the electricity supply.
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
        self.regional_resolution = None
        self.location = None
        self.consumption_mix = None
        self.year = None
        self.impacts = None

    @classmethod
    def from_location(cls, location, regional_resolution):
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
        elec_supp_authority.set_type(type)
        elec_supp_authority.set_impacts()

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
    
    def set_regional_resolution(self, regional_resolution):
        """ Set the set_regional resolution of the electricity supply authority.
        
            Parameters
            ----------
            regional_resolution : str
                Regional resolution fo the electricity supply.
                    'National': US average
                    'Regional': FERC region
                    'Local': Balancing Authority.
            
        """

        self.regional_resolution = regional_resolution

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
        self.set_impacts()

        return self
    
    def set_year(self, year):
        """ Set the year of the electricity supply authority.
        
            Parameters
            ----------
            year : int
                The year of the electricity supply authority.
        """

        self.year = year
        self.set_impacts()

        return self
    
    def set_impacts(self):
        """ Set the impacts of the electricity supply authority.
    
        """

        # TODO: calculate the impacts based on the consumption mix and year (defaulting values when not set)

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
    
    def get_set_regional_resolution(self):
        """ Get the set regional_resolution of the electricity supply authority.
        
            Returns
            -------
            str
                The set_regional_resolution of the electricity supply.
        """

        return self.regional_resolution

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
    pass

    # try to create a new ElectricitySupplyAuthority object
    # reproduce 