# Units Map

`pod_lca.units.UNITS_MAP` maps name strings (used in imported data sets) to [`Unit`](units.md#pod_lca.units.Unit) objects.

This dictionary is not exhaustive and useres can extend it as desired.

```python
from pod_lca.units import CUBIC_FEET
from pod_lca.units import CUBIC_METER
from pod_lca.units import DAY
from pod_lca.units import HOUR
from pod_lca.units import ITEM
from pod_lca.units import JOULE
from pod_lca.units import KG_CARBON
from pod_lca.units import KG_CARBON_DIOXIDE
from pod_lca.units import KILO
from pod_lca.units import KILOGRAM
from pod_lca.units import KILOMETER
from pod_lca.units import LITER
from pod_lca.units import MEGA
from pod_lca.units import SQUARE_METER
from pod_lca.units import M_TON
from pod_lca.units import TON_KILOMETER
from pod_lca.units import UNITS_MAP
from pod_lca.units import US_GALLON
from pod_lca.units import WATT_HOUR

UNITS_MAP.update({
                 'd': DAY,
                 'h': HOUR,
                 'kg': KILOGRAM,
                 't': M_TON,
                 'km': KILOMETER,
                 't': M_TON,
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
                 'Item(s)': ITEM,
                 'kg C': KG_CARBON,
                 'kg CO2': KG_CARBON_DIOXIDE,
                 'kg CO2 eq': KG_CARBON_DIOXIDE
             })
```
