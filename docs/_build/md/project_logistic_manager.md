# Project Logistics Manager

[`TransportationManager`](#pod_lca.transportation.TransportationManager) class provides a means of managing a transportation operation. [`USDomesticTransportationManager`](#pod_lca.transportation.USDomesticTransportationManager) and [`USGlobalTransportationManager`](#pod_lca.transportation.USGlobalTransportationManager) are specific classes for the US domestic and Gloabl-to-US transportation.

---

### *class* pod_lca.transportation.TransportationManager

This class maintains the legs of transportation for products transported.

#### name

name of the project.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### transport_legs

Dictionary mapping products to their corresponding transportation legs: {**product** ([`Product`](products.md#pod_lca.materials_screening.Product)) : **transport leg** ([`TransportationLeg`](logistics_link.md#pod_lca.transportation.TransportationLeg))}.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### mode_impact_database

Database containing unit impacts for transportation modes.

* **Type:**
  [*TranportationModeImpactsDatabase*](impact_databases.md#pod_lca.impacts.TranportationModeImpactsDatabase)

#### *classmethod* new(name=None)

Create a new project.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the project.
* **Returns:**
  Project created.
* **Return type:**
  [*TransportationManager*](#pod_lca.transportation.TransportationManager)

#### set_name(name: [str](https://docs.python.org/3/library/stdtypes.html#str))

Set the name of the project.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the project.

#### set_impact_database(database)

Set mode impact database used in the project.

* **Parameters:**
  **database** ([*TranportationModeImpactsDatabase*](impact_databases.md#pod_lca.impacts.TranportationModeImpactsDatabase) *or* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Impact database object or if a string, filepath to the corresponding csv file containing impact data.
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Database input not recognized

#### set_project_origin(origin: [str](https://docs.python.org/3/library/stdtypes.html#str))

Set the origin location of the project.

* **Parameters:**
  **origin** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Origin location of the project.

#### set_project_destination(destination: [str](https://docs.python.org/3/library/stdtypes.html#str))

Set the destination location of the project.

* **Parameters:**
  **destination** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Destination location of the project.

#### get_name()

Retrieve the name of the project.

* **Returns:**
  Name of the project.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_transportation_legs()

Retrieve the transportation legs of the project.

* **Returns:**
  List of transportation legs.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*TransportationLeg*](logistics_link.md#pod_lca.transportation.TransportationLeg)

#### get_transportation_leg(product)

Retrieve the transportation legs corresponding to a product.

* **Parameters:**
  **product** ([*Product*](products.md#pod_lca.materials_screening.Product)) -- Object for which the transportation leg correspond to.
* **Returns:**
  Transportation leg.
* **Return type:**
  [*TransportationLeg*](logistics_link.md#pod_lca.transportation.TransportationLeg)

#### get_goods()

Retrieve the goods of the project.

* **Returns:**
  List of goods.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Product*](products.md#pod_lca.materials_screening.Product)

#### get_impact_database()

Retrieve the transportation mode impact database.

* **Returns:**
  Transportation mode impact database.
* **Return type:**
  [*TranportationModeImpactsDatabase*](impact_databases.md#pod_lca.impacts.TranportationModeImpactsDatabase)

#### get_impacts(product=None)

Retrieve the impacts of the project.

* **Parameters:**
  **product** ([*Product*](products.md#pod_lca.materials_screening.Product)) -- Product for which the transportation impacts rquested
* **Returns:**
  Impacts of the project.
* **Return type:**
  [*Impacts*](impact_records.md#pod_lca.impacts.Impacts)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Product not found in the project.

#### get_emissions(product=None)

Retrieve the emissions of the product.

* **Parameters:**
  **product** ([*Product*](products.md#pod_lca.materials_screening.Product)) -- Product for which the transportation impacts rquested
* **Returns:**
  Emissions of the product/process.
* **Return type:**
  [*Emissions*](impact_records.md#pod_lca.impacts.Emissions)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Product not found in the project.

#### add_good(good, travel_dist=None, shipping_dest=None, shipping_org=None, transport_scenario=None, distance_unit=<pod_lca.units.units.Unit object>, return_trip_factor=None, mode_name=None, mode_fuel_type='Regular', mode_efficiency='Median')

Add goods to the project. This method creates the appropriate transportation legs based on the data provided

* **Parameters:**
  * **good** ([*Product*](products.md#pod_lca.materials_screening.Product)) -- Goods to be transported.
  * **travel_dist** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Transportation distance for goods
  * **shipping_dest** ([*Location*](location_module.md#pod_lca.location.Location)) -- Shipping destination.
  * **shipping_org** ([*Location*](location_module.md#pod_lca.location.Location)) -- Shipping origin
  * **transportation_scenario** ( *{'Local'* *,*  *'Regional'* *,*  *'Regional_c'* *,*  *'National'* *,*  *'Global'}*) -- Transportation scenario considered.
  * **distance_unit** ([*Unit*](units.md#pod_lca.units.Unit)) -- Unit of measurement of distances.
  * **return_trip_factor** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Return trip factor.
  * **mode_name** ( *{'Truck'* *,*  *'E_Truck'* *,*  *'Rail'* *,*  *'Barge'* *,*  *'Ocean'* *,*  *'Air'}*) -- Name of the transportation mode.
  * **mode_efficiency** ( *{'High'* *,*  *'Median'* *,*  *'Low'}*) -- Efficiency of the transportation mode.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Transport scenario not recognized.

#### clear_project()

Clear the project by removing all transportation legs.

#### save(file_path: [str](https://docs.python.org/3/library/stdtypes.html#str))

Save as a 

```
*
```

.pkl file.

* **Parameters:**
  **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location (including the name) where the data be saved.

#### *static* load(file_path: [str](https://docs.python.org/3/library/stdtypes.html#str))

Load a project from a pickled file.

* **Parameters:**
  **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location (including the name) where the data be loaded from.
* **Raises:**
  * [**FileNotFoundError**](https://docs.python.org/3/library/exceptions.html#FileNotFoundError) -- File not found.
  * [**PermissionError**](https://docs.python.org/3/library/exceptions.html#PermissionError) -- Permission denied to access file.

### *class* pod_lca.transportation.USDomesticTransportationManager

Bases: [`TransportationManager`](#pod_lca.transportation.TransportationManager)

A project in US using domestic logistic.

#### dataset

Dataset corresponding to the project.

* **Type:**
  [*TransportDataset*](transport_datasets.md#pod_lca.transportation.TransportDataset)

#### *classmethod* new(name=None)

Create a new project.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the project.
* **Returns:**
  Project created.
* **Return type:**
  [*TransportationManager*](#pod_lca.transportation.TransportationManager)

#### set_dataset(dataset)

Set background dataset for the proect.

* **Parameters:**
  **dataset** ([*TransportDataset*](transport_datasets.md#pod_lca.transportation.TransportDataset)) -- Dataset corresponding to the project

#### get_dataset(name=None)

Return the dataset corresponding to the project.

* **Returns:**
  Dataset corresponding to the project.
* **Return type:**
  [*TransportDataset*](transport_datasets.md#pod_lca.transportation.TransportDataset)

#### add_good(good, travel_dist=None, shipping_dest=None, shipping_org=None, transport_scenario=None, distance_unit=<pod_lca.units.units.Unit object>, return_trip_factor=None, mode_name=None, mode_efficiency='Median')

Add goods to the project. This method creates the appropriate transportation legs based on the data provided

* **Parameters:**
  * **good** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*Product*](products.md#pod_lca.materials_screening.Product)) -- Good to be transported.
  * **travel_dist** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Transportation distance for goods
  * **shipping_dest** ([*Location*](location_module.md#pod_lca.location.Location)) -- Shipping destination.
  * **shipping_org** ([*Location*](location_module.md#pod_lca.location.Location)) -- Shipping origin
  * **transport_scenario** ( *{'Local'* *,*  *'Regional'* *,*  *'Regional_c'* *,*  *'National'}*) -- Transportation scenario considered.
  * **distance_unit** ([*Unit*](units.md#pod_lca.units.Unit)) -- Unit of measurement of distances.
  * **return_trip_factor** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Return trip factor.
  * **mode_name** ( *{'Truck'* *,*  *'E_Truck'* *,*  *'Rail'* *,*  *'Barge'}*) -- Name of the transportation mode.
  * **mode_efficiency** ( *{'High'* *,*  *'Median'* *,*  *'Low'}*) -- Efficiency of the transportation mode. Default is 'Median'
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Transport scenario not recognized.

### *class* pod_lca.transportation.USGlobalTransportationManager

Bases: [`TransportationManager`](#pod_lca.transportation.TransportationManager)

A project in US using global logistic.

#### dataset

Dataset corresponding to the project.

* **Type:**
  [*TransportDataset*](transport_datasets.md#pod_lca.transportation.TransportDataset)

#### *classmethod* new(name=None)

Create a new project.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the project.
* **Returns:**
  Project created.
* **Return type:**
  [*TransportationManager*](#pod_lca.transportation.TransportationManager)

#### set_dataset(dataset)

Set background dataset for the proect.

* **Parameters:**
  **dataset** ([*TransportDataset*](transport_datasets.md#pod_lca.transportation.TransportDataset)) -- Dataset corresponding to the project.

#### get_dataset(name=None)

Return the dataset corresponding to the project.

* **Returns:**
  Dataset corresponding to the project.
* **Return type:**
  [*TransportDataset*](transport_datasets.md#pod_lca.transportation.TransportDataset)

#### add_good(good, travel_dist=None, shipping_dest=None, shipping_org=None, transport_scenario=None, distance_unit=<pod_lca.units.units.Unit object>, return_trip_factor=None, mode_name=None, mode_efficiency='Median')

Add good to the project. This method creates the appropriate tranportation leg based on the data provided

* **Parameters:**
  * **good** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*Product*](products.md#pod_lca.materials_screening.Product)) -- Good to be transported.
  * **travel_dist** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Transportation distance for goods.
  * **shipping_dest** ([*Location*](location_module.md#pod_lca.location.Location)) -- Shipping destination.
  * **shipping_org** ([*Location*](location_module.md#pod_lca.location.Location)) -- Shipping origin
  * **transport_scenario** ( *{'Global'}*) -- Transportation scenario considered.
  * **distance_unit** ([*Unit*](units.md#pod_lca.units.Unit)) -- Unit of measurement of distances.
  * **return_trip_factor** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Return trip factor.
  * **mode_name** ( *{'Truck'* *,*  *'E_Truck'* *,*  *'Rail'* *,*  *'Ocean'* *,*  *'Air'}*) -- Name of the transportation mode.
  * **mode_efficiency** ( *{'High'* *,*  *'Median'* *,*  *'Low'}*) -- Efficiency of the transportation mode. Default is 'Median'.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Transport scenario not recognized.
