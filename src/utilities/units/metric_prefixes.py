from utilities.units.units import MetricPrefix
from utilities.units import ALL_PREFIXES

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# ALL_PREFIXES is a definitve list of metric prefixes, with reference to [1].

# REF: [1]  National Institute of Standards and Technology (NIST) Handbook 44 (2024). Specifications, Tolerances, and 
#           Other Technical Requirements for Weighing and Measuring Devices.

YOTTA = MetricPrefix('yotta', 'Y', 24)
ZETTA = MetricPrefix('zetta', 'Z', 21)
EXA = MetricPrefix('exa', 'E', 18)
PETA = MetricPrefix('peta', 'P', 15)
TERA = MetricPrefix('tera', 'T', 12)
GIGA = MetricPrefix('giga', 'G', 9)
MEGA = MetricPrefix('mega', 'M', 6)
KILO = MetricPrefix('kilo', 'k', 3)
HECTO = MetricPrefix('hecto', 'h', 2)
DEKA= MetricPrefix('deka', 'da', 1)
DECI = MetricPrefix('deci', 'd', -1)
CENTI = MetricPrefix('centi', 'c', -2)
MILI = MetricPrefix('mili', 'm', -3)
MICRO = MetricPrefix('micro', 'mu', -6)
NANO = MetricPrefix('nano', 'n', -9)
PICO = MetricPrefix('pico', 'p', -12)
FEMTO = MetricPrefix('femto', 'f', -15)
ATTO = MetricPrefix('atto', 'a', -18)
ZEPTO = MetricPrefix('zepto', 'z', -21)
YOCTO = MetricPrefix('yocto', 'y', -24)

ALL_PREFIXES.extend([YOTTA, ZETTA, EXA, PETA, TERA, GIGA, MEGA, KILO, HECTO, DEKA, DECI, CENTI, MILI, MICRO, NANO, PICO, FEMTO, ATTO, ZEPTO, YOCTO])
