# Metrix Prefixes

There is a definitive list of [`MetricPrefix`](#pod_lca.units.MetricPrefix) objects [1].

They can be imported as follows;

```python
from pod_lca.units import MEGA
```

| Metric Prefix Object Name   | Prefix Name   | Symbol   |   Exponent |
|-----------------------------|---------------|----------|------------|
| YOTTA                       | yotta         | Y        |         24 |
| ZETTA                       | zetta         | Z        |         21 |
| EXA                         | exa           | E        |         18 |
| PETA                        | peta          | P        |         15 |
| TERA                        | tera          | T        |         12 |
| GIGA                        | giga          | G        |          9 |
| MEGA                        | mega          | M        |          6 |
| KILO                        | kilo          | k        |          3 |
| HECTO                       | hecto         | h        |          2 |
| DEKA                        | deka          | da       |          1 |
| DECI                        | deci          | d        |         -1 |
| CENTI                       | centi         | c        |         -2 |
| MILI                        | mili          | m        |         -3 |
| MICRO                       | micro         | mu       |         -6 |
| NANO                        | nano          | n        |         -9 |
| PICO                        | pico          | p        |        -12 |
| FEMTO                       | femto         | f        |        -15 |
| ATTO                        | atto          | a        |        -18 |
| ZEPTO                       | zepto         | z        |        -21 |
| YOCTO                       | yocto         | y        |        -24 |

Reference:

[1]  National Institute of Standards and Technology (NIST) Handbook 44 (2024). Specifications, Tolerances, and Other Technical Requirements for Weighing and Measuring Devices.

### *class* pod_lca.units.MetricPrefix(name, symbol, power)

Unit object from which units are created.

#### name

Standard name of the prefix.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### symbol

Standard symbol of the unit.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### power

Power to the ten corresponding to the prefix.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_name()

Retrieve the name of the prefix.

* **Returns:**
  Standard name of the prefix.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_symbol()

Retrieve the symbol of the prefix.

* **Returns:**
  Symbol of the prefix.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_power()

Retrieve the power to the ten corresponding to the prefix.

* **Returns:**
  Power to the ten corresponding to the prefix.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### convert_to(to_prefix)

Compute conversion factor for converting preixes.

* **Parameters:**
  **to_prefix** ([*MetricPrefix*](#pod_lca.units.MetricPrefix)) -- Metric prefix to which the value will be converted to (from the current metric prefix).
* **Returns:**
  Conversion factor to be applied on the value.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)
