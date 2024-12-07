from geopy.geocoders import Nominatim
from geopy.geocoders import Photon

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"




class Location:
    
    def __init__(self, location):

        self.location = location
        self.geolocator_ph = Photon(user_agent="geoapiExercises")
        self.geolocator_no = Nominatim (user_agent="pod_lca")
        self.state = None
        self.city = None
        self.zipcode = None
        self.coords = None
        self.country = None

        self.get_location_info()
    
    def get_location_info(self):

        location_data_ph = self.geolocator_ph.geocode(self.location)
        location_data_no = self.geolocator_no.geocode(self.location)


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

    
    def loc_to_state(self):
        return self.state
    
    def loc_to_city(self):
        return self.city
    
    def loc_to_zip(self):
        return self.zipcode
    
    def loc_to_cordinates(self):
        return self.coords

    def loc_to_egrid(self):
        return self.coords  #TODO we have to find a dataset for this

if __name__ == '__main__':

    location_input = "seattle"
    location_obj = Location(location_input)
    
    print(f"State: {location_obj.loc_to_state()}")
    print(f"City: {location_obj.loc_to_city()}")
    print(f"Zipcode: {location_obj.loc_to_zip()}")
    print(f"Coordinates: {location_obj.loc_to_cordinates()}")