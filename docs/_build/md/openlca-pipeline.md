# OpenLCA Pipeline

This provides a link to the [OpenLCA](https://www.openlca.org/) application.

---

### *class* pod_lca.impacts.openLCA

#### set_connection()

Connect to the openLCA server.

* **Returns:**
  The client object for the openLCA server.
* **Return type:**
  olca_ipc.Client
* **Raises:**
  [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) -- olca-ipc package not installed.

#### create_product_system(process)

Set the product system for the process.

* **Parameters:**
  * **client** (*olca_ipc.Client*) -- The client object for the openLCA server.
  * **process** (*Schema.Process* *or* *schema.Ref*) -- Process object or reference to the process object.
* **Returns:**
  Reference to the product system object.
* **Return type:**
  schema.Ref
* **Raises:**
  [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) -- olca-ipc package not installed.

#### get_impact_method(impact_method_uuid)

Get the impact method from the openLCA server.

* **Parameters:**
  **client** (*olca_ipc.Client*) -- The client object for the openLCA server.
* **Returns:**
  The impact method object.
* **Return type:**
  schema.ImpactMethod
* **Raises:**
  [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) -- olca-ipc package not installed.

#### get_process_list(uuids=None)

Get the list of processes from the openLCA server.

* **Parameters:**
  * **client** (*olca_ipc.Client*) -- The client object for the openLCA server.
  * **uuids** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- List of UUIDs of the processes to be filtered. If None, all processes are returned.
* **Returns:**
  List of processes reference objects from the openLCA server.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)
* **Raises:**
  * [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) -- olca-ipc package not installed.
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Invalid uuid.

#### get_impacts(result, impact_dict)

Get the impact results of the product system.

* **Parameters:**
  * **client** (*olca_ipc.Client*) -- The client object for the openLCA server.
  * **result** (*olca_ipc.Result*) -- The result of the calculation.
  * **impact_dict** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- Dictionary of impact categories.
* **Returns:**
  Dictionary of impact results.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)
* **Raises:**
  [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) -- olca-ipc package not installed.

#### get_category_in_process(node, level, impact, qty, unit, conversion_map, max_levels=3)

This function recursively expands an upstream tree.
: The maximum number of levels and maximum number of child nodes are defined with the constants above.

