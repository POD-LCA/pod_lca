__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class Location:
    """Location object updates the location into subcategores.
        The geocoding is done using Nominatim (https://nominatim.org/release-docs/develop/) which looks up OpenStreetMap (https://www.openstreetmap.org/)

    Attributes
    ----------
    location_name : str
        Name of the location.
    regionality : {'Local', 'Regional', 'National'}
        Regionality of the location.
    coords : tuple
        Location coordinate using WGS-84 coordinate system.
    zipcode : str
        ZIP code of the location (in the corresponding local system).
    city : str
        Name of the city the location is in.
    state : str
        Name of the state the location is in.
    state_abbr : str
        Standard abbreviation of the state name.
    country : str
        Name of the country the location is in.
    country_code : str
        Country code from ISO 3166-1 Codes for the representation of names of countries and their subdivisions – Part 1: Country code
    cfs_area : int
        Code of the Comodity Flow Survey (CFS) area.
    faf_foreign_name : str
        Name of the Freight Analysis Framework (FAF) region (foreign) corresponding to the location.
    faf_foreign_code : str
        Code of the Freight Analysis Framework (FAF) region (foreign) corresponding to the location.
    faf_domestic_codes : list of int
        Codes of the Freight Analysis Framework (FAF) region (domestic) corresponding to the location.
    us_coast : str
        US coast closest to the location.
    ferc_region : str
        Federal Energy Regulatory Commission (FERC) Region corresponding to the location.
    balancing_authority : str
        Balancing authority corresponding to the location.
    cambium_gea_region : str
        Cambium Generation and Emissions Assessment (GEA) region corresponding to the location.
    reeds_balancing_area : str
        Regional Energy Deployment System (ReEDS) balancing area corresponding to the location.
    """

    def __init__(self):
        self.location_name = None
        self.regionality = None
        self.coords = None
        self.zipcode = None
        self.city = None
        self.state = None
        self.state_abbr = None
        self.country = None
        self.country_code = None
        self.cfs_area = None
        self.faf_foreign_name = None
        self.faf_foreign_code = None
        self.faf_domestic_codes = None
        self.us_coast = None
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
        """Create location from name.
            The location data populated based on the centroid of the location prescribed.

        Parameters
        ----------
        string : str
            Free-form textual description or address (or part thereof) of the location.
        """
        location = cls()

        try:
            geolocator = Nominatim(user_agent="pod_lca", timeout=10)

            location_data = geolocator.geocode(string, language="en", addressdetails=True, extratags=True)
            location.set_regionality(location_data)
            location.set_cordinates(location_data)

            location_data = geolocator.reverse(
                location.get_cordinates(), addressdetails=True, zoom=15, language="en"
            )  # zoom level 14 = neighbourhood

            location.set_zip(location_data)
            location.set_city(location_data)
            location.set_state(location_data)
            location.set_country(location_data)
            location.set_country_code(location_data)

            # transportaion specific data
            if location.get_country_code() == "US":
                location.set_cfs_area()
                location.set_faf_domestic_region()
                location.set_us_coast()
            else:
                location.set_faf_foreign_region()

            return location

        except Exception as e:
            print(f"Error retrieving location data: {e}")

    @classmethod
    def from_US_zip(cls, zipcode, set_all_location_data=False):
        """Create location from US zipcode.
            The location data populated based on the centroid of the area represented by the ZIP code.

        Parameters
        ----------
        zipcode : str
            ZIP code of the location.
        set_all_location_data : bool
            If true, set location properties other than country and ZIP code.
        """
        location = cls()

        location.country = "USA"
        location.country_code = "US"
        location.zipcode = zipcode
        location.regionality = "Local"

        location.set_city(zip_code=zipcode)
        location.set_state(zip_code=zipcode)

        if set_all_location_data:
            try:
                string = zipcode + ", USA"
                geolocator = Nominatim(user_agent="pod_lca")

                location_data = geolocator.geocode(
                    string,
                    featuretype=["settlement", "city", "town", "village", "county", "state", "country"],
                    language="en",
                    addressdetails=True,
                    extratags=True,
                )
                location.set_regionality(location_data)
                location.set_cordinates(location_data)

                location_data = geolocator.reverse(
                    location.get_cordinates(), addressdetails=True, zoom=15, language="en"
                )  # zoom level 14 = neighbourhood

                location.set_cfs_area()
                location.set_faf_domestic_region()
                location.set_us_coast()

            except Exception as e:
                print(f"Error retrieving location data: {e}")

        return location

    @classmethod
    def from_US_state(cls, state, set_all_location_data=False):
        """Create location from US state.
            The location data populated based on the centroid of the area represented by the zipcode.

        Parameters
        ----------
        state : str
            US state name.
        set_all_location_data : bool
            If true, set location properties other than country, state, coast, CFS area, and FAF region.

        Raises
        ------
        ValueError
            State name not recognized as a US state.
        """
        location = cls()

        location.country = "USA"
        location.country_code = "US"

        us_states = DataImporter.json_to_dict(config["file_paths"]["location"]["US_STATES"])
        if state in us_states:
            location.state = state
            location.state_abbr = us_states[state]
        else:
            raise ValueError(f"{state} not recognized as a US State.")

        location.regionality = "Regional"
        location.set_zip(None, state=state)
        location.set_cfs_area()
        location.set_faf_domestic_region()
        location.set_us_coast()
        

        if set_all_location_data:
            try:
                string = state + ", USA"
                geolocator = Nominatim(user_agent="pod_lca")

                location_data = geolocator.geocode(
                    string,
                    featuretype=["settlement", "city", "town", "village", "county", "state", "country"],
                    language="en",
                    addressdetails=True,
                    extratags=True,
                )
                location.set_regionality(location_data)
                location.set_cordinates(location_data)
                location.set_zip(location_data)

                location_data = geolocator.reverse(
                    location.get_cordinates(), addressdetails=True, zoom=15, language="en"
                )  # zoom level 14 = neighbourhood
                location.set_city(location_data)

            except Exception as e:
                print(f"Error retrieving location data: {e}")

        return location

    @classmethod
    def from_faf_regions(cls, faf_region, set_all_location_data=False):
        """Create location from Freight Analysis Framework (FAF) region

        Parameters
        ----------
        faf_region : str
            FAF region name.
        set_all_location_data : bool
            If true, set location properties based on location coordinate.

        Raises
        ------
        ValueError
            FAF region not recognized
        """
        faf_foreign_regions = DataImporter.json_to_dict(config["file_paths"]["location"]["FAF_FOREIGN_REGION"])
        faf_foreign_regions_city = DataImporter.json_to_dict(
            config["file_paths"]["location"]["FAF_CITY_REPRESENTATION"]
        )

        if faf_region not in [None] + list(faf_foreign_regions.keys()):
            raise ValueError("FAF region not recognized.")

        location = cls()

        location.faf_foreign_code = faf_foreign_regions[faf_region]
        location.faf_foreign_name = faf_region
        location.location_name = faf_foreign_regions_city[location.faf_foreign_code]

        if set_all_location_data:
            try:
                string = location.location_name
                geolocator = Nominatim(user_agent="pod_lca")

                location_data = geolocator.geocode(
                    string,
                    featuretype=["settlement", "city", "town", "village", "county", "state", "country"],
                    language="en",
                    addressdetails=True,
                    extratags=True,
                )
                location.set_regionality(location_data)
                location.set_cordinates(location_data)

                location_data = geolocator.reverse(
                    location.get_cordinates(), addressdetails=True, zoom=15, language="en"
                )  # zoom level 14 = neighbourhood
                location.set_city(location_data)

            except Exception as e:
                print(f"Error retrieving location data: {e}")

        return location

    # ================================
    # Setters
    # ================================
    def set_name(self, name):
        """Set name of the location.

        Parameters
        ----------
        location_name : str
            Name of the location
        """
        self.location_name = name

        return self

    def set_regionality(self, geopy_location_nominatim):
        """Set the regionality of the location.

        Parameters
        ----------
        geopy_location_nominatim : geopy.location.Location
            Geopy location object from Nominatim
        """
        local_type = [
            "postcode",
            "county",
            "municipality",
            "city",
            "town",
            "village",
            "city_district",
            "district",
            "borough",
            "suburb",
            "subdivision",
            "hamlet",
            "croft",
            "neighbourhood",
            "allotments",
            "quarter",
        ]
        regional_type = ["region", "state", "province", "state_district"]
        national_type = ["country", "country_code"]

        if geopy_location_nominatim.raw["addresstype"] in local_type:
            self.regionality = "Local"
        elif geopy_location_nominatim.raw["addresstype"] in regional_type:
            self.regionality = "Regional"
        elif geopy_location_nominatim.raw["addresstype"] in national_type:
            self.regionality = "National"
        else:
            self.regionality = None
            log("Regionality not set", "Warn")

        return self

    def set_cordinates(self, geopy_location_nominatim=None):
        """Set the coordinates of the location.

        Parameters
        ----------
        geopy_location_nominatim : geopy.location.Location
            Geopy location object from Nominatim
        """
        if geopy_location_nominatim is None:
            for attr in ["location_name", "zipcode", "city", "state", "country"]:
                if getattr(self, attr) is None:
                    pass
                else:
                    string = getattr(self, attr)
                    break
            geolocator = Nominatim(user_agent="pod_lca", timeout=10)
            geopy_location_nominatim = geolocator.geocode(string, language="en", addressdetails=True, extratags=True)

        self.coords = geopy_location_nominatim.latitude, geopy_location_nominatim.longitude

        return self

    def set_zip(self, geopy_location, state=None):
        """Set the zipcode of the location.

        Parameters
        ----------
        geopy_location : geopy.location.Location
            Geopy location object.
        state : str
            US state name.
        """
        if geopy_location is not None:
            try:
                if "postcode" in geopy_location.raw["address"]:
                    self.zipcode = geopy_location.raw["address"]["postcode"]
                else:
                    self.zipcode = self.get_closest_zip(geopy_location)
            except:
                self.zipcode = None
        elif state is not None:
            us_state_zip = DataImporter.csv_to_pandas(config["file_paths"]["location"]["US_STATE_ZIP"])
            state_zips = us_state_zip[us_state_zip["State"] == state]["ZIP"].tolist()
            if len(state_zips) > 0:
                self.zipcode = str(state_zips[0])
            else:
                self.zipcode = None

        return self

    def set_city(self, geopy_location=None, zip_code=None):
        """Set the city of the location.

        Parameters
        ----------
        geopy_location : geopy.location.Location
            Geopy location object.
        zip_code : str
            US ZIP code of the location.
        """
        if geopy_location is not None:
            try:
                self.city = geopy_location.raw["address"]["city"]
                return self
            except:
                self.city = None

        if zip_code is not None:
            try:
                data = DataImporter.csv_to_pandas(config["file_paths"]["location"]["US_ZIP_STATE"],
                                                  dtype={"USZIP": str})
                self.city = data.loc[data["USZIP"] == zip_code, "City"].iloc[0]
            except:
                self.city = None

        return self

    def set_state(self, geopy_location=None, zip_code=None):
        """Set the state of the location.

        Parameters
        ----------
        geopy_location : geopy.location.Location
            Geopy location object.
        zip_code : str
            US ZIP code of the location.
        """
        if geopy_location is not None:
            try:
                self.state = geopy_location.raw["address"]["state"]

                us_states = DataImporter.json_to_dict(config["file_paths"]["location"]["US_STATES"])
                self.state_abbr = us_states[self.state]
            except:
                self.state = None

        if zip_code is not None:
            try:
                data = DataImporter.csv_to_pandas(config["file_paths"]["location"]["US_ZIP_STATE"],
                                                  dtype={"USZIP": str})
                self.state = data.loc[data["USZIP"] == zip_code, "State"].iloc[0]

                us_states = DataImporter.json_to_dict(config["file_paths"]["location"]["US_STATES"])
                self.state_abbr = us_states[self.state]
            except:
                self.city = None

        return self

    def set_country(self, geopy_location_photon):
        """Set the country of the location.

        Parameters
        ----------
        geopy_location_photon : geopy.location.Location
            Geopy location object from Photon
        """
        try:
            self.country = geopy_location_photon.raw["address"]["country"]
        except:
            self.country = None

        return self

    def set_country_code(self, geopy_location_photon):
        """Set the country code of the location.

        Parameters
        ----------
        geopy_location_photon : geopy.location.Location
            Geopy location object from Photon
        """
        try:
            self.country_code = geopy_location_photon.raw["address"]["country_code"].upper()
        except:
            self.country_code = None

        return self

    def set_cfs_area(self):
        """Set the state code from the Comodity Flow Survey (CFS)."""
        cfs_area = DataImporter.json_to_dict(config["file_paths"]["transportation"]["CFS_STATE_CODE"])
        state = self.get_state()

        if state:
            self.cfs_area = cfs_area[state]
        else:
            self.cfs_area = None

        return self

    def set_faf_foreign_region(self):
        """Set the FAF region (foreign) of the location."""
        country = self.get_country()
        faf_foreign_region_country = DataImporter.json_to_dict(
            config["file_paths"]["location"]["FAF_FOREIGN_REGION_COUNTRY"]
        )

        for key, value in faf_foreign_region_country.items():
            if country in value:
                self.faf_foreign_code = key
                break

        faf_region = DataImporter.json_to_dict(config["file_paths"]["location"]["FAF_FOREIGN_REGION"])
        for key, value in faf_region.items():
            if self.faf_foreign_code == value:
                self.faf_foreign_name = key
                break

        return self

    def set_faf_domestic_region(self):
        """Set the FAF region (domestic) of the location."""
        faf_domestic_region = DataImporter.json_to_dict(config["file_paths"]["location"]["FAF_DOMESTIC_REGION"])
        state = self.get_state()

        for key, value in faf_domestic_region.items():
            if state in key:
                self.faf_domestic_codes = value
                return self
        log(f"State '{state}' not found in any FAF region.", "Warn")
        self.faf_domestic_codes = None
        return self

    def set_ferc_region(self):
        """Set the Federal Energy Regulatory Commission (FERC) Region."""
        df = DataImporter.csv_to_pandas(config["file_paths"]["location"]["FERC_ZIPCODE_MAP_PATH"])
        balancing_authority = self.get_balancing_authority()
        if balancing_authority is None:
            self.set_balancing_authority()
            balancing_authority = self.get_balancing_authority()

        ferc_region = df[df["balancing_authority"].isin(balancing_authority)]["FERC_region"].unique()

        self.ferc_region = ferc_region

        return self

    def set_balancing_authority(self):
        """Set the Balancing Authority."""
        df = DataImporter.csv_to_pandas(config["file_paths"]["location"]["FERC_BA_ZIPCODE_MAP_PATH"])
        zipcode = self.get_zip()
        if df["zip_code"].dtype == "int64":
            zipcode = int(zipcode)

        balancing_authority = df[df["zip_code"] == zipcode]["balancing_authority"].unique()

        if (
            len(balancing_authority) == 0
        ):  # If no balancing authority is found, try to find it by adding leading zeros to the zipcode
            if df["zip_code"].dtype == "O":
                trail_zeros = "0" * (5 - len(zipcode))
                balancing_authority = df[df["zip_code"] == trail_zeros + zipcode]["balancing_authority"].unique()

        self.balancing_authority = balancing_authority

        return self

    def set_cambium_gea_region(self):
        """Set the Cambium Generation and Emissions Assessment (GEA) region."""
        df = DataImporter.csv_to_pandas(config["file_paths"]["location"]["GEA_ZIPCODE_MAP_PATH"])
        zipcode = self.get_zip()
        if df["zip_code"].dtype == "int64":
            zipcode = int(zipcode)

        cambium_gea_region = df[df["zip_code"] == zipcode]["cambium_gea"].unique()

        if (
            len(cambium_gea_region) == 0
        ):  # If no cambium GEA is found, try to find it by adding leading zeros to the zipcode
            if df["zip_code"].dtype == "O":
                trail_zeros = "0" * (5 - len(zipcode))
                cambium_gea_region = df[df["zip_code"] == trail_zeros + zipcode]["cambium_gea"].unique()

        self.cambium_gea_region = cambium_gea_region[0]

        return self

    def set_reeds_balancing_area(self):
        """Set the Balancing Area under the Get the Regional Energy Deployment System (ReEDS)."""
        df = DataImporter.csv_to_pandas(config["file_paths"]["location"]["REEDS_BA_ZIPCODE_MAP_PATH"])
        zipcode = self.get_zip()
        if df["zip_code"].dtype == "int64":
            zipcode = int(zipcode)

        balancing_area = df[df["zip_code"] == zipcode]["reeds_ba"].unique()

        if (
            len(balancing_area) == 0
        ):  # If no balancing area is found, try to find it by adding leading zeros to the zipcode
            if df["zip_code"].dtype == "O":
                trail_zeros = "0" * (5 - len(zipcode))
                balancing_area = df[df["zip_code"] == trail_zeros + zipcode]["reeds_ba"].unique()

        self.reeds_balancing_area = balancing_area[0]

        return self

    def set_us_coast(self):
        """Set the US coast closest to the location."""
        us_coast = DataImporter.json_to_dict(config["file_paths"]["location"]["US_COAST"])
        state = self.get_state()

        for key, value in us_coast.items():
            if state in value:
                self.us_coast = key
                return self

        log(f"State '{state}' not found in any US coast region.", "Warn")
        self.us_coast = None

        return self

    # ================================
    # Getters
    # ================================
    def get_location_name(self):
        """Retrieve the location name.

        Returns
        -------
        str
            Name of the location.
        """
        return self.location_name

    def get_regionality(self):
        """Retrieve the regionality of the location.

        Returns
        -------
        str
            Regionality of the location.
        """

        return self.regionality

    def get_cordinates(self):
        """Retrieve the coordinates of the location.

        Returns
        -------
        tuple
                (latitude, longitude).
        """
        return self.coords

    def get_zip(self):
        """Retrieve the zipcode of the location.

        Returns
        -------
        str
            Name of the ZIP code.
        """
        return self.zipcode

    def get_city(self):
        """Retrieve the city of the location.

        Returns
        -------
        str
            Name of the city.
        """
        return self.city

    def get_state(self):
        """Retrieve the state of the location.

        Returns
        -------
        str
            Name of the state.
        """
        return self.state

    def get_state_abbr(self):
        """Retrieve the state abbreviation of the location.

        Returns
        -------
        str
            Standard abbreviation of the state name.
        """
        return self.state_abbr

    def get_country(self):
        """Retrieve the country of the location.

        Returns
        -------
        str
            Name of the country.
        """
        return self.country

    def get_country_code(self):
        """Retrieve the country code of the location.

        Returns
        -------
        str
            Country code from ISO 3166-1.
        """
        return self.country_code

    def get_cfs_area(self):
        """Get the Comodity Flow Survey (CFS) area of the location.

        Returns
        -------
        int
            Code of the Comodity Flow Survey (CFS) area.
        """
        return self.cfs_area

    def get_faf_foreign_region(self, type="code"):
        """Get the Freight Analysis Framework (FAF) region (foreign) of the location.

        Parameters
        ----------
        type : {'code', 'name'}
            FAF foreign region code or name
        Returns
        -------
        :class:`str`
            Code of the Freight Analysis Framework (FAF) region (foreign).
        :class:`str`
            Name of the Freight Analysis Framework (FAF) region (foreign).

        Raises
        ------
        ValueError
            Request type not recognized.
        """
        if type == "code":
            return self.faf_foreign_code
        elif type == "name":
            return self.faf_foreign_name
        else:
            raise ValueError("Request type not recognized.")

    def get_faf_domestic_region(self):
        """Get the Freight Analysis Framework (FAF) region (domestic) of the location.

        Returns
        -------
        list of int
            Codes of the Freight Analysis Framework (FAF) region (domestic).
        """
        return self.faf_domestic_codes

    def get_us_coast(self):
        """Get the US coast closest to the location.

        Returns
        -------
        str
            US coast closest to the location.
        """
        return self.us_coast

    def get_ferc_region(self):
        """Get the Federal Energy Regulatory Commission (FERC) Region.

        Returns
        -------
        str
            Federal Energy Regulatory Commission (FERC) Region corresponding to the location.
        """
        return self.ferc_region

    def get_balancing_authority(self):
        """Get the balancing authority.

        Returns
        -------
        str
            Balancing authority corresponding to the location.
        """
        return self.balancing_authority

    def get_cambium_gea_region(self):
        """Get Cambium Generation and Emissions Assessment (GEA) region.

        Returns
        -------
        str
            Cambium Generation and Emissions Assessment (GEA) region corresponding to the location.
        """
        return self.cambium_gea_region

    def get_reeds_balancing_area(self):
        """Get the Regional Energy Deployment System (ReEDS) balancing area.

        Returns
        -------
        str
            Regional Energy Deployment System (ReEDS) balancing area corresponding to the location.
        """
        return self.reeds_balancing_area

    # ================================
    # Methods
    # ================================
    @staticmethod
    def get_closest_states(location, states_lst=None):
        """Get the closest states to the destination.

        Parameters
        ----------
        destination : ~pod_lca.location.Location
            Destination location object.
        states_lst : list of int
            List of states to find the closest ones from.

        Returns
        -------
        str
            The closest state to the destination.
        """
        state_coords = DataImporter.csv_to_pandas(config["file_paths"]["location"]["US_STATE_COORDS"])

        if states_lst is None:
            pass

        lat = state_coords[state_coords["State"].isin(states_lst)]["lat"].values
        lon = state_coords[state_coords["State"].isin(states_lst)]["lon"].values
        states = state_coords[state_coords["State"].isin(states_lst)]["State"].values

        coords = list(zip(lat, lon))
        dest_to_state = []
        for coord in coords:
            distance = geodesic(coord, location.get_cordinates()).km
            dest_to_state.append(distance)

        min_index = dest_to_state.index(min(dest_to_state))

        closest_state = states[min_index]

        return closest_state

    @staticmethod
    def get_closest_zip(geopy_location, max_attempts=10, step=1):
        """Get the closest ZIP code of the location.

        Parameters
        ----------
        geopy_location : geopy.location.Location
            Geopy location object.
        max_attempts: int
            Maximum number of attempts to find the closest zip code
        step : float
            Step size in km (approx.)
        """
        geolocator = Nominatim(user_agent="pod_lca")

        if "county" in geopy_location.raw["address"]:
            query = geopy_location.raw["address"]["county"]
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

            geopy_location = geolocator.reverse(
                (new_lat, new_lon), exactly_one=True, addressdetails=True, zoom=18, language="en"
            )

            if geopy_location and "postcode" in geopy_location.raw["address"]:
                return geopy_location.raw["address"]["postcode"]

        return "ZIP code not found within search range"

    def get_closest_state_CFS(destination, codes_lst):
        """Get the closest states to the destination, where states are given in CFS codes

        Parameters
        ----------
        destination : ~pod_lca.location.Location
            Destination location object.
        states_lst : list of int
            List of states to find the closest ones from.

        Returns
        -------
        :class:`str`
            The closest state to the destination.
        :class:`int`
            CFS code of the closest state.
        """
        codes_lst = list(set(codes_lst))

        cfs_state_code = DataImporter.json_to_dict(config["file_paths"]["transportation"]["CFS_STATE_CODE"])
        cfs_code_state = {v: k for k, v in cfs_state_code.items()}
        cfs_state_list = [cfs_code_state[v] for v in codes_lst if v in cfs_code_state]

        closest_state_name = Location.get_closest_states(destination, cfs_state_list)

        closest_state_code = cfs_state_code[closest_state_name]

        return closest_state_name, closest_state_code

    def get_closest_regions_FAF(destination, region_lst):
        """Get the closest states to the destination, where states are given in Freight Analysis Framework (FAF) domestic region codes

        Parameters
        ----------
        destination : ~pod_lca.location.Location
            Destination location object.
        states_lst : list of int
            List of states to find the closest ones from.

        Returns
        -------
        :class:`str`
            The closest state to the destination.
        :class:`int`
            FAF code of the closest state.
        """
        faf_domestic_data = DataImporter.json_to_dict(config["file_paths"]["location"]["FAF_DOMESTIC_REGION"])

        faf_code_list = [v // 10 for v in region_lst]
        closest_state_name, _ = Location.get_closest_state_CFS(destination, faf_code_list)

        closest_faf_region_codes = faf_domestic_data[closest_state_name]

        return closest_state_name, closest_faf_region_codes


if __name__ == "__main__":
    pass
