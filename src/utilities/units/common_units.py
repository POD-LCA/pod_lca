from utilities.units import UNIT_CONVERSIONS
from utilities.units.units import Unit
from utilities.units.metric_prefixes import KILO

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# ==================================
# INTRODUCTION
# ==================================

# REF: [1]  National Institute of Standards and Technology (NIST) Handbook 44 (2024). Specifications, Tolerances, and 
#           Other Technical Requirements for Weighing and Measuring Devices.

# TODO add unit conversions (volume/energy)
# TODO add instructions on adding new base units

# ==================================
# TIME UNITS
# ==================================

SECOND = Unit.from_basics('second', 'sec', 'time')
MINUTE = Unit.from_basics('minute', 'min', 'time')
HOUR = Unit.from_basics('hour', 'hr', 'time')

UNIT_CONVERSIONS['time'] = {'second': 3600, 
                            'minute': 60, 
                            'hour': 1}

# ==================================
# MASS UNITS
# ==================================

GRAM = Unit.from_basics('gram', 'g', 'mass')
M_TON = Unit.from_basics('metric Ton', 't', 'mass')
S_TON = Unit.from_basics('short Ton', 'tn', 'mass')
POUND = Unit.from_basics('pound', 'lb', 'mass')
OUNCE = Unit.from_basics('ounce', 'oz', 'mass')

UNIT_CONVERSIONS['mass'] = {'short Ton': 1.0, 
                            'gram': 907184.74, 
                            'metric Ton': 0.90718474, 
                            'pound': 2000, 
                            'ounce':32000}
# REF [1] pp. C-19/20

KILOGRAM = KILO * GRAM

# ==================================
# LENGTH UNITS
# ==================================

METER = Unit.from_basics('meter', 'm', 'length')
FEET = Unit.from_basics('feet', 'ft', 'length')
INCH = Unit.from_basics('inch', 'in', 'length')
YARD = Unit.from_basics('yard', 'yd', 'length')
MILE = Unit.from_basics('mile', 'mi', 'length')
NAUTICAL_MILE = Unit.from_basics('nautical mile', 'nmi', 'length')

UNIT_CONVERSIONS['length'] = {'inch': 63360, 
                              'feet': 5280, 
                              'yard': 1760, 
                              'mile': 1, 
                              'meter': 1609.344, 
                              'nautical mile': 1.151} 
# REF [1] pp. C-10

KILOMETER = KILO * METER

# ==================================
# TRANSPORTATION UNITS
# ==================================

TON_KILOMETER = M_TON * KILOMETER
TON_MILE = M_TON * MILE

# ==================================
# AREA UNITS
# ==================================

SQUARE_METER = Unit.from_basics('square meter', 'm^2', 'area')
SQUARE_FEET = Unit.from_basics('square feet', 'ft^2', 'area')
ACRE = Unit.from_basics('acre', 'acre', 'area')
HECTARE = Unit.from_basics('hectare', 'ha', 'area')

UNIT_CONVERSIONS['area'] = {'square feet': 43560, 
                            'acre': 1.0, 
                            'square meter': 4046.8564224,  
                            'hectare': 0.40468564224} 
# REF [1] pp. C-14/15

# ==================================
# VOLUME UNITS
# ==================================

LITER = Unit.from_basics('liter', 'l', 'volume')
US_GALLON = Unit.from_basics('US gallon', 'US gal', 'volume')
CUBIC_METER = Unit.from_basics('cubic meter', 'm^3', 'volume')
CUBIC_FEET = Unit.from_basics('cubic feet', 'ft^3', 'volume')

UNIT_CONVERSIONS['volume'] = {}
# REF [1] pp. C-14/15

# ==================================
# POWER UNITS
# ==================================

WATT = Unit.from_basics('watt', 'W', 'power')

UNIT_CONVERSIONS['power'] = {'watt': 1.0}

# ==================================
# ENERGY UNITS
# ==================================

WATT_HOUR = Unit.from_basics('watt-hour', 'Wh', 'energy')
JOULE = Unit.from_basics('joule', 'J', 'energy')
THERM = Unit.from_basics('therm', 'thm', 'energy')

UNIT_CONVERSIONS['energy'] = {} 
# REF [1] pp. 

# ==================================
# INSULATION UNITS
# ==================================

BTU = Unit.from_basics('British Thermal Units', 'BTU', 'heat content')

UNIT_CONVERSIONS['heat content'] = {'British Thermal Units': 1.0}
