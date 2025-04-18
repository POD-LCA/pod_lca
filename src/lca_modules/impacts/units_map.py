from utilities.units.common_units import KILOGRAM, JOULE, KILOMETER, WATT_HOUR, TON_KILOMETER, CUBIC_METER, LITER, HOUR, SQUARE_METER, ITEMS
from utilities.units.metric_prefixes import KILO, MEGA

UNITS_MAP = {'kg': KILOGRAM, 
             'km': KILOMETER, 
             'tkm': TON_KILOMETER, 
             'MJ': MEGA * JOULE, 
             'kWh': KILO * WATT_HOUR,
             'm3': CUBIC_METER,
             't*km': TON_KILOMETER,
             'l': LITER,
             'h': HOUR,
             'm2': SQUARE_METER,
             'Item(s)': ITEMS}
