# Electricity Generation

[`ElectricityProducer`](#pod_lca.electricity.ElectricityProducer) class manages the electricity generation aspects including [`Impacts`](inventory-records.md#pod_lca.impacts.Impacts) and [`Emissions`](inventory-records.md#pod_lca.impacts.Emissions).

---

### *class* pod_lca.electricity.ElectricityProducer

Electricity generation facility (i.e., power station)

#### name

Name of the power station / facility.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### technology

Power generation technology.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### year

Year of power generation.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### unit_impacts

Impacts per declared unit of power generation.

* **Type:**
  [*Impacts*](inventory-records.md#pod_lca.impacts.Impacts)

#### unit_emissions

Emissions per declared unit of power generation.

* **Type:**
  [*Emissions*](inventory-records.md#pod_lca.impacts.Emissions)

#### declared_unit

Unit of power generation for which the impacts and emissions are declared.

* **Type:**
  [*Unit*](units-object.md#pod_lca.units.Unit)

#### *classmethod* from_technology_year(technology, year)

Create a new ElectricityProducer object with the given location

* **Parameters:**
  * **technology** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Power generation technology.
  * **year** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Year of power generation.
* **Returns:**
  A new ElectricityProducer object with the given location.
* **Return type:**
  [*ElectricityProducer*](#pod_lca.electricity.ElectricityProducer)

#### set_name(name)

Set the name of the electricity producer.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- The name of the electricity producer.

#### set_technology(technology)

Set the power generation technology.

* **Parameters:**
  **technology** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Power generation technology.

#### set_year(year)

Set the year of the power generation.

* **Parameters:**
  **year** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Year of power generation.

#### set_unit_impacts(impacts)

Set the impacts of the electricity producer, per unit of power generation.

* **Parameters:**
  **impacts** ([*Impacts*](inventory-records.md#pod_lca.impacts.Impacts)) -- Impacts per declared unit of power generation.

#### set_unit_emissions(emissions)

Set the emissions of the electricity producer, per unit of power generation.

* **Parameters:**
  **emissions** ([*Emissions*](inventory-records.md#pod_lca.impacts.Emissions)) -- Emissions per declared unit of power generation.

#### set_declared_unit(unit)

Set the declared unit of impacts.

* **Parameters:**
  **unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Declared unit.

#### get_name()

Get the name of the electricity producer.

* **Returns:**
  The name of the electricity producer.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_technology()

Get the power generation technology.

* **Returns:**
  Power generation technology.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_year()

Get the year of the power generation.

* **Returns:**
  The year of the electricity producer.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_unit_impacts()

Get the impacts of the electricity producer.

* **Returns:**
  Impacts per declared unit of power generation.
* **Return type:**
  [*Impacts*](inventory-records.md#pod_lca.impacts.Impacts)

#### get_unit_emissions()

Get the emissions of the electricity producer.

* **Returns:**
  Emissions per declared unit of power generation.
* **Return type:**
  [*Emissions*](inventory-records.md#pod_lca.impacts.Emissions)

#### get_declared_unit()

Set the declared unit of impacts.

* **Returns:**
  Declared unit.
* **Return type:**
  [*Unit*](units-object.md#pod_lca.units.Unit)
