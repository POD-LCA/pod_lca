from geopy.geocoders import Nominatim
from geopy.geocoders import Photon
import pandas as pd

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"




class Location:
    """
    Location object updates the location into subcategores.

    Attributes
    ----------
    location : str.
        Any kind of address, city name, state name or a full address.
    """
    def __init__(self, location):
        
        self.location = location
        self.state = None
        self.city = None
        self.zipcode = None
        self.coords = None
        self.country = None
        self.cfs_area = None
        self.faf_foreign = None
        self.location_data_ph = None
        self.location_data_no = None
        self.get_location_info(location)
    
    def get_location_info(self, location):
        """
        process the location and update the location sub categories.

        Attributes
        ----------
        location : str.
            Any kind of address, city name, state name or a full address.
        """

        try:
            geolocator_ph = Photon(user_agent="pod_lca1")
            geolocator_no = Nominatim(user_agent="pod_lca2")

            self.location_data_ph = geolocator_ph.geocode(location)
            self.location_data_no = geolocator_no.geocode(location)

        except Exception as e:
            print(f"Error retrieving location data: {e}")

    def get_location(self):

        """ Retrieve the location.

            Returns
            -------
            str
                Name of the location.
        """
        return self.location

    def get_state(self):

        """ Retrieve the state of the location.

            Returns
            -------
            str
                Name of the state.
        """
        if self.location_data_no.raw['addresstype'] == "state":
            self.state = self.location_data_no.raw['name']
        
        elif self.location_data_no.raw['addresstype'] != "state":
            try:
                self.state = self.location_data_ph.raw['properties']['state']
            except:
                self.state = None

        return self.state
    
    def get_city(self):

        """ Retrieve the city of the location.

            Returns
            -------
            str
                Name of the city.
        """

        if self.location_data_no.raw['addresstype'] == "city":
            self.city = self.location_data_no.raw['name']

        elif self.location_data_no.raw["addresstype"] != "city":
            try:
                self.city = self.location_data_ph.raw['properties']['city']
            except:
                self.city = None

        return self.city
    
    def get_zip(self):

        """ Retrieve the zipcode of the location.

            Returns
            -------
            str
                Name of the zipcode.
        """
        try:
            self.zipcode = self.location_data_ph.raw['properties']['postcode']
        except:
            self.zipcode = None #TODO a zip code should be defined for each city

        return self.zipcode
    
    def get_cordinates(self):

        """ Retrieve the coordinates of the location.

            Returns
            -------
            tuple
                 (latitude, longitude).
        """
        self.coords = self.location_data_no.latitude, self.location_data_no.longitude

        return self.coords

    def get_country(self):

        """ Retrieve the country of the location.

            Returns
            -------
            str
                Name of the country.
        """
        try:
            self.country = self.location_data_ph.raw['properties']['country']
        except:
            self.country = None 

        return self.country

    def get_egrid(self):

        #TODO we have to find a dataset for this
        pass


    def get_cfs_area(self):
        
        try:
            df = pd.read_csv("data\\location_cfs.csv")
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

    def get_faf_foreign_region(self, location):

        df_faf = {"Canada": 801, "Mexico": 802, "Rest of Americas": 803,
              "Europe": 804, "Africa": 805, "SW & Central Asia": 806,
              "Eastern Asia": 807, "SE Asia & Oceania": 808}
        
        if location in df_faf.keys():
            
            self.faf_foreign = df_faf[location]

            return self.faf_foreign

    def get_faf_domestic_region(self, location):

        pass #TODO we have to find a dataset for this

if __name__ == '__main__':

    # location_input = "Mexico"
    # location_obj = Location(location_input)
    
    # print (location_obj.get_faf_foreign_region(location_input))

    location_input = "7530 164th Ave NE, Redmond, WA 98052"
    location_obj = Location(location_input)

    print(f"State: {location_obj.get_state()}")
    print(f"City: {location_obj.get_city()}")
    print(f"Zipcode: {location_obj.get_zip()}")
    print(f"Coordinates: {location_obj.get_cordinates()}")
    print (f"Country: {location_obj.get_country()}")
    print (f"CFS Area: {location_obj.get_cfs_area()}")