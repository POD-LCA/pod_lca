# Model

A material screening [`Model`](#pod_lca.materials_screening.Model) will maintain a list of [`Product`](python-library/Products and Processes.md#pod_lca.materials_screening.Product) and [`Process`](python-library/Products and Processes.md#pod_lca.materials_screening.Process) objects going into the material production.

This also is a point to retrive the LCA output (e.g., [`get_total_impact()`](#pod_lca.materials_screening.Model.get_total_impact))

---

### *class* pod_lca.materials_screening.Model

Model object is the canvas to which the processes and prodcuts are added.
: The corresponding calculations are based on models.

#### project

Project on which the calculator operates.

* **Type:**
  [*Project*](python-library/Project.md#pod_lca.materials_screening.Project)

#### name

Name of the model.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### location

Location of the project.

* **Type:**
  [*Location*](python-library/Location.md#pod_lca.location.Location)

#### processes

Processes in the model.

* **Type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Process*](python-library/Products and Processes.md#pod_lca.materials_screening.Process)

#### products

Products in the model.

* **Type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Product*](python-library/Products and Processes.md#pod_lca.materials_screening.Product)

#### transportation_manager

Logistics manager for the model.

* **Type:**
  [*TransportationManager*](python-library/Project Logistics Manager.md#pod_lca.transportation.TransportationManager)

#### impacts

Impacts of products and processes categorized by life cycle stage {**life cycle stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`Impacts`](python-library/Inventory Records.md#pod_lca.impacts.Impacts)}

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### emissions

Emissions of products and processes categorized by life cycle stage {**life cycle stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`Emissions`](python-library/Inventory Records.md#pod_lca.impacts.Emissions)}

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### carbon_storage

Carbon storage of products and processes categorized by life cycle stage {**life cycle stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`CarbonStorage`](python-library/Inventory Records.md#pod_lca.impacts.CarbonStorage)}

#### *classmethod* in_project(project, name=None, transport_scope='local')

Create a model object from a parent object.

* **Parameters:**
  * **project** (python-library/[*Project*](project.md#pod_lca.materials_screening.Project)) -- Project to which the model belong.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the model.
  * **transport_scope** ( *{'local'* *,*  *'global'}*) -- Transportation scope of the model.
* **Returns:**
  Model object created.
* **Return type:**
  [*Model*](#pod_lca.materials_screening.Model)

#### *classmethod* from_CSV(file_path, project, name=None)

Create a model from data in a csv file.
: The csv file with headers: "Name", "Impact data", "type", "LC stage", "qty", "unit", "transported item", "density", "weight unit" (in any order).
  Transported item is the name of the product transported.
  Quantity in the transportation process should be the distance.

* **Parameters:**
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the csv file.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the model to be created.
  * **project** (python-library/[*Project*](project.md#pod_lca.materials_screening.Project)) -- Project to which the model belong.
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Item type not recognized.

#### set_project(project)

Set the project object.

* **Parameters:**
  **project** (python-library/[*Project*](project.md#pod_lca.materials_screening.Project)) -- Project to which the model belong.

#### set_name(name)

Set the name of the model.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the model.

#### set_location(location)

Set the location of the model.

* **Parameters:**
  **location** (python-library/[*Location*](location.md#pod_lca.location.Location)) -- Location of the model.

#### set_transportation_manager(logistic_type='local')

Set the logistics manager of the model.

* **Parameters:**
  **logistic_type** ( *{'local'* *,*  *'global'}*) -- Transportation scope of the model.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Logistic type not recognized.

#### get_project()

Retrieve the project object.

* **Returns:**
  Project to which the model belong.
* **Return type:**
  [*Project*](python-library/Project.md#pod_lca.materials_screening.Project)

#### get_name()

Retrieve the name of the model.

* **Returns:**
  Name of the model.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_location()

Retrieve the location of the model.

* **Returns:**
  Location of the model.
* **Return type:**
  [*Location*](python-library/Location.md#pod_lca.location.Location)

#### get_processes()

Retrieve all the processes in the model.

* **Returns:**
  All processes in the model.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Process*](python-library/Products and Processes.md#pod_lca.materials_screening.Process)

#### get_products()

Retrieve all the products in the model.

* **Returns:**
  All products in the model.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Product*](python-library/Products and Processes.md#pod_lca.materials_screening.Product)

#### get_all_items()

Retrieve all the products and processes in the model.

* **Returns:**
  All products and processess in the model.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Master*](python-library/Products and Processes.md#pod_lca.materials_screening.Master)

#### get_transportation_manager()

Retrieve the logistics manager of the model.

* **Returns:**
  Logistics manager for the model.
* **Return type:**
  [*TransportationManager*](python-library/Project Logistics Manager.md#pod_lca.transportation.TransportationManager)

#### get_impacts()

Retrieve all the impacts in the model categorized by life cycle stage.

* **Returns:**
  Impacts of products and processes categorized by life cycle stage {**life cycle stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`Impacts`](python-library/Inventory Records.md#pod_lca.impacts.Impacts)}
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### get_emissions()

Retrieve all the emissions in the model categorized by life cycle stage.

* **Returns:**
  Emissions of products and processes categorized by life cycle stage {**life cycle stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`Emissions`](python-library/Inventory Records.md#pod_lca.impacts.Emissions)}
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### get_carbon_storage()

Retrieve all the carbon storage in the model categorized by life cycle stage.

* **Returns:**
  Carbon Storage of products and processes categorized by life cycle stage {**life cycle stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`CarbonStorage`](python-library/Inventory Records.md#pod_lca.impacts.CarbonStorage)}
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### add_process(name, stage, qty, unit, impacts_from)

Create and add process to the model.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the process.
  * **stage** ( *{'A3'}*) -- Life cycle stage.
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Quantity processed.
  * **unit** (python-library/[*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of the quantity.
  * **impacts_from** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the impact database entry from which to use impacts.
* **Returns:**
  Process object created.
* **Return type:**
  [*Process*](python-library/Products and Processes.md#pod_lca.materials_screening.Process)

#### add_product(name, stage, qty, unit, impacts_from, \*\*kwargs)

Create and add product to the model.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the product.
  * **stage** ( *{'A1'}*) -- Life cycle stage.
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Product quantity.
  * **unit** (python-library/[*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of measurement.
  * **impacts_from** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the impact database entry from which to use impacts.
  * **sctg_code** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Standard Classification of Transported Goods (SCTG) code of the material.
  * **density** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Density of the material.
  * **density_unit** (python-library/[*Unit*](units-object.md#pod_lca.units.Unit)) -- Units corresponding to material density.
  * **ignore_transport** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, ignore setting transportation.
* **Returns:**
  Product object created.
* **Return type:**
  [*Product*](python-library/Products and Processes.md#pod_lca.materials_screening.Product)

#### add_energy(name, stage, qty, unit, impacts_from)

Create and add energy product to the model.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the product.
  * **stage** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Life cycle stage.
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Product quantity.
  * **unit** (python-library/[*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of measurement.
  * **impacts_from** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the impact database entry from which to use impacts.
* **Returns:**
  Energy product object created.
* **Return type:**
  [*Fuel*](python-library/Products and Processes.md#pod_lca.materials_screening.Fuel)

#### add_electricity(name, stage, qty, unit=<pod_lca.units.units.Unit object>)

Create and add electricity product to the model.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the product.
  * **stage** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Life cycle stage: 'A1', 'A2', 'A3'.
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Product quantity.
  * **unit** (python-library/[*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of measurement.
* **Returns:**
  Electricity object created.
* **Return type:**
  [*Electricity*](python-library/Products and Processes.md#pod_lca.materials_screening.Electricity)

#### find_item(name)

Find an item (product/process) in the model, given a name string.
: If multiple objects of the same name exist, returns all.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Product/Process name searched for.
* **Returns:**
  Product / Process object
* **Return type:**
  [*Master*](python-library/Products and Processes.md#pod_lca.materials_screening.Master)

#### delete_item(obj)

Removes products or processes, along with the impact objects, from the model.

* **Parameters:**
  **obj** (python-library/[*Master*](products-and-processes.md#pod_lca.materials_screening.Master)) -- Product or process to be removed from the model.

#### get_total_impact(impact_cat)

Calculate the total impact of the products and processes in the model.

* **Parameters:**
  **impact_cat** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Impact category considered, including 'weighted'.
* **Returns:**
  Total impact value.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)
* **Raises:**
  [**AttributeError**](https://docs.python.org/3/library/exceptions.html#AttributeError) -- Impact category not recognized.

#### get_impacts_by_LCstages(impact_cat)

Returns impact data by life cycle stage for given model and impact category.

* **Parameters:**
  **impact_cat** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of impact category.
* **Returns:**
  Impacts dictionary where {**Life Cycle stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : **quantity of impact** ([`float`](https://docs.python.org/3/library/functions.html#float))}.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)
* **Raises:**
  [**AttributeError**](https://docs.python.org/3/library/exceptions.html#AttributeError) -- impact category doe not exist in the current project

#### get_impacts_by_category()

Returns impact data by impact category for given model.

* **Returns:**
  Impacts dictionary where {**Life Cycle stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : **quantity of impact** ([`float`](https://docs.python.org/3/library/functions.html#float))}.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### get_normalized_impacts_by_category()

Returns impact data by impact category for given model.

* **Parameters:**
  **model** ([*Model*](#pod_lca.materials_screening.Model)) -- The model considered.
* **Returns:**
  Impacts dictionary where {**Life Cycle stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : **quantity of impact** ([`float`](https://docs.python.org/3/library/functions.html#float))}.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)
* **Raises:**
  [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- Impact category not recognized.

#### set_products_electricity_source(source)

Assign source for all products of the model.

* **Parameters:**
  **source** ( *{'from_database'* *,*  *'by_location'}*) -- Source of electricity inventories data. Default 'from_database'

#### get_drf_record(time_horizon=100, time_step=0.08333333333333333)

Get the dynamic radiative forcing record for all the products and procesess in the model.

* **Parameters:**
  * **time_horizon** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Time horizon in years.
  * **time_step** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Time step of the record. The same time step is used for both for integration and for reporting.
* **Returns:**
  Dynamic Radiative Forcing Record
* **Return type:**
  *DynamicRadiativeForcingRecord*
