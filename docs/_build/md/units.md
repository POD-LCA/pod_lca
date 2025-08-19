# Units

[`Unit`](#pod_lca.units.Unit) and [`MetricPrefix`](metric_prefixes.md#pod_lca.units.MetricPrefix) objects manage unit multiplication/division and unit conversions.

---

### *class* pod_lca.units.Unit

Unit object from which units are created.

#### name

Common name of the unit.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### standard_notation

Standard notation of the unit.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### qty_measured

The quantity measured by the unit.

* **Type:**
  {'time', 'mass', 'length', 'area', 'volume', 'power', 'energy', 'count', 'carbon storage'}

#### base_unit

Base unit of the Obj. None if itself a base unit.

* **Type:**
  [*Unit*](#pod_lca.units.Unit)

#### prefix

Metric prefix. None if a base unit or non-metric.

* **Type:**
  [*MetricPrefix*](metric_prefixes.md#pod_lca.units.MetricPrefix)

#### convert_compound

If True, unit conversion assuming the unit to be a compound unit.

* **Type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### components

List of components the unit is made up of. None if not a compound unit

* **Type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Unit*](#pod_lca.units.Unit)

#### *classmethod* from_basics(name, standard_notation, qty_measured)

Create a unit from basic data.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Common name of the unit.
  * **standard_notation** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Standard notation of the unit.
  * **qty_measured** ( *{'time'* *,*  *'mass'* *,*  *'length'* *,*  *'area'* *,*  *'volume'* *,*  *'power'* *,*  *'energy'* *,*  *'count'* *,*  *'carbon storage'}*) -- The quantity measured by the unit.

#### set_name(name)

Set the name of the unit of measurement.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the unit of measurement.

#### set_standard_notation(standard_notatoion)

Set the standard notation of the unit of measurement.

* **Parameters:**
  **standard_notatoion** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Standard notation of the unit of measurement.

#### set_qty_measured(qty_measured)

Set the quantity measured by the unit of measurement.

* **Parameters:**
  **qty_measured** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Quantity measured by the unit of measurement.

#### get_name()

Get the name of the unit of measurement.

* **Returns:**
  Name of the unit of measurement.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_standard_notation()

Retrieve the standard notation of the unit of measurement.

* **Returns:**
  Standard notation of the unit of measurement.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_qty_measured()

Get the quantity measured by the unit of measurement.

* **Returns:**
  Quantity measured by the unit of measurement.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_base()

Retrieve the base unit of the unit of measurement, if exist.

* **Returns:**
  Base unit of measurement, or None if itself a base unit of measurement.
* **Return type:**
  [*Unit*](#pod_lca.units.Unit)

#### get_prefix()

Retrieve the metric prefix of the unit of measurement, if exist.

* **Returns:**
  Metric prefix of the unit of measurement, or None if no prefix.
* **Return type:**
  [*MetricPrefix*](metric_prefixes.md#pod_lca.units.MetricPrefix)

#### get_components()

Retrieve components of the unit of measurement, if a compound unit.

* **Returns:**
  List of component units, or None if not a compound unit.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Unit*](#pod_lca.units.Unit)

#### convert_to(to_unit)

Returns conversion factor.

* **Parameters:**
  **to_unit** ([*Unit*](#pod_lca.units.Unit)) -- Unit of measurement to which the value will be converted to (from the current unit of measuremnt).
* **Returns:**
  Conversion factor to be applied on the value.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Incompatible units for conversion.

#### *static* compute_conversion_factor(unit_in, unit_out, qty_measured)

Computes conversion factor from unit_in to unit_out, given (a) They both measure same quantities, and
: 1. they are not compound units.

* **Parameters:**
  * **unit_in** ([*Unit*](#pod_lca.units.Unit)) -- Unit of measurement from which the value will be converted.
  * **unit_out** ([*Unit*](#pod_lca.units.Unit)) -- Unit of measurement to which the value will be converted.
  * **qty_measured** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Quantity measured by the units of measruements considered.
* **Returns:**
  Conversion factor to be applied on the value.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)
