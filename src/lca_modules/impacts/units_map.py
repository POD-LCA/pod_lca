from utilities.units.common_units import KILOGRAM, JOULE, KILOMETER, WATT_HOUR, TON_KILOMETER
from utilities.units.metric_prefixes import KILO, MEGA

UNITS_MAP = {'kg': KILOGRAM, 
             'km': KILOMETER, 
             'tkm': TON_KILOMETER, 
             'MJ': MEGA * JOULE, 
             'kWh': KILO * WATT_HOUR}
