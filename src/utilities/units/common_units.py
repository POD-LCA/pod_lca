
from utilities.units import UNIT_CONVERSIONS
from utilities.units.metric_prefixes import KILO
from utilities.units.units import Unit


__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


# ==================================
# INTRODUCTION
# ==================================

# The basics units are defined for this package, based on common units of measurements used in life cycle assessments.
# The units include both metric and imperial units of measurements.
# The units of measurements defined are categoriesed based on the quantity measured (e.g., 'time', 'length').

# If a user want to create a new basic unit, they are encouraged to use the Unit.from_basics(name, standard_notation, qty_measured) 
# method. For conversions to work as expected, they need to add the corresponding conversion factor to UNIT_CONVERSIONS, keyed 
# by the measurement category and the standard_notation. The values in UNIT_CONVERSIONS[category] are equivalent. The conversion
# factors defined are based on references [1] and [2] below.

# The units presented here can be used to create new units of measurements. These can be derived by multiplication and/or 
# division of units by other units or metric prefixes, where applicable. 
# e.g., KILOMETER = KILO * METER, UNIT_WEIGHT = KILOGRAM / CUBIC_METER
# The list below defines the derived units of KILOMETER and KILOGRAM as these are common units. The users are encouraged 
# to add their commonly used units here and import from this central source.

# A method is defined for obtaining the conversion factor for converting a unit to another within the same category.
# In this note the special case of 'area' and 'volume', when conversion across metric and imperial units are envisaged.
# Although you can define a new unit of measurement (say) METER * METER this would be categorized as 'length-length' 
# and thus cannot be converted to ACRE, which is categorized as 'area'. Thus, the users are encouraged to use the 
# predeefined unit of SQUARE_METER instead. The similar is applied to 'volume' calculations

# REF: [1]  National Institute of Standards and Technology (NIST) Handbook 44 (2024). Specifications, Tolerances, and 
#           Other Technical Requirements for Weighing and Measuring Devices.
#      [2]  National Institute of Standards and Technology (NIST) Special Publication 811 (2008). Guide for the Use of the International 
#           System of Units (SI)

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

SQUARE_METER = Unit.from_basics('square meter', 'm2', 'area')
SQUARE_FEET = Unit.from_basics('square feet', 'ft2', 'area')
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
CUBIC_METER = Unit.from_basics('cubic meter', 'm3', 'volume')
CUBIC_FEET = Unit.from_basics('cubic feet', 'ft3', 'volume')

UNIT_CONVERSIONS['volume'] = {'cubic feet': 1.0,
                              'cubic meter': 0.028316846592,
                              'liter': 28.316846592,
                              'US gallon': 28.316846592 / 3.785411784}
# REF [1] pp. C-17/18

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

UNIT_CONVERSIONS['energy'] = {'watt-hour': 1.0,
                              'joule': 3600,
                              'therm': 3600 / 1.054804e+08} 
# REF [2] pp.55 
