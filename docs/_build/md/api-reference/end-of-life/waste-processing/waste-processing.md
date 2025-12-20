# Waste Processing

[`WasteProcess`](#pod_lca.eol.WasteProcess) maintains data relevant to the end-of-life pathways, including their [`Impacts`](inventory-records.md#pod_lca.impacts.Impacts) and [`Emissions`](inventory-records.md#pod_lca.impacts.Emissions).

---

### *class* pod_lca.eol.WasteProcess

Waste process a waste object is subjected to.

#### parent

Waste object for which the waste processing belong.

* **Type:**
  [*Waste*](waste-products.md#pod_lca.eol.Waste)

#### process_name

End-of-life pathway:

- 'Landfill': transporting waste to a landfill.
- 'Recycle': transporting waste to a recycler.
- 'Compost': transporting to a composting facility.
- 'Incinerate': transporting to an incinerator.

Default to 'Incinerate'.

* **Type:**
  {'Landfill', 'Recycle', 'Compost', 'Incinerate'}

#### qty

Quantity of the parent object subjected to this process.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### unit

Unit of measurement.

* **Type:**
  [*Unit*](units-object.md#pod_lca.units.Unit)

#### life_cycle_stage

Life cycle stage of this process.

* **Type:**
  {'C3', 'C4', 'D'}

#### unit_impacts

Unit impacts of the process.

* **Type:**
  [*Impacts*](inventory-records.md#pod_lca.impacts.Impacts)

#### unit_emissions

Unit emissions of the process.

* **Type:**
  [*Emissions*](inventory-records.md#pod_lca.impacts.Emissions)

#### location

Location where the process occurs.

* **Type:**
  [*Location*](location.md#pod_lca.location.Location)

#### transporation_leg

Transportation of the waste object from parent's location to process location.

* **Type:**
  [*TransportationLeg*](logistics-leg.md#pod_lca.transportation.TransportationLeg)

#### linked_to

A follow up process. e.g, Recycle processing (C3) and Reuse (D).

* **Type:**
  [*WasteProcess*](#pod_lca.eol.WasteProcess)

#### linked_from

A previous end-of-life process. e.g, Recycle processing (C3) and Reuse (D).

* **Type:**
  [*WasteProcess*](#pod_lca.eol.WasteProcess)

#### *classmethod* new(parent, process_name, qty, unit, life_cycle_stage, linked_process=None)

Create new waste process.

* **Parameters:**
  * **parent** ([*Waste*](waste-products.md#pod_lca.eol.Waste)) -- Waste object for which the waste processing belong.
  * **process_name** ( *{'Landfill'* *,*  *'Recycle'* *,*  *'Compost'* *,*  *'Incinerate'}*) -- 

    End-of-life pathway:
    - 'Landfill': transporting waste to a landfill.
    - 'Recycle': transporting waste to a recycler.
    - 'Compost': transporting to a composting facility.
    - 'Incinerate': transporting to an incinerator.

    Default to 'Incinerate'.
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Quantity of the parent object subjected to this process.
  * **unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of measurement.
  * **life_cycle_stage** ( *{'C3'* *,*  *'C4'* *,*  *'D'}*) -- Life cycle stage of this process.
  * **linked_process** ( *{None* *,*  *'C4'* *,*  *'D'}*) -- Linked waste process.
* **Returns:**
  Waste process object.
* **Return type:**
  [*WasteProcess*](#pod_lca.eol.WasteProcess)

#### set_parent(parent)

Set parent Waste object of the Waste Processing.

* **Parameters:**
  **parent** ([*Waste*](waste-products.md#pod_lca.eol.Waste)) -- Waste object for which the waste processing belong.

#### set_process_name(name)

Set the process name.

* **Parameters:**
  **name** ( *{'Landfill'* *,*  *'Recycle'* *,*  *'Compost'* *,*  *'Incinerate'}*) -- 

  End-of-life pathway:
  - 'Landfill': transporting waste to a landfill.
  - 'Recycle': transporting waste to a recycler.
  - 'Compost': transporting to a composting facility.
  - 'Incinerate': transporting to an incinerator.

#### set_life_cycle_stage(life_cycle_stage)

Set life cycle stage of the product/process.

* **Parameters:**
  **life_cycle_stage** ( *{'C3'* *,*  *'C4'* *,*  *'D'}*) -- Life cycle stage of the product/process.

#### set_location(location)

Set location of the waste process facility.

* **Parameters:**
  **location** ([*Location*](location.md#pod_lca.location.Location)) -- Location of the waster process facility.

#### set_linked_process(process)

Set a linked process to the current process.

* **Parameters:**
  **process** ([*WasteProcess*](#pod_lca.eol.WasteProcess)) -- Secondary process following the current process.

#### get_parent()

Get parent Waste object of the Waste Processing.

* **Returns:**
  Waste object for which the waste processing belong.
* **Return type:**
  [*Waste*](waste-products.md#pod_lca.eol.Waste)

#### get_process_name()

Get the process name.

* **Returns:**
  Name of the process: e.g., 'Landfill', 'Recycle', 'Compost'
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_name()

Get name of the process identifying the parent and process.

* **Returns:**
  Name identifyer.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_qty()

Get quantity of the parent subjected to this waste process.

* **Returns:**
  Quantity of the parent object subjected to this process.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_unit()

Get unit of measurement for the waste amount processed.

* **Returns:**
  Unit of measurement.
* **Return type:**
  [*Unit*](units-object.md#pod_lca.units.Unit)

#### get_weight()

Get weight of the parent subjected to this waste process.

* **Returns:**
  Quantity of the parent object subjected to this process.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_weight_unit()

Get unit of measurement for the weight of waste processed.

* **Returns:**
  Unit of measurement.
* **Return type:**
  [*Unit*](units-object.md#pod_lca.units.Unit)

#### get_life_cycle_stage()

Retrieve the life cycle stage corresponding to the waste process.

* **Returns:**
  Corresponding life cycle stage.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_unit_impacts()

Get unit impacts of the waste process.

* **Returns:**
  Unit impacts of the process.
* **Return type:**
  [*Impacts*](inventory-records.md#pod_lca.impacts.Impacts)

#### get_unit_emissions()

Get unit emissions of the waste process.

* **Returns:**
  Unit emissions of the process.
* **Return type:**
  [*Emissions*](inventory-records.md#pod_lca.impacts.Emissions)

#### get_linked_process(to=True)

Get the linked process to the current process.

* **Parameters:**
  **to** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If True, return the process linked to, else linked from.
* **Returns:**
  Secondary process following the current process.
* **Return type:**
  [*WasteProcess*](#pod_lca.eol.WasteProcess)

#### get_transportation_leg()

Get the transportation leg corresponding to the end-of-life pathway.

* **Returns:**
  Secondary process following the current process.
* **Return type:**
  [*TransportationLeg*](logistics-leg.md#pod_lca.transportation.TransportationLeg)

#### update_unit_inventories()

Set unit impacts of the waste process.
