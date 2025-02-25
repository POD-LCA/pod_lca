from utilities.units.common_units import KILOGRAM, JOULE, KILOMETER, WATT_HOUR, TON_KILOMETER, CUBIC_METER, CUBIC_FEET, US_GALLON
from utilities.units.metric_prefixes import KILO, MEGA

UNITS_MAP = {'kg': KILOGRAM, 
             'km': KILOMETER, 
             'tkm': TON_KILOMETER,
             'kgkm': KILOGRAM * KILOMETER, 
             'MJ': MEGA * JOULE, 
             'kWh': KILO * WATT_HOUR,
             'm3': CUBIC_METER,
             'ft3': CUBIC_FEET,
             'gal': US_GALLON
             }
