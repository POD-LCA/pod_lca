from utilities.units import UNIT_CONVERSIONS
from utilities.units.units import Unit
from utilities.units.metric_prefixes import KILO

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# REF: [1]  National Institute of Standards and Technology (NIST) Handbook 44 (2024). Specifications, Tolerances, and 
#           Other Technical Requirements for Weighing and Measuring Devices.

# TODO add unit conversions (mass/volume/energy)
# TODO add instructions on adding new base units

# ==================================
# TIME UNITS
# ==================================

SECOND = Unit('second', 'sec', 'time', True)
MINUTE = Unit('minute', 'min', 'time', False)
HOUR = Unit('hour', 'hr', 'time', False)

UNIT_CONVERSIONS['time'] = {'second': 3600, 'minute': 60, 'hour': 1}

# ==================================
# MASS UNITS
# ==================================

GRAM = Unit('gram', 'g', 'mass', True)
M_TON = Unit('metric Ton', 't', 'mass', False)
S_TON = Unit('short Ton', 'tn', 'mass', False)
POUND = Unit('pound', 'lb', 'mass', True)
OUNCE = Unit('ounce', 'oz', 'mass', True)

KILOGRAM = Unit('kilogram', 'kg', 'mass', True)
KILOGRAM.base_unit = GRAM
KILOGRAM.prefix = KILO

UNIT_CONVERSIONS['mass'] = {}
# REF [1] pp. C-10

# ==================================
# LENGTH UNITS
# ==================================

METER = Unit('meter', 'm', 'length', True)
FEET = Unit('feet', 'ft', 'length', False)
INCH = Unit('inch', 'in', 'length', False)
YARD = Unit('yard', 'yd', 'length', False)
MILE = Unit('mile', 'mi', 'length', False)
NAUTICAL_MILE = Unit('nautical mile', 'nmi', 'length', False)

KILOMETER = Unit('kilogram', 'kg', 'length', True)
KILOMETER.base_unit = METER
KILOMETER.prefix = KILO

UNIT_CONVERSIONS['length'] = {'inch': 63360, 'feet': 5280, 'yard': 1760, 'mile': 1, 'meter': 1609.344} 
# REF [1] pp. C-10

# ==================================
# AREA UNITS
# ==================================

SQUARE_METER = Unit('square meter', 'm^2', 'area', True)
SQUARE_METER.is_compound_unit = True
SQUARE_METER.components = [METER, METER]

SQUARE_FEET = Unit('square feet', 'ft^2', 'area', False)
SQUARE_FEET.is_compound_unit = True
SQUARE_FEET.components = [FEET, FEET]

ACRE = Unit('acre', 'acre', 'area', False)
HECTARE = Unit('hectare', 'ha', 'area', False)

UNIT_CONVERSIONS['area'] = {'square feet': 43560, 'acre': 1.0, 'square meter': 4046.8564224,  'hectare': 0.40468564224} 
# REF [1] pp. C-14/15

# ==================================
# VOLUME UNITS
# ==================================

LITER = Unit('liter', 'l', 'volume', True)
US_GALLON = Unit('US gallon', 'US gal', 'volume', False)

CUBIC_METER = Unit('cubic meter', 'm^3', 'volume', True)
CUBIC_METER.is_compound_unit = True
CUBIC_METER.components = [METER, METER, METER]

CUBIC_FEET = Unit('cubic feet', 'ft^3', 'volume', False)
CUBIC_FEET.is_compound_unit = True
CUBIC_FEET.components = [FEET, FEET, FEET]

UNIT_CONVERSIONS['volume'] = {} 
# REF [1] pp. C-14/15

# ==================================
# POWER UNITS
# ==================================

WATT = Unit('watt', 'W', 'power', True)

UNIT_CONVERSIONS['power'] = {'watt': 1.0}

# ==================================
# ENERGY UNITS
# ==================================

WATT_HOUR = Unit('watt-hour', 'Whr', 'energy', True)
WATT_HOUR.is_compound_unit = True
WATT_HOUR.components = [WATT, HOUR]

JOULE = Unit('joule', 'J', 'energy', True)
JOULE.is_compound_unit = True
JOULE.components = [WATT, SECOND]

THERM = Unit('therm', 'thm', 'energy', False)

UNIT_CONVERSIONS['energy'] = {} 
# REF [1] pp. 

# ==================================
# INSULATION UNITS
# ==================================

BTU = Unit('British Thermal Units', 'BTU', 'heat content', False)

UNIT_CONVERSIONS['heat content'] = {'British Thermal Units': 1.0}
