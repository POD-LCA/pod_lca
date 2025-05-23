
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..units import CUBIC_FEET
from ..units import CUBIC_METER
from ..units import DAY
from ..units import HOUR
from ..units import ITEM
from ..units import JOULE
from ..units import KG_CARBON
from ..units import KG_CARBON_DIOXIDE
from ..units import KILO
from ..units import KILOGRAM
from ..units import KILOMETER
from ..units import LITER
from ..units import MEGA
from ..units import SQUARE_METER
from ..units import M_TON
from ..units import TON_KILOMETER
from ..units import UNITS_MAP
from ..units import US_GALLON
from ..units import WATT_HOUR

# This file contains a mapping of strings to their corresponding unit objects.
# This is to be used for conversions strings in import files (CSV, JSON, etc.) to their corresponding unit objects in the code.
# The mapping is not exhaustive and can be extended as needed.

UNITS_MAP.update({
                    'd': DAY,
                    'h': HOUR,
                    'kg': KILOGRAM,
                    't': M_TON,
                    'km': KILOMETER,
                    't': M_TON,
                    'tkm': TON_KILOMETER,
                    't*km': TON_KILOMETER,
                    'kgkm': KILOGRAM * KILOMETER,
                    'm2': SQUARE_METER, 
                    'l': LITER,
                    'm3': CUBIC_METER,
                    'ft3': CUBIC_FEET,
                    'gal': US_GALLON,
                    'MJ': MEGA * JOULE, 
                    'kWh': KILO * WATT_HOUR,
                    'MWh': MEGA * WATT_HOUR,
                    'Item(s)': ITEM,
                    'kg C': KG_CARBON,
                    'kg CO2': KG_CARBON_DIOXIDE,
                    'kg CO2 eq': KG_CARBON_DIOXIDE
                })
