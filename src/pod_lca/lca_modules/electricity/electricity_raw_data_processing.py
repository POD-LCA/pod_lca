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
# National Energy Technology Laboratory (NETL) data are pre-processed and provided as static input tables.

# 2.1 data/electricity_netl_national-consumption-impacts-by-technology.csv
# 2.2 data/electricity_netl_regional-consumption-impacts-by-technology.csv

# The NETL Grid Mix Explorer is used to generate impact and emission data for electricity generation per 23 powerplant technology types and 11 geographical regions.
# The 23 powerplant technology types include the following (with at least 90% of electricity generation from specified technology):

# A custom excel macro (macro name: “generate_production_LCI_per_FERC” in the edited Grid Mix Explorer in https://drive.google.com/file/d/1sazCmBN6gCqvZ8xPloszxJ1p_bBf2Swg/view?usp=sharing) is used to generate the impact and emission data.
# The macro parametrically changes the custom mix entries in the “generation_mix” excel tab of the Grid Mix Explorer to 100% for the corresponding technology it is calculating (cells D16 through D38). It also changes the FERC region in cell B7 to the corresponding region it is calculating.
# Prior to running the macro, IPCC AR-5, 100-year time horizon w/out climate carbon feedback was chosen as the GWP characterization factor method.
# The tool includes a “1 and 2 kg CO2e adder” in the characterization factor for methane. To stay consistent with the rest of the POD|LCA methods, the user needs to manually enter the IPCC AR-5 100-year characterization factor without the adder (28 kgCO2e/kg methane) in cell AF30 in the “traci_factor” tab.

# =========================
# 3. Regional mapping data
# =========================
# The following mappings are also used. These data files are saved in the data folder as CSV files. The files should have one row of headers at the top.

# 3.1 data/location_doe_ba-zip-mapping.csv [BA_zip_mapping]
# 3.2 data/location_netl_ferc-ba-mapping.csv [FERC_BA_mapping]
# 3.3 data/location_cambium_gea-reeds-zip-mapping.csv
# 3.4 data/electricity_cambium_technology-headers.json [cambium_headers]
# 3.5 data/electricity_cambium_technology-map.json [cambium_technology_map]

# Balancing authorities are mapped to zip codes using the balancing authority look-up table.
# The data are available for 40326 zip codes (excluding the zip codes marked as ‘NA’ or ‘Balancing authority not available’, and those from Alaska and Hawaii).
# Balancing areas are then mapped to FERC regions using the FERC_BA mapping, which is extracted from the ‘ba_ferc_mapping’ tab in the NETL Grid Mix explorer.
# BA_zip_mapping must include headers  ‘zip_code’ and  ‘balancing_authority’, while FERC_BA_mapping must have ‘balancing_authority’ and ‘ferc_region’ as headers.
# Balancing authority names in FERC_BA_mapping needed to be updated to match the spellings used in BA_zip_mapping.
# Similarly, the FERC region names used in the FERC_BA_mapping should match the spelling used in Regional_consumption_impacts_by_technology.
# The GEA and ReEDS balancing area mappings to zip codes are from data.gov.
# This data set has mapping for 40462 zip codes, each uniquely mapped to a GEA and ReEDS balancing area.
# The data headers must include ‘zip_code’, ‘reeds_ba’, and ‘cambium_ga’.

# The electricity generation technologies need to be mapped from the Cambium data to the impact data.
# ‘Cambium_headers’ JSON files map the Cambium technology type (key of the dictionary) to the corresponding header names (value in the dictionary) in the Cambium data files.
# ‘Cambium_technology_map’ JSON file maps the Cambium technology (key of the dictionary) to the corresponding technology type in the impact data (value in the dictionary).

# Note that when saving data from MS Excel worksheets as a CSV file, the number displayed is what is saved, regardless of what is being displayed in the formula bar (e.g., a cell displaying 3.2 and the formula bar displaying 3.25485).
# This can end up with the significance of the values being lost.
# The Cambium data are saved in the CSV files with 15 significant digits.
