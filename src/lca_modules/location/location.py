from geopy.geocoders import Nominatim
from geopy.geocoders import Photon

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
        
        self.state = None
        self.city = None
        self.zipcode = None
        self.coords = None
        self.country = None
        self.get_location_info(location)
    
    def get_location_info(self, location):
        """
        process the location and update the location sub categories.

        Attributes
        ----------
        location : str.
            Any kind of address, city name, state name or a full address.
        """

        geolocator_ph = Photon(user_agent="pod_lca1")
        geolocator_no = Nominatim (user_agent="pod_lca2")

        location_data_ph = geolocator_ph.geocode(location)
        location_data_no = geolocator_no.geocode(location)

        if location_data_no.raw['addresstype'] == "city":
            self.city = location_data_no.raw['name']
        else:
            self.city = location_data_ph.raw['properties']['city']

        if location_data_no.raw['addresstype'] == "state":
            self.state = location_data_no.raw['name']
        else:
            self.state = location_data_ph.raw['properties']['state']

        try:
            self.zipcode = location_data_ph.raw['properties']['postcode']
        except:
            self.zipcode = None #TODO a zip code should be defined for each city

        self.coords = location_data_no.latitude, location_data_no.longitude

    
    def get_state(self):

        """ Retrieve the state of the location.

            Returns
            -------
            str
                Name of the state.
        """
        return self.state
    
    def get_city(self):

        """ Retrieve the city of the location.

            Returns
            -------
            str
                Name of the city.
        """
        return self.city
    
    def get_zip(self):

        """ Retrieve the zipcode of the location.

            Returns
            -------
            str
                Name of the zipcode.
        """
        return self.zipcode
    
    def get_cordinates(self):

        """ Retrieve the coordinates of the location.

            Returns
            -------
            tuple
                 (latitude, longitude).
        """
        return self.coords

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
        return self.coords


        #TODO Transportation region 
        #TODO End of life region


if __name__ == '__main__':

    location_input = "Seattle"
    location_obj = Location(location_input)
    
    print(f"State: {location_obj.get_state()}")
    print(f"City: {location_obj.get_city()}")
    print(f"Zipcode: {location_obj.get_zip()}")
    print(f"Coordinates: {location_obj.get_cordinates()}")