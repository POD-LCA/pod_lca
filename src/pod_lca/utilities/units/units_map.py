from utilities.units.common_units import KILOGRAM, JOULE, KILOMETER, WATT_HOUR, TON_KILOMETER, CUBIC_METER, LITER, HOUR, SQUARE_METER, ITEM, CUBIC_FEET, US_GALLON
from utilities.units.metric_prefixes import KILO, MEGA

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


# This file contains a mapping of strings to their corresponding unit objects.
# This is to be used for conversions strings in import files (CSV, JSON, etc.) to their corresponding unit objects in the code.
# The mapping is not exhaustive and can be extended as needed.

UNITS_MAP = {
                'h': HOUR,
                'kg': KILOGRAM,
                'km': KILOMETER,
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
                'Item(s)': ITEM
            }
