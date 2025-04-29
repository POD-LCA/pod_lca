__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# =========================
# ELECTRICITY SOURCE DATA
# =========================
# The following source data set is used to determine the electricity consumption mix and the impacts. 

# =========================
# 1. Cambium data
# =========================
# These are all source data downloaded from the Cambium database. Currently, the Cambium 2024 data set is used.

# 1.1 data/electricity_cambium_consumption-national.csv 
# 1.2 data/electricity_cambium_consumption-regional.csv 
# 1.3 data/electricity_cambium_consumption-local.csv

# The dataset needs some editorial changes in the headers to be used by the Python framework. There should be only one header row, and there should be headers  ‘scenario’ and  ‘t’ corresponding to the cambium scenario and the year. 
# The national data set should have a header  ‘country_code’  code, in this instance, the entry should be ‘US’. 
# Similarly, the regional dataset should have a header  ‘gea’, and the local data a header  ‘r’.

# The electricity generation technologies need to be mapped from the Cambium data to the impact data.

# 1.4 data/electricity_cambium_technology-headers.json
#           maps the Cambium technology type (key of the dictionary) to the corresponding header names (value in the dictionary) in the Cambium data files. 
# 1.5 data/electricity_cambium_technology-map.json 
#           maps the Cambium technology (key of the dictionary) to the corresponding technology type in the impact data (value in the dictionary).


# =========================
# 2. Impact data
# =========================
# National Energy Technology Laboratory (NETL) data are manually pre-processed and provided as static input tables. 

# 2.1 data/electricity_netl_national-consumption-impacts-by-technology.csv
# 2.2 data/electricity_netl_regional-consumption-impacts-by-technology.csv
# TODO: Update description from  https://docs.google.com/document/d/1bULE-q0xY9u9l8cELIm-NK8HQG9KOhreWHsDgJToatI/edit?usp=sharing

# =========================
# 3. Regional mapping data
# =========================
# The following mappings are also used. These data files are saved in the data folder as CSV files. The files should have one row of headers at the top.

# 3.1 data/location_doe_ba-zip-mapping.csv [BA_zip_mapping]
# 3.2 data/location_netl_ferc-ba-mapping.csv [FERC_BA_mapping]
# 3.3 data/location_cambium_gea-reeds-zip-mapping.csv []

# Balancing authorities are mapped to zip codes using the balancing authority look-up table.
# The data are available for 40326 zip codes (excluding the zip codes marked as ‘NA’ or ‘Balancing authority not available’, and those from Alaska and Hawaii). 
# Balancing areas are then mapped to FERC regions using the FERC_BA mapping, which is extracted from the ‘ba_ferc_mapping’ tab in the NETL Grid Mix explorer. 
# BA_zip_mapping must include headers  ‘zip_code’ and  ‘balancing_authority’, while FERC_BA_mapping must have ‘balancing_authority’ and ‘ferc_region’ as headers.
# Balancing authority names in FERC_BA_mapping needed to be updated to match the spellings used in BA_zip_mapping. 
# Similarly, the FERC region names used in the FERC_BA_mapping should match the spelling used in Regional_consumption_impacts_by_technology.
# The GEA and ReEDS balancing area mappings to zip codes are from data.gov. 
# This data set has mapping for 40462 zip codes, each uniquely mapped to a GEA and ReEDS balancing area. 
# The data headers must include ‘zip_code’, ‘reeds_ba’, and ‘cambium_ga’.

# Note that when saving data from MS Excel worksheets as a CSV file, the number displayed is what is saved, regardless of what is being displayed in the formula bar (e.g., a cell displaying 3.2 and the formula bar displaying 3.25485). 
# This can end up with the significance of the values being lost. 
# The Cambium data are saved in the CSV files with 15 significant digits.
