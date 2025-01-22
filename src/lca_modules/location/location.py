from geopy.geocoders import Nominatim
import pandas as pd

from lca_modules.location.data import CFS_DATA_PATH, FAF_DATA

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"


class Location:
    """
    Location object updates the location into subcategores.
    The geocoding is done using Nominatim (https://nominatim.org/release-docs/develop/) which looks up OpenStreetMap (https://www.openstreetmap.org/)

    Attributes
    ----------
    location_name : str.
        Name of the location.
    coords : tuple
        Location coordinate using WGS-84 coordinate system.
    zipcode : str
        Zipcode of the location (in the corresponding local system).
    city : str
        Name of the city the location is in.
    state : str
        Name of the state the location is in.
    country : str
        Name of the country the location is in.
    """
    def __init__(self):
        self.location_name = None
        self.coords = None
        self.zipcode = None
        self.city = None
        self.state = None
        self.country = None
        self.cfs_area = None
        self.faf_foreign = None

    def __str__(self):
        return f"{self.get_city()}, {self.get_state()} {self.get_zip()}, {self.get_country()} {self.get_cordinates()}"

    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_str(cls, string):
        """ Create location from name.
            The location data populated based on the centroid of the location prescribed.
        
            Parameters
            ----------
            string : str
                Free-form textual description or address (or part thereof) of the location.
        """

        location = cls()

        try:
            geolocator = Nominatim(user_agent="pod_lca2")

            location_data = geolocator.geocode(string)
            location.set_cordinates(location_data)

            location_data = geolocator.reverse(location.get_cordinates())

            location.set_zip(location_data)
            location.set_city(location_data)
            location.set_state(location_data)
            location.set_country(location_data)
            location.set_cfs_area()
            location.set_faf_foreign_region(string)

            return location

        except Exception as e:
            print(f"Error retrieving location data: {e}")        
    
    # ================================
    # Setters
    # ================================
    def set_name(self, name):
        """ Set name of the location.
        
            Parameters
            ----------
            location_name : str
                Name of the location
        
        """
        self.location_name = name

        return self

    def set_cordinates(self, geopy_location_nominatim):
        """ Set the coordinates of the location.

            Parameters
            ----------
            geopy_location_nominatim : <class 'geopy.location.Location'>
                Geopy location object from Nominatim
        """
        self.coords = geopy_location_nominatim.latitude, geopy_location_nominatim.longitude

        return self

    def set_zip(self, geopy_location):
        """ Set the zipcode of the location.

            Parameters
            ----------
            geopy_location : <class 'geopy.location.Location'>
                Geopy location object.
        """
        try:
            self.zipcode = geopy_location.raw['address']['postcode']
        except:
            self.zipcode = None

        return self
    
    def set_city(self, geopy_location):
        """ Set the city of the location.

            Parameters
            ----------
            geopy_location : <class 'geopy.location.Location'>
                Geopy location object.
        """
        try:
            self.city = geopy_location.raw['address']['city']
        except:
            self.city = None

        return self
    
    def set_state(self, geopy_location):
        """ Set the state of the location.

            Parameters
            ----------
            geopy_location : <class 'geopy.location.Location'>
                Geopy location object.
        """
        try:
            self.state = geopy_location.raw['address']['state']
        except:
            self.state = None

        return self

    def set_country(self, geopy_location_photon):
        """ Set the country of the location.

            Parameters
            ----------
            geopy_location_photon : <class 'geopy.location.Location'>
                Geopy location object from Photon
        """
        try:
            self.country = geopy_location_photon.raw['address']['country']
        except:
            self.country = None

        return self

    def set_cfs_area(self):
        """ Set the country of the location.
        """    
        try:
            df = pd.read_csv(CFS_DATA_PATH)
            state = self.get_state()

            if state:
                if state in df["State"].values:
                    self.cfs_area = df[df['State'] == state].iloc[0, 2]
                elif state in df["State_Initial"].values:
                    self.cfs_area = df[df['State_Initial'] == state].iloc[0, 2]
                else:
                    self.cfs_area = None
            else:
                self.cfs_area = None

            return self.cfs_area

        except:
            self.cfs_area = None

        return self

    def set_faf_foreign_region(self, location):
        """ Set the FAF region (foreign) of the location.
        """  
        #TODO: need a more comprehensive way to do this (e.g., consider bounding boxes of the regions and check if location cooridinate is inside)
        if location in FAF_DATA.keys(): 
            
            self.faf_foreign = FAF_DATA[location]

            return self.faf_foreign
        
        return self

    # ================================
    # Getters
    # ================================
    def get_location_name(self):
        """ Retrieve the location name.

            Returns
            -------
            str
                Name of the location.
        """
        return self.location_name

    def get_cordinates(self):
        """ Retrieve the coordinates of the location.

            Returns
            -------
            tuple
                 (latitude, longitude).
        """
        return self.coords
    
    def get_zip(self):
        """ Retrieve the zipcode of the location.

            Returns
            -------
            str
                Name of the zipcode.
        """
        return self.zipcode
    
    def get_city(self):
        """ Retrieve the city of the location.

            Returns
            -------
            str
                Name of the city.
        """
        return self.city
     
    def get_state(self):
        """ Retrieve the state of the location.

            Returns
            -------
            str
                Name of the state.
        """
        return self.state

    def get_country(self):
        """ Retrieve the country of the location.

            Returns
            -------
            str
                Name of the country.
        """
        return self.country

    def get_egrid(self):

        #TODO we have to find a dataset for this
        pass


    def get_cfs_area(self):
        """ Get the Comodity Flow Survey (CFS) area of the location.

            Returns
            -------
            str
                Name of the Comodity Flow Survey (CFS) area.        
        """          
        return self.cfs_area

    def get_faf_foreign_region(self):
        """ Set the FAF region (foreign) of the location.
        """  
        return self.faf_foreign

    def get_faf_domestic_region(self):

        pass #TODO we have to find a dataset for this

if __name__ == '__main__':

    # location_input = "Mexico"
    # location_obj = Location(location_input)
    
    # print (location_obj.get_faf_foreign_region(location_input))

    location_obj = Location.from_str("Architecture Hall, Washington")
    print(location_obj)

    # location_input = 98102
    # location_obj = Location(location_input)

    # print(f"State: {location_obj.get_state()}")
    # print(f"City: {location_obj.get_city()}")
    # print(f"Zipcode: {location_obj.get_zip()}")
    # print(f"Coordinates: {location_obj.get_cordinates()}")
    # print (f"Country: {location_obj.get_country()}")
    # print (f"CFS Area: {location_obj.get_cfs_area()}")