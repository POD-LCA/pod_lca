# Impacts Database

Impact databases manages importing ([`set_data()`](#pod_lca.impacts.ImpactsDatabase.set_data)) and retrieval ([`get_data_entry()`](#pod_lca.impacts.ImpactsDatabase.get_data_entry)) of LCA data.

Specialized databases, [`ElectricityImpactsDatabase`](#pod_lca.impacts.ElectricityImpactsDatabase), [`EOLImpactsDatabase`](#pod_lca.impacts.EOLImpactsDatabase), and [`TranportationModeImpactsDatabase`](#pod_lca.impacts.TranportationModeImpactsDatabase), are inherited from the base class [`ImpactsDatabase`](#pod_lca.impacts.ImpactsDatabase) to account for additional classifiers present in those databases (e.g., region and technology type used in ElectricityImpactsDatabase).

---

### *class* pod_lca.impacts.ImpactsDatabase

Database manager maintains the impact database.

#### name

Name of the database.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### primary_key

Primary key organizing the database.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### unit_key

Data header corresponding to the units of the database entries.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### qty_key

Data header corresponding to the quantity of the database entries.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### data

Impact data, with following headings;
- **primary_key** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): Name of the impact.
- **qty_key** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): Impacts per unit of measure.
- **unit_key** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): The unit of measure.
- **impact category** ([`float`](https://docs.python.org/3/library/functions.html#float)): Quantity of impact.

* **Type:**
  [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)

#### *classmethod* new(name)

Create a new database.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the database.
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the impact categories json file.
* **Returns:**
  Database created.
* **Return type:**
  [*ImpactsDatabase*](#pod_lca.impacts.ImpactsDatabase)

#### set_name(name)

Set the name of the database.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the database.

#### set_data(file_path, \*\*kwargs)

Set the database data.

* **Parameters:**
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the CSV file.
  * **impact_headers_map** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- The headers of the CSV file as they would be mapped to the impacts in the database: {**header** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **impact category** ([`str`](https://docs.python.org/3/library/stdtypes.html#str))}.
  * **emission_headers_map** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- The headers of the CSV file as they would be mapped to the emission inventories in the database: {**header** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **inventory** ([`str`](https://docs.python.org/3/library/stdtypes.html#str))}.
  * **carbon_storage_headers_map** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- The headers of the CSV file as they would be mapped to the carbon storage in the database: {**header** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **carbon storage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str))}.
  * **grouped_data** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Prefix used in the grouped data.
  * **additional_headers** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Headers of the columns to be imported, other than name, unit, and impact categories.
  * **multipliers** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Values of each column of the CSV will be multiplied by these values, in the order given in impact headers first and then additional headers.
* **Raises:**
  [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- Category not recognized.

#### set_data_entry(flow, qty, unit, \*\*kwargs)

Add a custom entry the database.

* **Parameters:**
  * **flow** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the impact.
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Quantity of the flow.
  * **unit** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Unit of measurement for which the impacts are applied.
  * **impacts** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- Dictionary of impacts {**impact catergory** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **impact** ([`float`](https://docs.python.org/3/library/functions.html#float))}.
  * **emissions** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- Dictionary of emissions {**emission inventory** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **emission** ([`float`](https://docs.python.org/3/library/functions.html#float))}.
  * **carbon_storage** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- Dictionary of carbon storage {**carbon storage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **carbon quantity** ([`float`](https://docs.python.org/3/library/functions.html#float))}.
  * **additional_data** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- Dictionary of additional data {**header** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **value** ([`str`](https://docs.python.org/3/library/stdtypes.html#str) / [`float`](https://docs.python.org/3/library/functions.html#float)/ [`int`](https://docs.python.org/3/library/functions.html#int))}.
* **Raises:**
  [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- Category not recognized.

#### set_primary_key(key)

Set primary key of the database.

* **Parameters:**
  **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Primary key organizing the database.

#### set_unit_key(key)

Set unit key of the database.

* **Parameters:**
  **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Data header corresponding to the units of the database entries.

#### set_qty_key(key)

Set quantity key of the database.

* **Parameters:**
  **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Data header corresponding to the quantity of the database entries.

#### get_name()

Get the name of the database.

* **Returns:**
  Name of the database.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_impact_category_units()

Get the units of the impact categories.

* **Returns:**
  List of units of the impact categories.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_data_all()

Retrieve impact data in the database.

* **Returns:**
  Impact data.
* **Return type:**
  [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)

#### get_data_entry(flow_name)

Retrieve impacts for given flow.

* **Parameters:**
  **flow_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the flow
* **Returns:**
  Databse entry corresponding to the flow.
* **Return type:**
  [pandas.Series](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series)
* **Raises:**
  [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) -- Multiple matching entries.

#### get_primary_key()

Get primary key of the database.

* **Returns:**
  Primary key organizing the database.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_unit_key()

Get unit key of the database.

* **Returns:**
  Data header corresponding to the units of the database entries.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_qty_key()

Get quantity key of the database.

* **Returns:**
  Data header corresponding to the quantity of the database entries.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_required_headers()

Get the required headers of the database.

* **Returns:**
  Headers of the columns to be imported, other than name, unit, and impact categories.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [str](https://docs.python.org/3/library/stdtypes.html#str)

### *class* pod_lca.impacts.ElectricityImpactsDatabase

Bases: [`ImpactsDatabase`](#pod_lca.impacts.ImpactsDatabase)

Database manager to handle electricity impacts.

#### process_key

Data header corresponding to the end-of-life process corresponding to the database entry.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### life_cycle_stage_key

Data header corresponding to the life cycle stage corresponding to the database entry.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### *classmethod* new(name, geographical_scope=None)

Create a new database.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the database.
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the impact categories json file.
  * **geographical_scope** ( *{'National'* *,*  *'Regional'* *,*  *'Local'}*) -- Geographical scope of the database.
* **Returns:**
  Database created.
* **Return type:**
  [*ElectricityImpactsDatabase*](#pod_lca.impacts.ElectricityImpactsDatabase)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- If geographical scope is not one of the options given.

#### set_region_key(key)

Set region key of the database.

* **Parameters:**
  **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Data header corresponding to the end-of-life process corresponding to the database entry.

#### set_technology_key(key)

Set technology key of the database.

* **Parameters:**
  **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Data header corresponding to the end-of-life process corresponding to the database entry.

#### get_region_key()

Get region key of the database.

* **Returns:**
  Data header corresponding to the end-of-life process corresponding to the database entry.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_technology_key()

Get technology key of the database.

* **Returns:**
  Data header corresponding to the end-of-life process corresponding to the database entry.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_required_headers()

Get the required headers of the database.

* **Returns:**
  Headers of the database.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_data_entry(region, technology)

Retrieve impacts for given flow.

* **Parameters:**
  * **region** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Electricity generation region, as appropriate to the regionality used.
  * **technology** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Electricity generation technology.
* **Returns:**
  Databse entry corresponding to the flow.
* **Return type:**
  [pandas.Series](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series)

### *class* pod_lca.impacts.EOLImpactsDatabase

Bases: [`ImpactsDatabase`](#pod_lca.impacts.ImpactsDatabase)

Database manager to handle End-of-Life impacts.

#### process_key

Data header corresponding to the end-of-life pathway corresponding to the database entry.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### life_cycle_stage_key

Data header corresponding to the life cycle stage corresponding to the database entry.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### *classmethod* new(name)

Create a new database.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the database.
* **Returns:**
  Database created.
* **Return type:**
  [*EOLImpactsDatabase*](#pod_lca.impacts.EOLImpactsDatabase)

#### set_process_key(key)

Set process key of the database.

* **Parameters:**
  **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Data header corresponding to the end-of-life pathway corresponding to the database entry.

#### set_life_cycle_stage_key(key)

Set life cycle stage key of the database.

* **Parameters:**
  **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Data header corresponding to the life cycle stage corresponding to the database entry.

#### get_process_key()

Get process key of the database.

* **Returns:**
  Data header corresponding to the end-of-life process corresponding to the database entry.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_life_cycle_stage_key()

Get life cycle stage key of the database.

* **Returns:**
  Data header corresponding to the life cycle stage corresponding to the database entry.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_required_headers()

Get the required headers of the database.

* **Returns:**
  Database headers.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_data_entry(material_name, process_name, life_cycle_stage)

Retrieve impacts for given flow.

* **Parameters:**
  * **material_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the material
  * **process_name** ( *{'Landfill'* *,*  *'Recycle'* *,*  *'Compost'* *,*  *'Incinerate'}*) -- 

    End-of-life pathway:
    - 'Landfill': transporting waste to a landfill.
    - 'Recycle': transporting waste to a recycler.
    - 'Compost': transporting to a composting facility.
    - 'Incinerate': transporting to an incinerator.
  * **life_cycle_stage** ( *{'C3'* *,*  *'C4'* *,*  *'D'}*) -- 

    Life cycle stage.
    - 'C3': waste processing
    - 'C4': disposal
    - 'D': reuse
* **Returns:**
  Databse entry corresponding to the flow.
* **Return type:**
  [pandas.Series](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series)
* **Raises:**
  [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) -- Data not in database or multiple matching entries.

### *class* pod_lca.impacts.TranportationModeImpactsDatabase

Bases: [`ImpactsDatabase`](#pod_lca.impacts.ImpactsDatabase)

Database manager to handle End-of-Life impacts.

#### fuel_type_key

Data header corresponding to the fuel type corresponding to the database entry.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### mode_efficiency_key

Data header corresponding to the mode efficiency corresponding to the database entry.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### *classmethod* new(name)

Create a new database.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the database.
* **Returns:**
  Database created.
* **Return type:**
  [*ImpactsDatabase*](#pod_lca.impacts.ImpactsDatabase)

#### set_mode_efficiency_key(key)

Set the mode efficiency key of the database.

* **Parameters:**
  **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Data header corresponding to the mode efficiency corresponding to the database entry.

#### get_mode_efficiency_key()

Get the mode efficiency key of the database.

* **Returns:**
  Data header corresponding to the mode efficiency corresponding to the database entry.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_required_headers()

Get the required headers of the database.

* **Returns:**
  Database headers.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_data_entry(mode)

Retrieve impacts for given flow.

* **Parameters:**
  **mode** ([*TransportMode*](transport_mode.md#pod_lca.transportation.TransportMode)) -- Transport mode with its name, fuel type, and efficiency.
* **Returns:**
  Databse entry corresponding to the flow.
* **Return type:**
  [pandas.Series](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series)
