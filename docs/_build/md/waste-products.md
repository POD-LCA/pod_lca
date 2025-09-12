# Waste Products

[`Waste`](#pod_lca.eol.Waste) maintains data relevant to the end-of-life of a material, including the mix of end-of-life pathways.

---

### *class* pod_lca.eol.Waste

Bases: [`Product`](products-and-processes.md#pod_lca.materials_screening.Product)

Waste product handling the end-of-life or product.

#### parent

The thing being was converted to waste.

* **Type:**
  *BuildingComponent* or [*Product*](products-and-processes.md#pod_lca.materials_screening.Product)

#### waste_processes

List of processes the waste will be subjected to. These processes are in parallel.

* **Type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*WasteProcess*](waste-processing.md#pod_lca.eol.WasteProcess)

#### process_mix

The mix of processes the waste product will be subject to: {**process name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **percentage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str) or [`float`](https://docs.python.org/3/library/functions.html#float))}.
Percentage can be in the form of string with a % sign or decimal value.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### impacts

Impact objects categorized by life cycle stage {**life cycle stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): list of [`Impacts`](inventory-records.md#pod_lca.impacts.Impacts)}

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### emissions

Emission objects categorized by life cycle stage {**life cycle stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): list of [`Emissions`](inventory-records.md#pod_lca.impacts.Emissions)}

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### bio_based

True if the material is bio-based.

* **Type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### *classmethod* new(parent, database_item, qty, unit, process_mix, bio_based=None)

Create new waste product.

* **Parameters:**
  * **parent** (*BuildingComponent* *or* [*Product*](products-and-processes.md#pod_lca.materials_screening.Product)) -- The thing that which was converted to waste.
  * **database_item** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Material name corresponding to the database entry which gives the unit impact of the product.
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Quantity of the product/process.
  * **unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of measurement corresponding to the quantity of the product/process.
  * **process_mix** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- The mix of processes the waste product will be subject to: {**process name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **percentage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str) or [`float`](https://docs.python.org/3/library/functions.html#float))}.
    Percentage can be in the form of string with a % sign or decimal value.
  * **bio_based** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- True if the material is bio-based.
* **Returns:**
  Waste product.
* **Return type:**
  [*Waste*](#pod_lca.eol.Waste)

#### set_parent(parent)

Set parent of the waste product.

* **Parameters:**
  **parent** (*BuildingComponent* *or* [*Product*](products-and-processes.md#pod_lca.materials_screening.Product)) -- The thing that which was converted to waste.

#### set_impact_database_entry(database_item: [str](https://docs.python.org/3/library/stdtypes.html#str))

Sets the impacts database entry corresponding to the item.
This method will also update the corresponding impact quanitities.

* **Parameters:**
  **database_item** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- The name of the database item which gives the item impacts.

#### set_waste_processess()

Set waste processe for the waste product. Also sets the process mix.

### Notes

The waste mix allocated to any process which is beyond its cutoff distance is reallocated to Landfill.

* **Parameters:**
  **process_mix** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- The mix of processes the waste product will be subject to: {**process name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **percentage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str) or [`float`](https://docs.python.org/3/library/functions.html#float))}.
  Percentage can be in the form of string with a % sign or decimal value.

#### set_waste_process(process_name, process_qty)

Set waste process. If cutoff due to distance, returns the unprocessed waste quantity.

* **Parameters:**
  * **process_name** ( *{'Landfill'* *,*  *'Recycle'* *,*  *'Compost'* *,*  *'Incinerate'}*) -- 

    End-of-life pathway:
    - 'Landfill': transporting waste to a landfill.
    - 'Recycle': transporting waste to a recycler.
    - 'Compost': transporting to a composting facility.
    - 'Incinerate': transporting to an incinerator.
  * **process_qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Quantity of waste subjected to this process
* **Returns:**
  * [`WasteProcess`](waste-processing.md#pod_lca.eol.WasteProcess) -- If the process is not cutoff
  * [`float`](https://docs.python.org/3/library/functions.html#float) -- If the process is cutoff, the balance waste quantity to be processed

#### set_bio_based(is_bio_based)

Set the bio-based nature of the material.

* **Parameters:**
  **is_bio_based** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- True, if the material is bio-based.

#### set_process_mix(process_mix)

Get the mix of process the waste product is subjected to.

* **Parameters:**
  **dict** -- The mix of processes the waste product will be subject to: {**process name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **percentage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str) or [`float`](https://docs.python.org/3/library/functions.html#float))}.
  Percentage can be in the form of string with a % sign or decimal value.
* **Raises:**
  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Mix percentates are unrecognized.
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Mix percentages does not sum to 100%.

#### get_parent()

Get parent of the waste product.

* **Returns:**
  The thing that which was converted to waste.
* **Return type:**
  *BuildingComponent* or [*Product*](products-and-processes.md#pod_lca.materials_screening.Product)

#### get_waste_processes()

Get waste processe for the waste product.

* **Returns:**
  List of processes the waste will be subjected to. These processes are in parallel.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*WasteProcess*](waste-processing.md#pod_lca.eol.WasteProcess)

#### get_process_mix(process_name=None, mode='assigned')

Get the mix of process the waste product is subjected to.

* **Parameters:**
  * **process_name** ( *{'Landfill'* *,*  *'Recycle'* *,*  *'Compost'* *,*  *'Incinerate'}*) -- 

    End-of-life pathway:
    - 'Landfill': transporting waste to a landfill.
    - 'Recycle': transporting waste to a recycler.
    - 'Compost': transporting to a composting facility.
    - 'Incinerate': transporting to an incinerator.
  * **mode** ( *{'assigned'* *,*  *'actual'}*) -- 

    Mode of calculation used for process mix;
    - 'assigned': the prescribed process mix.
    - 'actual': realized process mix. The differences due to cut-off distances are considered.

    Default is 'assigned'
* **Returns:**
  The mix of processes the waste product will be subject to: {**process name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **percentage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str) or [`float`](https://docs.python.org/3/library/functions.html#float))}.
  Percentage can be in the form of string with a % sign or decimal value.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Calculation mode not recognized.

#### get_bio_based()

Get the bio-based nature of the material.

* **Returns:**
  True, if the material is bio-based.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### update_inventory_records()

Update the transportation and processing impacts of the waste (C2-C4).

#### update_waste_processess()

Update the waste processess.

### Notes

The waste mix allocated to any process which is beyond its cutoff distance is reallocated to Landfill.

#### *static* check_mix_sum(process_mix, tol=1e-05)

check if the process mix adds up to 100%.

* **Parameters:**
  * **process_mix** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- The mix of processes the waste product will be subject to: {**process name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **percentage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str) or [`float`](https://docs.python.org/3/library/functions.html#float))}.
    Percentage can be in the form of string with a % sign or decimal value.
  * **tol** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Tolerence checked against
* **Returns:**
  True if the sum of the mix percentages adds upto a 100%, within tolerence.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)
