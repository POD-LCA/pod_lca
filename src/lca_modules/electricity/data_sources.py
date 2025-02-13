
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# ==================================
# INSTRUCTIONS
# ==================================

# File path to the National level electricity data to be provided here
# The data file should have the following columns
#   Country : the common name of the country
#   Country code : country code following ISO 3166-1 Codes for the representation of names of countries and their subdivisions – Part 1: Country code.
#                   country code is in upper case
#   <impact categories> : Impact category names should match the impact categories used across the project (default path: data/impact_categories.json.
#                           Impact category names are case sensitive.

NATIONAL_DATA = "data\\National_consumption_impacts_by_technology.csv"

# File path to the Regional level electricity data to be provided here
# The data file should have the following columns
#   Region : the common name of the region.
#            Corresponding methods should be implemented in the location module to set and get the region name.
#   <impact categories> : Impact category names should match the impact categories used across the project (default path: data/impact_categories.json.
#                           Impact category names are case sensitive.

REGIONAL_DATA = "data\\FERC_consumption_impacts.csv"

# File path to the Local level electricity data to be provided here
# The data file should have the following columns
#   Area : the common name of the local area.
#            Corresponding methods should be implemented in the location module to set and get the local area name.
#   <impact categories> : Impact category names should match the impact categories used across the project (default path: data/impact_categories.json.
#                           Impact category names are case sensitive.

LOCAL_DATA = "data\\BA_consumption_impacts.csv"
