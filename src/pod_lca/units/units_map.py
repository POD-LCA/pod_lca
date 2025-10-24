
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..units import BTU
from ..units import CUBIC_FEET
from ..units import CUBIC_METER
from ..units import DAY
from ..units import FEET
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
from ..units import METER
from ..units import SQUARE_FEET
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
                    'm': METER,
                    'ft': FEET,
                    't': M_TON,
                    'metric ton': M_TON,
                    'tonne': M_TON,
                    'tkm': TON_KILOMETER,
                    't*km': TON_KILOMETER,
                    'kgkm': KILOGRAM * KILOMETER,
                    'm2': SQUARE_METER, 
                    'ft2' : SQUARE_FEET,
                    'l': LITER,
                    'm3': CUBIC_METER,
                    'ft3': CUBIC_FEET,
                    'gal': US_GALLON,
                    'J': JOULE,
                    'MJ': MEGA * JOULE, 
                    'kWh': KILO * WATT_HOUR,
                    'MWh': MEGA * WATT_HOUR,
                    'kBtu/ft2': KILO * BTU / SQUARE_FEET,
                    'kWh/ft2': KILO * WATT_HOUR / SQUARE_FEET,
                    'Item(s)': ITEM,
                    'kg C': KG_CARBON,
                    'kg CO2': KG_CARBON_DIOXIDE,
                    'kg CO2 eq': KG_CARBON_DIOXIDE,
                    'kg/m': KILOGRAM / METER,
                    'kg/m3': KILOGRAM / CUBIC_METER,
                    'kg/m2': KILOGRAM / SQUARE_METER,
                    'kg/ft2': KILOGRAM / SQUARE_FEET,
                    'kg/item': KILOGRAM / ITEM
                })
