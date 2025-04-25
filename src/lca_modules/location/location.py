from geopy.geocoders import Nominatim
import pandas as pd

from lca_modules.location.data import CFS_DATA_PATH, FAF_DATA, FERC_BA_MAP_PATH, BA_ZIPCODE_MAP_PATH, GEA_ZIPCODE_MAP_PATH, REEDS_BA_ZIPCODE_MAP_PATH

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
    regionality : str
        Regionality of the location (Local, Regional, National).
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
    country_code : str
        Country code from ISO 3166-1 Codes for the representation of names of countries and their subdivisions – Part 1: Country code
    """
    def __init__(self):
        self.location_name = None
        self.regionality = None
        self.coords = None
        self.zipcode = None
        self.city = None
        self.state = None
        self.country = None
        self.cfs_area = None
        self.faf_foreign = None
        self.ferc_region = None
        self.balancing_authority = None
        self.cambium_gea_region = None
        self.reeds_balancing_area = None

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
            geolocator = Nominatim(user_agent="pod_lca")

            location_data = geolocator.geocode(string, featuretype=['settlement', 'city', 'town', 'village', 'county', 'state', 'country'], language='en', addressdetails=True, extratags=True) 
            location.set_regionality(location_data)
            location.set_cordinates(location_data)

            location_data = geolocator.reverse(location.get_cordinates(), addressdetails=True, zoom=15, language='en') # zoom level 14 = neighbourhood

            location.set_zip(location_data)
            location.set_city(location_data)
            location.set_state(location_data)
            location.set_country(location_data)
            location.set_country_code(location_data)
            location.set_cfs_area()
            location.set_faf_foreign_region(string)

            return location

        except Exception as e:
            print(f"Error retrieving location data: {e}") 

    @classmethod
    def from_US_zip(cls, zipcode, set_all_location_data=False):
        """ Create location from US zipcode.
            The location data populated based on the centroid of the area represented by the zipcode.
        
            Parameters
            ----------
            zipcode : str
                Zipcode of the location.
        """
        location = cls()

        location.country = "USA"
        location.country_code = "US"
        location.zipcode = zipcode
        location.regionality = 'Local'

        if set_all_location_data:
            try:
                string = zipcode + ", USA"
                geolocator = Nominatim(user_agent="pod_lca")

                location_data = geolocator.geocode(string, featuretype=['settlement', 'city', 'town', 'village', 'county', 'state', 'country'], language='en', addressdetails=True, extratags=True) 
                location.set_regionality(location_data)
                location.set_cordinates(location_data)

                location_data = geolocator.reverse(location.get_cordinates(), addressdetails=True, zoom=15, language='en') # zoom level 14 = neighbourhood

                location.set_city(location_data)
                location.set_state(location_data)
                location.set_cfs_area()
                location.set_faf_foreign_region(string)

            except Exception as e:
                print(f"Error retrieving location data: {e}")

        return location
    
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

    def set_regionality(self, geopy_location_nominatim):
        """ Set the regionality of the location.

            Parameters
            ----------
            geopy_location_nominatim : <class 'geopy.location.Location'>
                Geopy location object from Nominatim
        """
        local_type = ['postcode', 'county', 'municipality', 'city', 'town', 'village', 'city_district', 'district', 'borough', 'suburb', 'subdivision', 'hamlet', 'croft', 'neighbourhood', 'allotments', 'quarter']
        regional_type = ['region', 'state', 'province', 'state_district']
        national_type = ['country', 'country_code']

        if geopy_location_nominatim.raw['addresstype'] in local_type:
            self.regionality = 'Local'
        elif geopy_location_nominatim.raw['addresstype'] in regional_type:
            self.regionality = 'Regional'
        elif geopy_location_nominatim.raw['addresstype'] in national_type:
            self.regionality = 'National'
        else:
            raise ValueError("Regionality not recognized")

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
            if 'postcode' in geopy_location.raw['address']:
                self.zipcode = geopy_location.raw['address']['postcode']
            else:
                self.zipcode = self.get_closest_zip(geopy_location)
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
    
    def set_country_code(self, geopy_location_photon):
        """ Set the country code of the location.

            Parameters
            ----------
            geopy_location_photon : <class 'geopy.location.Location'>
                Geopy location object from Photon
        """
        try:
            self.country_code = geopy_location_photon.raw['address']['country_code'].upper()
        except:
            self.country_code = None

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
    
    def set_ferc_region(self):
        """ Set the Federal Energy Regulatory Commission (FERC) Region."""

        df = pd.read_csv(FERC_BA_MAP_PATH, on_bad_lines='warn')
        balancing_authority = self.get_balancing_authority()
        if balancing_authority is None:
            self.set_balancing_authority()
            balancing_authority = self.get_balancing_authority()

        ferc_region = df[df['balancing_authority'].isin(balancing_authority)]['FERC_region'].unique()

        self.ferc_region = ferc_region
    
        return self
    
    def set_balancing_authority(self):
        """ Set the Balancing Authority."""

        df = pd.read_csv(BA_ZIPCODE_MAP_PATH, on_bad_lines='warn')
        zipcode = self.get_zip()
        if df['zip_code'].dtype == 'int64':
            zipcode = int(zipcode)

        balancing_authority = df[df['zip_code'] == zipcode]['balancing_authority'].unique()

        if len(balancing_authority) == 0: # If no balancing authority is found, try to find it by adding leading zeros to the zipcode
            if df['zip_code'].dtype == 'O': 
                trail_zeros = '0' * (5 - len(zipcode))
                balancing_authority = df[df['zip_code'] == trail_zeros + zipcode]['balancing_authority'].unique()

        self.balancing_authority = balancing_authority
            
        return self
    
    def set_cambium_gea_region(self):
        """ Set the Cambium Generation and Emissions Assessment (GEA) region."""

        df = pd.read_csv(GEA_ZIPCODE_MAP_PATH, on_bad_lines='warn')
        zipcode = self.get_zip()
        if df['zip_code'].dtype == 'int64':
            zipcode = int(zipcode)

        cambium_gea_region = df[df['zip_code'] == zipcode]['cambium_gea'].unique()

        if len(cambium_gea_region) == 0: # If no cambium GEA is found, try to find it by adding leading zeros to the zipcode
            if df['zip_code'].dtype == 'O': 
                trail_zeros = '0' * (5 - len(zipcode))
                cambium_gea_region = df[df['zip_code'] == trail_zeros + zipcode]['cambium_gea'].unique()

        self.cambium_gea_region = cambium_gea_region[0]
            
        return self
    
    def set_reeds_balancing_area(self):
        """ Set the Balancing Area under the Get the Regional Energy Deployment System (ReEDS)."""

        df = pd.read_csv(REEDS_BA_ZIPCODE_MAP_PATH, on_bad_lines='warn')
        zipcode = self.get_zip()
        if df['zip_code'].dtype == 'int64':
            zipcode = int(zipcode)

        balancing_area = df[df['zip_code'] == zipcode]['reeds_ba'].unique()

        if len(balancing_area) == 0: # If no balancing area is found, try to find it by adding leading zeros to the zipcode
            if df['zip_code'].dtype == 'O': 
                trail_zeros = '0' * (5 - len(zipcode))
                balancing_area = df[df['zip_code'] == trail_zeros + zipcode]['reeds_ba'].unique()

        self.reeds_balancing_area = balancing_area[0]
            
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
    
    def get_regionality(self):
        """ Retrieve the regionality of the location.

            Returns
            -------
            str
                Regionality of the location.
        """

        return self.regionality

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

    def get_country_code(self):
        """ Retrieve the country code of the location.

            Returns
            -------
            str
                Country code from IS) 3166-1.
        """
        return self.country_code
    
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
        """ Get the FAF region (foreign) of the location.
        """  
        return self.faf_foreign

    def get_faf_domestic_region(self):

        pass #TODO we have to find a dataset for this

    def get_ferc_region(self):
        """ Get the Federal Energy Regulatory Commission (FERC) Region."""

        return self.ferc_region

    def get_balancing_authority(self):
        """ Get the balancing authority."""

        return self.balancing_authority
    
    def get_cambium_gea_region(self):
        """ Get Cambium Generation and Emissions Assessment (GEA) region."""

        return self.cambium_gea_region
    
    def get_reeds_balancing_area(self):
        """ Get the Regional Energy Deployment System (ReEDS) balancing area."""

        return self.reeds_balancing_area
        
    # ================================
    # Methods
    # ================================
    @staticmethod
    def get_closest_zip(geopy_location, max_attempts=10, step=1):
        """ Get the zipcode of the location.

            Parameters
            ----------
            geopy_location : <class 'geopy.location.Location'>
                Geopy location object.
            max_attempts: int
                Maximum number of attempts to find the closest zip code
            step : float
                Step size in km (approx.)
        """
        geolocator = Nominatim(user_agent="pod_lca")

        if 'county' in geopy_location.raw['address']:
            query = geopy_location.raw['address']['county']
            geopy_location = geolocator.geocode(query, exactly_one=True)
                    
            lat = geopy_location.latitude
            lon = geopy_location.longitude
        else:
            lat = geopy_location.latitude
            lon = geopy_location.longitude
        
        for i in range(max_attempts):
            lat_offset = 0.01 * step * (i // 2) * (-1 if i % 2 else 1)
            lon_offset = 0.01 * step * (i // 2) * (-1 if i % 2 else 1)
            new_lat, new_lon = lat + lat_offset, lon + lon_offset

            geopy_location = geolocator.reverse((new_lat, new_lon), exactly_one=True, addressdetails=True, zoom=18, language='en')

            if geopy_location and 'postcode' in geopy_location.raw['address']:
                return geopy_location.raw['address']['postcode']
        
        return "ZIP code not found within search range"
    
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