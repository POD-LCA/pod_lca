from utilities.units.common_units import WATT_HOUR   
from utilities.units.metric_prefixes import MEGA

DEFAULT_REIGIONAL_RESOLUTION = 'National'
DEFAULT_COUNTRY = 'USA'
DEFAULT_COUNTRY_CODE = 'US'
DEFAULT_YEAR = 2025
DEFAULT_SCENARIO = 'MidCase'
DEFAULT_DECLARED_UNIT = MEGA * WATT_HOUR

CAMBIUM_NATIONAL_DATA = "data\\electricity_cambium_consumption-national.csv"
CAMBIUM_REGIONAL_DATA = "data\\electricity_cambium_consumption-regional.csv"
CAMBIUM_LOCAL_DATA = "data\\electricity_cambium_consumption-local.csv"
CAMBIUM_DATA_YEARS = [2025, 2030, 2035, 2040, 2045, 2050]
CAMBIUM_HEADER_MAP = "data\\electricity_cambium_technology-headers.json"
CAMBIUM_TECHNOLOGY_MAP = "data\\electricity_cambium_technology-map.json"
CAMBIUM_REGIONS_MAP = "data\\electricity_cambium_regions-map.json"

# File path to the National level electricity data to be provided here
# The data file should have the following columns
#   Country : the common name of the country
#   Country code : country code following ISO 3166-1 Codes for the representation of names of countries and their subdivisions – Part 1: Country code.
#                   country code is in upper case
#   <impact categories> : Impact category names should match the impact categories used across the project (default path: data/impact_categories.json.
#                           Impact category names are case sensitive.

ELECTRICITY_IMPACT_NATIONAL_DATA = "data\\electricity_netl_national-consumption-impacts-by-technology.csv"

# File path to the Regional level electricity data to be provided here
# The data file should have the following columns
#   Region : the common name of the region.
#            Corresponding methods should be implemented in the location module to set and get the region name.
#   <impact categories> : Impact category names should match the impact categories used across the project (default path: data/impact_categories.json.
#                           Impact category names are case sensitive.

ELECTRICITY_IMPACT_REGIONAL_DATA = "data\\electricity_netl_regional-consumption-impacts-by-technology.csv"

ELECTRICITY_TECHNOLOGIES = "data\\electricity_netl_electricity-technologies.csv"
