# Transport Mode

[`TransportMode`](#pod_lca.transportation.TransportMode) class manages various aspects of transportation modes, including their [`Impacts`](impact_records.md#pod_lca.impacts.Impacts) and [`Emissions`](impact_records.md#pod_lca.impacts.Emissions). [`ElectricTransportMode`](#pod_lca.transportation.ElectricTransportMode) is a specific class abstracted to manage electric vehicles and calls the electricity module to manage the impacts and emissions associated.

---

### *class* pod_lca.transportation.TransportMode

Transportation mode object.

#### parent

Transportation leg to which the transportation mode correspond to.

* **Type:**
  [*TransportationLeg*](logistics_link.md#pod_lca.transportation.TransportationLeg)

#### mode_name

The name of the transportation mode.

* **Type:**
  {'Truck', 'E_Truck', 'Rail', 'Barge', 'Ocean', 'Air'}

#### efficiency

The efficiency level.

* **Type:**
  {'High', 'Median', 'Low'}

#### unit_impacts

Impacts from the transportation mode, per unit of declared quantity.

* **Type:**
  [*Impacts*](impact_records.md#pod_lca.impacts.Impacts)

#### unit_emissions

Emissions from the transportation mode, per unit of declared quantity.

* **Type:**
  [*Emissions*](impact_records.md#pod_lca.impacts.Emissions)

#### declared_unit

The declared unit corresponding to inventories.

* **Type:**
  [*Unit*](units.md#pod_lca.units.Unit)

#### faf_mode

FAF mode code for the transportation mode.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### cfs_mode

CFS mode code for the transportation mode.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### *classmethod* new(mode_name, efficiency='Median')

Create a new transportation mode.

* **Parameters:**
  * **mode_name** ( *{'Truck'* *,*  *'E_Truck'* *,*  *'Rail'* *,*  *'Barge'* *,*  *'Ocean'* *,*  *'Air'}*) -- The name of the transportation mode.
  * **efficiency** ( *{'High'* *,*  *'Median'* *,*  *'Low'}*) -- The efficiency level.
* **Returns:**
  An instance of the TransportMode class with the specified parameters.
* **Return type:**
  [*TransportMode*](#pod_lca.transportation.TransportMode)

#### set_parent(parent)

Set the parent transportation leg.

* **Parameters:**
  **parent** ([*TransportationLeg*](logistics_link.md#pod_lca.transportation.TransportationLeg)) -- The transportation leg to which this mode belong.

#### set_name(mode_name: [str](https://docs.python.org/3/library/stdtypes.html#str))

Set the name of the transportation mode.

* **Parameters:**
  **mode_name** ( *{'Truck'* *,*  *'E_Truck'* *,*  *'Rail'* *,*  *'Barge'* *,*  *'Ocean'* *,*  *'Air'}*) -- The name of the transportation mode.

#### set_efficiency(efficiency: [str](https://docs.python.org/3/library/stdtypes.html#str))

Set the efficiency of the transportation mode.

* **Parameters:**
  **efficiency** ( *{'High'* *,*  *'Median'* *,*  *'Low'}*) -- the efficiency level.

#### get_parent()

Set the parent transportation leg.

* **Returns:**
  The transportation leg to which this mode belong.
* **Return type:**
  [*TransportationLeg*](logistics_link.md#pod_lca.transportation.TransportationLeg)

#### get_name()

Retrieve the name of the transportation mode.

* **Returns:**
  The name of the transportation mode.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_efficiency()

Retrieve the efficiency of the transportation mode.

* **Returns:**
  the efficiency level.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_unit_impacts()

Get unit impacts from the transportation mode.

* **Returns:**
  Impacts from the transportation mode, per declared quantity and unit.
* **Return type:**
  [*Impacts*](impact_records.md#pod_lca.impacts.Impacts)

#### get_unit_emissions()

Get unit emissions from the transportation mode.

* **Returns:**
  Emissions from the transportation mode, per declared quantity and unit.
* **Return type:**
  [*Emissions*](impact_records.md#pod_lca.impacts.Emissions)

#### get_declared_unit()

Get the declared unit of the transportation mode.

* **Returns:**
  The unit corresponding to declared quantity of inventories.
* **Return type:**
  [*Unit*](units.md#pod_lca.units.Unit)

#### get_impact_database()

Get the impact database.

* **Returns:**
  Impacts database
* **Return type:**
  [*ImpactsDatabase*](impact_databases.md#pod_lca.impacts.ImpactsDatabase)

#### set_inventory_records()

Set unit inventory records of impacts and emissions for the transportation mode.

### *class* pod_lca.transportation.ElectricTransportMode

Bases: [`TransportMode`](#pod_lca.transportation.TransportMode)

Transportation mode using electricity.

#### location

Location where the electricity consumption occurs.

* **Type:**
  [*Location*](location_module.md#pod_lca.location.Location)

#### year

The year of electricity consumption.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### electricity_consumption

Electricity consumption by the transportation mode.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### electricity_consumption_units

Unit corresponding to electricity consumption.

* **Type:**
  [*Unit*](units.md#pod_lca.units.Unit)

#### set_location(location)

Set the location of electricity consumption (i.e., where the vehcile is charged).

* **Parameters:**
  **location** ([*Location*](location_module.md#pod_lca.location.Location)) -- Location of electricity consumption.

#### get_location()

Get the location of electricity consumption.

* **Returns:**
  Location of electricity consumption.
* **Return type:**
  [*Location*](location_module.md#pod_lca.location.Location)

#### get_electricity_consumption()

Retrieve the electricity consumption of the transportation mode.

* **Returns:**
  * [`float`](https://docs.python.org/3/library/functions.html#float) -- Electricity consumption.
  * [`Unit`](units.md#pod_lca.units.Unit) -- Corresponding unit of measurement.

#### get_electricity_inventories()

Get electricity impacts and emission for the transportation mode.

#### NOTE
1. Uses 'National' average electricity consumption, at the 'MidCase' scenario for the calculation of the electricity impacts.

* **Returns:**
  * [`Impacts`](impact_records.md#pod_lca.impacts.Impacts) -- Unit electricity impacts.
  * [`Emissions`](impact_records.md#pod_lca.impacts.Emissions) -- Unit electricity emissions.
  * [`Unit`](units.md#pod_lca.units.Unit) -- Corresponding electricity supply unit.

#### set_inventory_records()

Set unit inventory records of impacts and emissions for the transportation mode.
