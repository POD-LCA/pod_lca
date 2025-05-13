
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# =========================
# END-OF-LIFE SOURCE DATA
# =========================
# The following source data set is used to determine the default EOL mix and the impacts. 

# =========================
# 1. Default mixes
# =========================
# These are source data provided by the POD|LCA EOL Team [bjarvin@uw.edu;pierobon@uw.edu].

# 1.1 data/eol_podlca_default-mixes.csv

# The default mixes of the end-of-life processes are given for a list of materials.
# This includes an item named 'DEFAULT' corresponding to the default mix to be used when a corresponding material is not found in the list. 
# The percentages can be given either as a percentage (i.e., with a % mark) where the sum adds up to hundred or as a number where the sum adds up to 1.
# An entry marked 'NA' (or 'N/A') indicates that the corresponding EOL process is not available for the material. 
# This means that the users are not allowed to set a value for these processes when they try out different mix proportions. 
# If the technology exists for the process (and therefore the impact data is available) but is rarely used, it is suggested to set a value of 0% (or 0.0) in the default mix table.

# =========================
# 2. Impact data
# =========================
# These are source data provided by the POD|LCA EOL Team [bjarvin@uw.edu;pierobon@uw.edu].

# 2.1 data/impacts_podlca_eol-impacts.csv

# EOL Impact data set requires 'Process' and 'LCA Stage' to be included in addition to the 'Material' name to uniquely identify an impact data entry. 
# Two default impact data entries are set for unrecognized materials: ‘C4, Landfill, DEFAULT_BIOBASED’ and ‘C4, Landfill, DEFAULT_OTHER’. 
# By default, the unrecognized material is assumed to be bio-based, the more conservative assumption.
