from utilities.units.units import Unit
from utilities.units.metric_prefixes import KILO

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


# ==================================
# TIME UNITS
# ==================================

SECOND = Unit('second', 'sec', 'time', True)
MINUTE = Unit('minute', 'min', 'time', False)
HOUR = Unit('hour', 'hr', 'time', False)

# ==================================
# MASS UNITS
# ==================================

GRAM = Unit('gram', 'g', 'weight', True)
M_TON = Unit('metric Ton', 't', 'weight', False)
S_TON = Unit('short Ton', 'tn', 'weight', False)
POUND = Unit('pound', 'lb', 'weight', True)
OUNCE = Unit('ounce', 'oz', 'weight', True)

KILOGRAM = Unit('kilogram', 'kg', 'weight', True)
KILOGRAM.base_unit = GRAM
KILOGRAM.prefix = KILO

# ==================================
# LENGTH UNITS
# ==================================

METER = Unit('meter', 'm', 'length', True)
FEET = Unit('feet', 'ft', 'length', False)
INCH = Unit('inch', 'in', 'length', False)
YARD = Unit('yard', 'yd', 'length', False)
MILE = Unit('mile', 'mi', 'length', False)
NAUTICAL_MILE = Unit('nautical mile', 'nmi', 'length', False)

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

# ==================================
# POWER UNITS
# ==================================

WATT = Unit('watt', 'W', 'power', True)

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

# ==================================
# INSULATION UNITS
# ==================================

BTU = Unit('British Thermal Units', 'BTU', 'insulation', False)


# TODO add unit conversions 
# TODO add instructions on adding new base units