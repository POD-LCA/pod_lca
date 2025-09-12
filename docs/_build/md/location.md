# Location

[`Location`](#pod_lca.location.Location) object maintains a record of location and is used by other classes to store and retrieve location specific data (e.g., [`get_ferc_region()`](#pod_lca.location.Location.get_ferc_region) in [`ElectricitySupply`](electricity-supply.md#pod_lca.electricity.ElectricitySupply)).

---

### *class* pod_lca.location.Location

Location object updates the location into subcategores.
: The geocoding is done using Nominatim ([https://nominatim.org/release-docs/develop/](https://nominatim.org/release-docs/develop/)) which looks up OpenStreetMap ([https://www.openstreetmap.org/](https://www.openstreetmap.org/))

#### location_name

Name of the location.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### regionality

Regionality of the location.

* **Type:**
  {'Local', 'Regional', 'National'}

#### coords

Location coordinate using WGS-84 coordinate system.

* **Type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)

#### zipcode

ZIP code of the location (in the corresponding local system).

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### city

Name of the city the location is in.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### state

Name of the state the location is in.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### state_abbr

Standard abbreviation of the state name.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### country

Name of the country the location is in.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### country_code

Country code from ISO 3166-1 Codes for the representation of names of countries and their subdivisions – Part 1: Country code

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### cfs_area

Code of the Comodity Flow Survey (CFS) area.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### faf_foreign_name

Name of the Freight Analysis Framework (FAF) region (foreign) corresponding to the location.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### faf_foreign_code

Code of the Freight Analysis Framework (FAF) region (foreign) corresponding to the location.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### faf_domestic_codes

Codes of the Freight Analysis Framework (FAF) region (domestic) corresponding to the location.

* **Type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [int](https://docs.python.org/3/library/functions.html#int)

#### us_coast

US coast closest to the location.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### ferc_region

Federal Energy Regulatory Commission (FERC) Region corresponding to the location.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### balancing_authority

Balancing authority corresponding to the location.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### cambium_gea_region

Cambium Generation and Emissions Assessment (GEA) region corresponding to the location.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### reeds_balancing_area

Regional Energy Deployment System (ReEDS) balancing area corresponding to the location.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### *classmethod* from_str(string)

Create location from name.
: The location data populated based on the centroid of the location prescribed.

* **Parameters:**
  **string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Free-form textual description or address (or part thereof) of the location.

#### *classmethod* from_US_zip(zipcode, set_all_location_data=False)

Create location from US zipcode.
: The location data populated based on the centroid of the area represented by the ZIP code.

* **Parameters:**
  * **zipcode** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- ZIP code of the location.
  * **set_all_location_data** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, set location properties other than country and ZIP code.

#### *classmethod* from_US_state(state, set_all_location_data=False)

Create location from US state.
: The location data populated based on the centroid of the area represented by the zipcode.

* **Parameters:**
  * **state** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- US state name.
  * **set_all_location_data** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, set location properties other than country, state, coast, CFS area, and FAF region.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- State name not recognized as a US state.

#### *classmethod* from_faf_regions(faf_region, set_all_location_data=False)

Create location from Freight Analysis Framework (FAF) region

* **Parameters:**
  * **faf_region** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- FAF region name.
  * **set_all_location_data** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, set location properties based on location coordinate.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- FAF region not recognized

#### set_name(name)

Set name of the location.

* **Parameters:**
  **location_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the location

#### set_regionality(geopy_location_nominatim)

Set the regionality of the location.

* **Parameters:**
  **geopy_location_nominatim** ([*geopy.location.Location*](https://geopy.readthedocs.io/en/stable/index.html#geopy.location.Location)) -- Geopy location object from Nominatim

#### set_cordinates(geopy_location_nominatim=None)

Set the coordinates of the location.

* **Parameters:**
  **geopy_location_nominatim** ([*geopy.location.Location*](https://geopy.readthedocs.io/en/stable/index.html#geopy.location.Location)) -- Geopy location object from Nominatim

#### set_zip(geopy_location)

Set the zipcode of the location.

* **Parameters:**
  **geopy_location** ([*geopy.location.Location*](https://geopy.readthedocs.io/en/stable/index.html#geopy.location.Location)) -- Geopy location object.

#### set_city(geopy_location)

Set the city of the location.

* **Parameters:**
  **geopy_location** ([*geopy.location.Location*](https://geopy.readthedocs.io/en/stable/index.html#geopy.location.Location)) -- Geopy location object.

#### set_state(geopy_location)

Set the state of the location.

* **Parameters:**
  **geopy_location** ([*geopy.location.Location*](https://geopy.readthedocs.io/en/stable/index.html#geopy.location.Location)) -- Geopy location object.

#### set_country(geopy_location_photon)

Set the country of the location.

* **Parameters:**
  **geopy_location_photon** ([*geopy.location.Location*](https://geopy.readthedocs.io/en/stable/index.html#geopy.location.Location)) -- Geopy location object from Photon

#### set_country_code(geopy_location_photon)

Set the country code of the location.

* **Parameters:**
  **geopy_location_photon** ([*geopy.location.Location*](https://geopy.readthedocs.io/en/stable/index.html#geopy.location.Location)) -- Geopy location object from Photon

#### set_cfs_area()

Set the state code from the Comodity Flow Survey (CFS).

#### set_faf_foreign_region()

Set the FAF region (foreign) of the location.

#### set_faf_domestic_region()

Set the FAF region (domestic) of the location.

#### set_ferc_region()

Set the Federal Energy Regulatory Commission (FERC) Region.

#### set_balancing_authority()

Set the Balancing Authority.

#### set_cambium_gea_region()

Set the Cambium Generation and Emissions Assessment (GEA) region.

#### set_reeds_balancing_area()

Set the Balancing Area under the Get the Regional Energy Deployment System (ReEDS).

#### set_us_coast()

Set the US coast closest to the location.

#### get_location_name()

Retrieve the location name.

* **Returns:**
  Name of the location.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_regionality()

Retrieve the regionality of the location.

* **Returns:**
  Regionality of the location.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_cordinates()

Retrieve the coordinates of the location.

* **Returns:**
  (latitude, longitude).
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)

#### get_zip()

Retrieve the zipcode of the location.

* **Returns:**
  Name of the ZIP code.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_city()

Retrieve the city of the location.

* **Returns:**
  Name of the city.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_state()

Retrieve the state of the location.

* **Returns:**
  Name of the state.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_state_abbr()

Retrieve the state abbreviation of the location.

* **Returns:**
  Standard abbreviation of the state name.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_country()

Retrieve the country of the location.

* **Returns:**
  Name of the country.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_country_code()

Retrieve the country code of the location.

* **Returns:**
  Country code from ISO 3166-1.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_cfs_area()

Get the Comodity Flow Survey (CFS) area of the location.

* **Returns:**
  Code of the Comodity Flow Survey (CFS) area.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_faf_foreign_region(type='code')

Get the Freight Analysis Framework (FAF) region (foreign) of the location.

* **Parameters:**
  **type** ( *{'code'* *,*  *'name'}*) -- FAF foreign region code or name
* **Returns:**
  * [`str`](https://docs.python.org/3/library/stdtypes.html#str) -- Code of the Freight Analysis Framework (FAF) region (foreign).
  * [`str`](https://docs.python.org/3/library/stdtypes.html#str) -- Name of the Freight Analysis Framework (FAF) region (foreign).
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Request type not recognized.

#### get_faf_domestic_region()

Get the Freight Analysis Framework (FAF) region (domestic) of the location.

* **Returns:**
  Codes of the Freight Analysis Framework (FAF) region (domestic).
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [int](https://docs.python.org/3/library/functions.html#int)

#### get_us_coast()

Get the US coast closest to the location.

* **Returns:**
  US coast closest to the location.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_ferc_region()

Get the Federal Energy Regulatory Commission (FERC) Region.

* **Returns:**
  Federal Energy Regulatory Commission (FERC) Region corresponding to the location.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_balancing_authority()

Get the balancing authority.

* **Returns:**
  Balancing authority corresponding to the location.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_cambium_gea_region()

Get Cambium Generation and Emissions Assessment (GEA) region.

* **Returns:**
  Cambium Generation and Emissions Assessment (GEA) region corresponding to the location.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_reeds_balancing_area()

Get the Regional Energy Deployment System (ReEDS) balancing area.

* **Returns:**
  Regional Energy Deployment System (ReEDS) balancing area corresponding to the location.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### *static* get_closest_states(location, states_lst=None)

Get the closest states to the destination.

* **Parameters:**
  * **destination** ([*Location*](#pod_lca.location.Location)) -- Destination location object.
  * **states_lst** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*int*](https://docs.python.org/3/library/functions.html#int)) -- List of states to find the closest ones from.
* **Returns:**
  The closest state to the destination.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### *static* get_closest_zip(geopy_location, max_attempts=10, step=1)

Get the closest ZIP code of the location.

* **Parameters:**
  * **geopy_location** ([*geopy.location.Location*](https://geopy.readthedocs.io/en/stable/index.html#geopy.location.Location)) -- Geopy location object.
  * **max_attempts** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Maximum number of attempts to find the closest zip code
  * **step** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Step size in km (approx.)

#### get_closest_state_CFS(codes_lst)

Get the closest states to the destination, where states are given in CFS codes

* **Parameters:**
  * **destination** ([*Location*](#pod_lca.location.Location)) -- Destination location object.
  * **states_lst** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*int*](https://docs.python.org/3/library/functions.html#int)) -- List of states to find the closest ones from.
* **Returns:**
  * [`str`](https://docs.python.org/3/library/stdtypes.html#str) -- The closest state to the destination.
  * [`int`](https://docs.python.org/3/library/functions.html#int) -- CFS code of the closest state.

#### get_closest_regions_FAF(region_lst)

Get the closest states to the destination, where states are given in Freight Analysis Framework (FAF) domestic region codes

* **Parameters:**
  * **destination** ([*Location*](#pod_lca.location.Location)) -- Destination location object.
  * **states_lst** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*int*](https://docs.python.org/3/library/functions.html#int)) -- List of states to find the closest ones from.
* **Returns:**
  * [`str`](https://docs.python.org/3/library/stdtypes.html#str) -- The closest state to the destination.
  * [`int`](https://docs.python.org/3/library/functions.html#int) -- FAF code of the closest state.
