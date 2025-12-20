# Products and Processes

[`Product`](#pod_lca.materials_screening.Product) and [`Process`](#pod_lca.materials_screening.Process) objects keeps track of product/process quantities and their LCA data (e.g., [`Impacts`](inventory-records.md#pod_lca.impacts.Impacts), [`Emissions`](inventory-records.md#pod_lca.impacts.Emissions)). They both inherit from the abstract class [`Master`](#pod_lca.materials_screening.Master).

Furthermore, they keep track of advanced analysis options such as [`is_hotspot`](#pod_lca.materials_screening.Master.is_hotspot), [`data_distribution`](#pod_lca.materials_screening.Master.data_distribution) and [`pedigree_score`](#pod_lca.materials_screening.Master.pedigree_score).

[`Product`](#pod_lca.materials_screening.Product) object keep track of its electricity usage (if the database provides data disagregated for electricity consumption), allowing swapping out of electricity based on project location ([`set_electricity_source()`](#pod_lca.materials_screening.Product.set_electricity_source)).

---

### *class* pod_lca.materials_screening.Master

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Master object from which product and process objects inherit.

#### id

An identification number.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### model

Model object to which this product/process belong.

* **Type:**
  [*Model*](model.md#pod_lca.materials_screening.Model)

#### name

Name of the product/process.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### life_cycle_stage

Life cycle stage corresponding to the product/process.

* **Type:**
  {'A1', 'A3'}

#### impact_database_entry

Flow name corresponding to the database entry which gives the unit impact of the product.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### qty

Quantity of the product/process.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### unit

Unit of measurement corresponding to the quantity of the product/process.

* **Type:**
  [*Unit*](units-object.md#pod_lca.units.Unit)

#### impacts

Total impacts of the product/process.

* **Type:**
  [*Impacts*](inventory-records.md#pod_lca.impacts.Impacts)

#### emissions

Total emissions of the product/process.

* **Type:**
  [*Emissions*](inventory-records.md#pod_lca.impacts.Emissions)

#### carbon_storage

Total carbon storage of the product/process.

* **Type:**
  [*CarbonStorage*](inventory-records.md#pod_lca.impacts.CarbonStorage)

#### unit_impacts

Unit impacts of the product/process.

* **Type:**
  [*Impacts*](inventory-records.md#pod_lca.impacts.Impacts)

#### unit_emissions

Unit emissions of the product/process.

* **Type:**
  [*Emissions*](inventory-records.md#pod_lca.impacts.Emissions)

#### unit_carbon_storage

Carbon storage corresponding to the product/process.

* **Type:**
  [*CarbonStorage*](inventory-records.md#pod_lca.impacts.CarbonStorage)

#### inventories_declared_unit

Declared unit of impacts

* **Type:**
  [*Unit*](units-object.md#pod_lca.units.Unit)

#### inventories_declared_qty

Declared quantity of impacts

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### is_hotspot

True, if the object is a hotspot in the model.

* **Type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### data_distribution

Data distributions corresponding to attributes: {**attr** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): `DataDistribution`}.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### pedigree_score

Data quality indicator for the object

* **Type:**
  *PedigreeScore*

#### *classmethod* new(id, name, model, stage, qty, unit, impacts_from)

Create a new item in a model.

* **Parameters:**
  * **id** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- An identification number.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the item.
  * **model** ([*Model*](model.md#pod_lca.materials_screening.Model)) -- Model in which the item is created.
  * **stage** ( *{'A1'* *,*  *'A3'}*) -- LCA stage.
    - 'A1': Raw materials supply.
    - 'A3': manufacturing.
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Quantity of the item
  * **unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit corresponding to the quantity.
  * **impacts_from** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the impact database entry from which to use impacts.

#### *classmethod* copy(obj)

Make a copy of an object.

* **Returns:**
  Copy of the object.
* **Return type:**
  [*Master*](#pod_lca.materials_screening.Master)

#### set_id(id)

Set the product/process id.

* **Parameters:**
  **id** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Item identification number.

#### set_model(model)

Set the model corresponding to the product/process.

* **Parameters:**
  **model** ([*Model*](model.md#pod_lca.materials_screening.Model)) -- Model corresponding to the product/process.

#### set_life_cycle_stage(stage)

Set life cycle stage of the product/process.

* **Parameters:**
  **stage** ( *{'A1'* *,*  *'A3'}*) -- Life cycle stage of the product/process.
  - 'A1': Raw materials supply.
  - 'A3': manufacturing.

#### set_name(name)

Set name of the product/process.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the product/process.

#### set_impact_database_entry(database_item)

Sets the database (impacts) entry corresponding to the item.
: This method will also update the corresponding impact quanitities.

* **Parameters:**
  **database_item** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- The name of the database item which gives the item impacts.

#### set_qty(qty)

Update the qty of the item.
: This will also re-calculate the corresponding impact quantities.

* **Parameters:**
  **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Production quantity.
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Qunatity should be a number.

#### set_unit(unit)

Set unit of measurement for the product/process.

* **Parameters:**
  **unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of measurement.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Incompatible units.

#### set_data_distribution(distribution, attr)

Set a data_distribution object to the Master Obj.

* **Parameters:**
  * **distribution** (*DataDistribution*) -- DataDistribution object to be set
  * **attr** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Attribute to which the distribution correspond.

#### set_pedigree_score(pedigree_score)

Set a pedigree score (data quality score) to the Master Obj.

* **Parameters:**
  **pedigree_score** (*PedigreeScore*) -- Data quality indicator for the object

#### get_id()

Retrieve the identification number of the product/process.

* **Returns:**
  Identification number of the product/process.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_model()

Retrieve the model corresponding to the product/process.

* **Returns:**
  Model corresponding to the product/process.
* **Return type:**
  [*Model*](model.md#pod_lca.materials_screening.Model)

#### get_name()

Retrieve the name of the product/process.

* **Returns:**
  Name of the product/process.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_life_cycle_stage()

Retrieve the life cycle stage corresponding to the product/process.

* **Returns:**
  Corresponding life cycle stage.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_impact_database_entry()

Retrieve the impact database row corresponding to the product/process.

* **Returns:**
  Flow name corresponding to the database entry which gives the unit impact of the product.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_qty()

Retrieve the quantity of the product/process.

* **Returns:**
  Quantity of the product/process.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_unit()

Retrieve the unit of measurement of the product/process.

* **Returns:**
  Unit of measurement of the product/process.
* **Return type:**
  *Units*

#### get_impacts()

Retrieve the impacts of the product/process.

* **Returns:**
  Impacts of the product/process.
* **Return type:**
  [*Impacts*](inventory-records.md#pod_lca.impacts.Impacts)

#### get_impact_database()

Get the impacts database of the project.

* **Returns:**
  Impact database of the project.
* **Return type:**
  [*ImpactsDatabase*](impacts-database.md#pod_lca.impacts.ImpactsDatabase)

#### get_emissions()

Retrieve the emissions of the product/process.

* **Returns:**
  Emissions of the product/process.
* **Return type:**
  [*Emissions*](inventory-records.md#pod_lca.impacts.Emissions)

#### get_carbon_storage()

Retrieve the carbon storage of the product/process.

* **Returns:**
  Carbon storage of the product/process.
* **Return type:**
  [*CarbonStorage*](inventory-records.md#pod_lca.impacts.CarbonStorage)

#### get_data_distributions()

Get data_distribution objects of the Master obj.

* **Returns:**
  DataDistribution objects corresponding to attributes: {**attr** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): `DataDistribution`}
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### get_data_distribution(attr)

Get data_distribution object corresponding to the given attribute.

* **Parameters:**
  **attr** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Attribute to which the distribution correspond.
* **Returns:**
  Data distribution.
* **Return type:**
  *DataDistribution*

#### get_pedigree_score()

Get pedigree score of the product/process.

* **Returns:**
  Data quality indicator for the object
* **Return type:**
  *PedigreeScore*

#### get_project()

Retrieve the corresponding project.

* **Returns:**
  Corresponding project.
* **Return type:**
  [*Project*](project.md#pod_lca.materials_screening.Project)

#### get_parent()

Get the parent of the object.

## Retruns

~pod_lce.materials_screening.Model
: Parent of the object.

#### update_inventory_records()

Sets inventory quantities, based on database item asigned to the product/process
: and the product/process quantity.
  If no database entry is asigned, impacts are not updated.

* **Raises:**
  [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) -- Incompatible units of Master object and database entry.

#### remove_inventory_records_from_model(stage=None)

Remove all inventory records from the product/process.

* **Parameters:**
  **stage** ( *{'A1'* *,*  *'A2'* *,*  *'A3'}*) -- Life cycle stage of the product/process. If None, all stages are checked to find the product/process.

#### add_inventory_records_to_model()

Add all inventory records to the product/process, if it is not already in the model.

### *class* pod_lca.materials_screening.Product

Bases: [`Master`](#pod_lca.materials_screening.Master)

Product object, inheriting from the Master object, represent a product.

#### production_year

The year the product was produced.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### electricity

Dictionary containing A3 electricity impacts of the production of the material. Keys as follows;

- 'from_database': contains unit electricity impacts retrieved from the database;
- 'by_location': contains corresponding electricity impacts by location, retrieved from electricity sub-package.
- '_current': indicates which of the above is in use for impacts.
- '_tag': prefix used in the database to identify grouped impacts of electricity.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### weight

Mass of the product.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### weight_unit

Unit of measurement of mass.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### density

The mass of product in weight units per unit of product's unit of measurement. Default is 1.0.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### sctg_code

Standard Classification of Transported Goods (SCTG) code.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### transport_legs

Transportation leg corresponding to the product.

* **Type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of *TransportLeg*

#### mineral_carbonation_potential

Mineral carbonation potential of the product.

* **Type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### is_material

True, if the product is a material.

* **Type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### is_fuel

True, of the product is an energy source.

* **Type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### set_qty(qty)

Update the qty of the product.

* **Parameters:**
  **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Product quantity.

#### set_unit(unit)

Set unit of measurement for the product.
: If the unit of measurement is of mass dimensions, same unit is set as weight unit of the product.

* **Parameters:**
  **unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of measurement.

#### set_production_year(year)

Set the year of production for the item.

* **Parameters:**
  **year** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Year of production.

#### set_density_unit(unit)

Set unit of measurement for the mass of the product.

* **Parameters:**
  **unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of measurement. of mass.

#### set_density(density=None, density_unit=<pod_lca.units.units.Unit object>)

Set density of the product.
: Density is defined here as mass per unit measurement of product (not necessarily volume)

* **Parameters:**
  * **density** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Denisty of product (mass per unit mesurement of product).
  * **density_unit** (*unit*) -- Unit of measurement of density.
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Density must be a numerical value.

#### set_transportation(travel_dist=None, dist_unit=None, transport_scenario=None, return_trip_factor=None, mode_name=None, mode_efficiency=None)

Set transport processes the product is subject to.

* **Parameters:**
  * **travel_dist** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Transportation distance for goods
  * **dist_unit** (*Unit Obj*) -- Unit of measurement of distances.
  * **transportation_scenario** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Transportation scenario considered.
  * **return_trip_factor** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Return trip factor.
  * **mode_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the transportation mode..
  * **mode_efficiency** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Efficiency of the transportation mode.

#### set_electricity_source(source='from_database')

Set the source of electricity inventories.

* **Parameters:**
  **source** ( *{'from_database'* *,*  *'by_location'}*) -- Source of electricity inventories data. Default 'from_database'.

#### set_electricity_database_tag()

Find the tag used to identify electricity data in the database.

#### set_mineral_carbonation_potential(potential)

Set mineral carbonation potential of the product.

* **Parameters:**
  **potential** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- Mineral carbonation potential of the product.

#### set_mineral_carbon_intensity(qty, unit=<pod_lca.units.units.Unit object>, per=None)

Set accelerated carbonation uptake to the 'Mineral C' entry.

* **Parameters:**
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Quantity of accelerated carbonation uptake.
  * **unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of accelerated carbonation uptake.
  * **per** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *or* [*Unit*](units-object.md#pod_lca.units.Unit)) -- Parent quantity for which the mineral carbon intensity is declared.
    If dict, {'per': {'qty': ([`int`](https://docs.python.org/3/library/functions.html#int) or [`float`](https://docs.python.org/3/library/functions.html#float)), 'unit': ([`Unit`](units-object.md#pod_lca.units.Unit))}}
    If Unit object only, the quantity is taken as 1.0;
    If None, taken as per unit of parent objects declared unit.

#### set_sctg_code(code=None)

Set the Standard Classification of Transported Goods (SCTG) code for the material.

* **Parameters:**
  **code** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Standard Classification of Transported Goods (SCTG) code of the material

#### get_production_year()

Get the year of production for the item.

* **Returns:**
  **year** -- Year of production.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_electricity()

Get the electricity product of the item.

* **Returns:**
  Electricity used in the production of the item.
* **Return type:**
  *Electricity*

#### get_electricity_source()

Get the source of electricity inventories.

* **Returns:**
  Source of electricity inventories data.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_electricity_database_tag()

Find the tag used to identify electricity data in the database.

* **Returns:**
  Tag used to identify electricity data in the database.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_electricity_qty()

Get electricity quantity used for the production of product quantity.

* **Returns:**
  Quantity of the electricity
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_weight()

Retrieve the mass of the product.

* **Returns:**
  Mass of the product.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int) or [float](https://docs.python.org/3/library/functions.html#float)

#### get_weight_unit()

Retrieve the unit of measurement of mass of the product.
: This is used for the definition of density of the product.

* **Returns:**
  Unit of measurement of mass of the product.
* **Return type:**
  [*Unit*](units-object.md#pod_lca.units.Unit)

#### get_density()

Retrieve density of the product.
: Density is defined here as mass per unit measurement of product (not necessarily volume)

* **Returns:**
  Denisty of product (mass per unit mesurement of product).
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_density_unit()

Retrieve density unit of the product.

* **Returns:**
  Unit of measurement of the denisty of product.
* **Return type:**
  [*Unit*](units-object.md#pod_lca.units.Unit)

#### get_transportation_manager()

Get the transportation manager corresponding to the product.

* **Returns:**
  Transportation manager
* **Return type:**
  [*TransportationManager*](project-logistics-manager.md#pod_lca.transportation.TransportationManager)

#### get_transportation()

Retrieve transport processes the product is subject to, if any.

* **Returns:**
  Transportation legs the product is subject to.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*TransportationLeg*](logistics-leg.md#pod_lca.transportation.TransportationLeg)

#### get_mineral_carbonation_potential()

Set mineral carbonation potential of the product.

* **Returns:**
  Mineral carbonation potential of the product.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### get_sctg_code(digits=2)

Get the Standard Classification of Transported Goods (SCTG) code for the material.

* **Parameters:**
  **digits** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Significant digits of the Standard Classification of Transported Goods (SCTG) code of the material
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- SCTG code length shorter that digits requested.

#### get_eol_manager()

Return the place where end-of-life transport dataset reside.

* **Returns:**
  End-of-life transport data for materials screening project is at project level.
* **Return type:**
  [*Project*](project.md#pod_lca.materials_screening.Project)

#### update_inventory_records()

Set inventory quantities, based on database item asigned to the product/process and the product/process quantity. If no database entry is asigned, impacts are not updated.

* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Mineral carbonation potential not recognized.

#### update_electricity_records()

Set electricity objects from database and location. This is done only if the database seperates electricity data (i.e., quantity, unit, and inventories). The electricity data in the database should be prefixed with one of **'Electricity_'**, **'electricity_'**, **'elec_'**, or **'Elec_'**.

* **Raises:**
  [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- Inventory type not recognized.

### *class* pod_lca.materials_screening.Electricity

Bases: [`Master`](#pod_lca.materials_screening.Master)

Electricity product object, inheriting from the Fuel object.

#### electricity_supplier

Electricity supplier

* **Type:**
  [*ElectricitySupply*](electricity-supply.md#pod_lca.electricity.ElectricitySupply)

#### year

Year of electricity consumption

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### geographical_scope

Geographical scope considered for electricity data.

* **Type:**
  {'National'. 'Regional', 'Local'}

#### scenario

Cambium scenario for prediction of electricity technology futures.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### *classmethod* new(id, name, model, stage, qty, unit, year=None)

Create a new electricity product in a model.

* **Parameters:**
  * **id** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- An identification number.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the item.
  * **model** ([*Model*](model.md#pod_lca.materials_screening.Model)) -- Model in which the item is created.
  * **stage** ( *{'A1'* *,*  *'A3'}*) -- LCA stage.
    - 'A1': Raw materials supply.
    - 'A3': manufacturing.
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Quantity of the item
  * **unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit corresponding to the quantity.

#### *classmethod* from_unit_inventories(name, qty, unit, impacts, emissions, carbon_storage)

Create an electricity impact from given impacts. This is primarily for seperating electricity component of products.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the electricity.
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Quantity of elctricity consumption.
  * **unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of electricity consumption.
  * **impacts** ([*Impacts*](inventory-records.md#pod_lca.impacts.Impacts)) -- Impacts corresponding to electricity consumption.
  * **emissions** ([*Emissions*](inventory-records.md#pod_lca.impacts.Emissions)) -- Emissions corresponding to electricity consumption.
  * **carbon_storage** ([*CarbonStorage*](inventory-records.md#pod_lca.impacts.CarbonStorage)) -- Carbon storage corresponding to electricity consumption.

#### set_impact_database_entry(database_item: [str](https://docs.python.org/3/library/stdtypes.html#str))

Electricity does not directly read from database.

#### set_supplier(supplier)

Set electricity supplier.

* **Parameters:**
  **supplier** ([*ElectricitySupply*](electricity-supply.md#pod_lca.electricity.ElectricitySupply)) -- Electricity supply

#### set_year(year)

Set the year of electricity consumption.

* **Parameters:**
  **year** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Year of electricity consumption.

#### set_geographical_scope(geographical_scope)

Set the spatial resolution of the electricity supply.

* **Parameters:**
  **geographical_scope** ( *{'National'* *,*  *'Regional'* *,*  *'Local'}*) -- Geographical scope of the electricity supply.

#### set_scenario(scenario)

Set scenario name. This will be used with cambium data.

* **Parameters:**
  **scenario** ( *{'MidCase'* *,*  *'LowRECost'* *,*  *'HighRECost'* *,*  *'HighDemandGrowth'* *,*  *'LowNGPrice'* *,*  *'HighNGPrice'* *,*  *'Decarb95by2050'* *,*  *'Decarb100by2035'}*) -- Electricity consmuption scenario considered.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Scenario is not recognized.

#### get_impact_database_entry()

Electricity does not directly read from database.

#### get_supplier()

Get the electricity supplier.

* **Returns:**
  Electricity supplier.
* **Return type:**
  [*ElectricitySupply*](electricity-supply.md#pod_lca.electricity.ElectricitySupply)

#### get_year()

Get the year of electricity consumption.

* **Returns:**
  Year of electricity consumption.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_geographical_scope()

Get the spatial resolution of the electricity supply.

* **Parameters:**
  **str** -- Spatial resolution of the electricity supply: 'National', 'Regional', 'Local'.

#### get_scenario()

Get scenario name. This will what used with cambium data.

* **Parameters:**
  **str** -- Electricity consmuption scenario considered: e.g., 'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'.

#### get_data_distribution(attr)

Get data_distribution object corresponding to the given attribute.

* **Parameters:**
  **attr** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Attribute to which the distribution correspond.
* **Returns:**
  Data distribution.
* **Return type:**
  *DataDistribution*

#### update_inventory_records()

Sets impacts quantities, based on database item asigned to the product/process and the product/process quantity. If no database entry is asigned, impacts are not updated.

### *class* pod_lca.materials_screening.Fuel

Bases: [`Product`](#pod_lca.materials_screening.Product)

Fuel product.

#### is_material

True

* **Type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### is_energy

True

* **Type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

### *class* pod_lca.materials_screening.Process

Bases: [`Master`](#pod_lca.materials_screening.Master)

A process taking products as input.

#### inputs

Input products and processes.

* **Type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Product*](#pod_lca.materials_screening.Product)