* **Parameters:**
  * **categories** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *or* [*int*](https://docs.python.org/3/library/functions.html#int)) -- IDs of categories to be identified.
    Category IDs from the North American Industry Classification System (NAICS) or International Standard Industrial Classification (ISIC).
  * **node** (*utree.Node*) -- The node object.
  * **level** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- The level of the node in the tree.
  * **impact** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- The impact from the category.
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- The declared quantity of the category.
  * **unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- The declared unit of the category.
  * **max_levels** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- The maximum number of levels to expand the tree.
* **Returns:**
  * [`float`](https://docs.python.org/3/library/functions.html#float) -- The electricity impact.
  * [`float`](https://docs.python.org/3/library/functions.html#float) -- The electricity required sum.
  *  *~pod_lca.units.Unit* -- The declared unit of the category.
* **Raises:**
  [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) -- olca-ipc package not installed.

#### get_process_in_process(node, level, impact, qty, unit, conversion_map, max_levels=3)

This function recursively expands an upstream tree.
: The maximum number of levels and maximum number of child nodes are defined with the constants above.

* **Parameters:**
  * **processes** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *or* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- UUIDs of processess to be identified.
  * **node** (*utree.Node*) -- The node object.
  * **level** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- The level of the node in the tree.
  * **impact** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- The impact from the category.
  * **qty** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- The declared quantity of the category.
  * **unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- The declared unit of the category.
  * **max_levels** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- The maximum number of levels to expand the tree.
  * **conversion_map** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- A mapping for conversion of declared units of a given set of processes (e.g., fuel group unit conversion to energy units)
    {**uuid** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): {**'name'** : name of the process ([`str`](https://docs.python.org/3/library/stdtypes.html#str)),
    **'declared_qty'**: declared quantity of the process ([`str`](https://docs.python.org/3/library/stdtypes.html#str) or [`float`](https://docs.python.org/3/library/functions.html#float)),
    **'declared_unit'**: standard notation of the declared units of the process ([`str`](https://docs.python.org/3/library/stdtypes.html#str)),
    **'conversion_factor'**: conversion factor ([`str`](https://docs.python.org/3/library/stdtypes.html#str) or [`float`](https://docs.python.org/3/library/functions.html#float)),
    **'converted_unit'**: standard notation of the unit to which the process quantity is converted ([`str`](https://docs.python.org/3/library/stdtypes.html#str))}}
* **Returns:**
  * [`float`](https://docs.python.org/3/library/functions.html#float) -- The electricity impact.
  * [`float`](https://docs.python.org/3/library/functions.html#float) -- The electricity required sum.
  * [`Unit`](units-object.md#pod_lca.units.Unit) -- The declared unit of the category.
* **Raises:**
  [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) -- olca-ipc package not installed.

#### *static* is_UUID(uuid)

Check if the input is a valid UUID.

* **Parameters:**
  **uuid** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* [*int*](https://docs.python.org/3/library/functions.html#int)) -- The input to be checked.
* **Returns:**
  True if the input is a valid UUID, False otherwise.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### *static* is_NAICS(naics)

Check if the input is a valid North American Industry Classification System (NAICS) code.

* **Parameters:**
  **naics** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- The input integer to be checked.
* **Returns:**
  True if the input is a valid NAICS code, False otherwise.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### *static* is_ISIC(isic)

Check if the input is a valid International Standard Industrial Classification (ISIC) code.

* **Parameters:**
  **isic** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- The input integer to be checked.
* **Returns:**
  True if the input is a valid ISIC code, False otherwise.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### fix_last_internal_ids(process_list)

Finds any processes in process_list for which last_internal_id < len(exchanges), and fixes by setting last_internal_id = len(exchanges).

* **Parameters:**
  * **client** (*olca_ipc.Client*) -- The client object for the openLCA server.
  * **process_list** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of UUIDs of the processess to be tested
* **Returns:**
  The client object for the openLCA server.
* **Return type:**
  olca_ipc.Client

#### *static* filter_processes_by(process_list, filter_by)

Filters the process list by the category given by NAICS or ISIC ids.

* **Parameters:**
  * **process_list** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* *Schema.Process*) -- List of processes.
  * **filter_by** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*int*](https://docs.python.org/3/library/functions.html#int) *, or* [*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*int*](https://docs.python.org/3/library/functions.html#int)) -- NAICS or ISIC ids of Categories to be filter by.
* **Returns:**
  List of processess.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of Schema.Process

#### *static* import_from_zip(client, path, duplicates='overwrite')

Import a database from a zip file. Handle only the first level of nested zip files.

* **Parameters:**
  * **client** (*olca_ipc.Client*) -- The client object for the openLCA server.
  * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- The path to the zip file.
  * **duplicates** ( *{overwrite'* *,*  *'update'* *,*  *'never'}*) -- The action to take if a duplicate item is found. Default is 'overwrite'.

#### *static* import_from_json(client, file_name, data, duplicates)

Import a database item from a json file.

* **Parameters:**
  * **client** (*olca_ipc.Client*) -- The client object for the openLCA server.
  * **file_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- The name of the file.
  * **data** (*ZipExtFile*) -- The data from the file.
  * **duplicates** ( *{'overwrite'* *,*  *'update'* *,*  *'never'}*) -- The action to take if a duplicate item is found.

#### compute_impacts(product_system_ref, impact_method_ref, qty=1.0)

Compute the impacts of the product system.

#### NOTE
1. Allocation method set to 'As Defined in Processes' by default (same as openLCA GUI default). For other allocation method names see [https://greendelta.github.io/olca-schema/enums/AllocationType.html](https://greendelta.github.io/olca-schema/enums/AllocationType.html).
2. The calculation of the impact method does not occur asynchronously, therefore the wait_until_ready() method called after the results object is created.

* **Parameters:**
  * **client** (*olca_ipc.Client*) -- The client object for the openLCA server.
  * **product_system_ref** (*schema.Ref*) -- Reference to the product system object.
  * **impact_method_ref** (*schema.Ref*) -- Reference to the impact method object.
* **Returns:**
  The result of the calculation.
* **Return type:**
  olca_ipc.Result

#### generate_impacts_dir(process_list, impact_dict, impact_method, group_by=None)

Generate the impacts of the processes in the openLCA server.

* **Parameters:**
  * **client** (*olca_ipc.Client*) -- The client object for the openLCA server.
  * **process_list** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of UUIDs of the processess to be tested
  * **impact_dict** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- Dictionary of impact categories.
  * **impact_method** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- UUID of the impact method.
  * **group_by** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *or* [*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- 

    Dictionary of group categorization: {**'name'**
    : **'ids'** : [**category id** ([`int`](https://docs.python.org/3/library/functions.html#int)) or product uuid ([`str`](https://docs.python.org/3/library/stdtypes.html#str))],
      **'unit'**: unit to be reported - optional ([`Unit`](units-object.md#pod_lca.units.Unit)),
      **'conversion_map'**: conversion map - optional ([`dict`](https://docs.python.org/3/library/stdtypes.html#dict))}

    Category IDs are from the North American Industry Classification System (NAICS).
    When unit is not given the default unit of the first item in the group is used.
    Conversion map needs the following keys: **'UUID'**, **'declared_unit'**, **'declared_qty'**, **'conversion_factor'**, **'converted_unit'**.
* **Returns:**
  Dictionary of impact results.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)
* **Raises:**
  * [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) -- olca-ipc package not installed.
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- uuids not recognized.
