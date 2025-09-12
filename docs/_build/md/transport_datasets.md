# Transport Datasets

[`TransportDataset`](#pod_lca.transportation.TransportDataset) class manages datasets which are used by [`TransportationLeg`](logistics_link.md#pod_lca.transportation.TransportationLeg) objects to estimate the traved distances. Transportation datasets and their corresponding transportation datasets are as in the table below.

| Transportation Leg                                                                | Dataset                                                              |
|-----------------------------------------------------------------------------------|----------------------------------------------------------------------|
| [`DomesticLeg`](logistics_link.md#pod_lca.transportation.DomesticLeg)             | [`CFSDataset`](#pod_lca.transportation.CFSDataset)                   |
| [`ForeignLeg`](logistics_link.md#pod_lca.transportation.ForeignLeg)               | [`USGlobalDataset`](#pod_lca.transportation.USGlobalDataset)         |
| [`WasteTransportLeg`](logistics_link.md#pod_lca.transportation.WasteTransportLeg) | [`EOLTransportDataset`](#pod_lca.transportation.EOLTransportDataset) |

---

### *class* pod_lca.transportation.TransportDataset

An abstract class to handle the dataset for transportation legs.

#### filter_datasets(material=None, destination=None, origin=None, mode=None, \*\*kwargs)

Filter the CFS dataset based on the provided parameters.

* **Parameters:**
  * **material** ([*Product*](products.md#pod_lca.materials_screening.Product)) -- Material considered.
  * **destination** ([*Location*](location_module.md#pod_lca.location.Location)) -- The destination location to filter by.
  * **origin** ([*Location*](location_module.md#pod_lca.location.Location)) -- The origin location to filter by.
  * **mode** ([*TransportMode*](transport_mode.md#pod_lca.transportation.TransportMode)) -- The transportation mode to filter by.
* **Returns:**
  The filtered CFS dataset.
* **Return type:**
  [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)

#### *static* get_distance_estimate(dataset, \*\*kwargs)

Get the average distance from the CFS dataset based on the scenario.

* **Parameters:**
  **dataset** ([*pandas.DataFrame*](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)) -- The filtered dataset.
* **Returns:**
  The average distance for the specified scenario.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

### *class* pod_lca.transportation.CFSDataset

Bases: [`TransportDataset`](#pod_lca.transportation.TransportDataset)

A class to handle the CFS dataset for transportation legs.

#### filter_datasets(material=None, destination=None, origin=None, mode=None)

Filter the CFS dataset based on the provided parameters.

* **Parameters:**
  * **material** ([*Product*](products.md#pod_lca.materials_screening.Product)) -- The Standard Classification of Transported Goods (SCTG) code to filter by.
  * **destination** ([*Location*](location_module.md#pod_lca.location.Location)) -- The destination location to filter by.
  * **origin** ([*Location*](location_module.md#pod_lca.location.Location)) -- The origin location to filter by.
  * **mode** ([*TransportMode*](transport_mode.md#pod_lca.transportation.TransportMode)) -- The transportation mode to filter by.
* **Returns:**
  The filtered CFS dataset.
* **Return type:**
  [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- If no data is found for the provided SCTG code or mode.

#### *static* get_distance_estimate(dataset, scenario)

Get the average distance from the CFS dataset based on the scenario.

* **Parameters:**
  * **dataset** ([*pandas.DataFrame*](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)) -- The filtered CFS dataset.
  * **scenario** ( *{'Local'* *,*  *'Regional'. 'Regional_c'* *,*  *'National'* *,*  *'Average'}*) -- The scenario to filter the distances by.
* **Returns:**
  The average distance for the specified scenario.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- If the scenario is not recognized.

### *class* pod_lca.transportation.USGlobalDataset

Bases: [`TransportDataset`](#pod_lca.transportation.TransportDataset)

A class to handle transportation of goods to US from global origins.

#### filter_datasets(material=None, destination=None, origin=None, mode_domestic=None, mode_foreign=None)

Filter all datasets corresponding to foreign travel.

* **Parameters:**
  * **material** ([*Master*](products.md#pod_lca.materials_screening.Master)) -- The Standard Classification of Transported Goods (SCTG) code to filter by.
  * **destination** ([*Location*](location_module.md#pod_lca.location.Location)) -- The destination location to filter by.
  * **origin** ([*Location*](location_module.md#pod_lca.location.Location)) -- The origin location to filter by.
  * **mode_domestic** ([*TransportMode*](transport_mode.md#pod_lca.transportation.TransportMode)) -- The foreign transportation mode to filter by.
  * **mode_foreign** ([*TransportMode*](transport_mode.md#pod_lca.transportation.TransportMode)) -- The domestic transportation mode to filter by.
* **Returns:**
  * [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame) -- The filtered FAF dataset.
  * [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame) -- The filtered marine dataset.
  * [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame) -- The filtered cfaf dataset.

#### filter_faf(sctg=None, destination=None, origin=None, mode_foreign=None, mode_domestic=None)

Filter FAF data.

* **Parameters:**
  * **sctg** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- The Standard Classification of Transported Goods (SCTG) code to filter by.
  * **destination** ([*Location*](location_module.md#pod_lca.location.Location)) -- The destination location to filter by.
  * **origin** ([*Location*](location_module.md#pod_lca.location.Location)) -- The origin location to filter by.
  * **mode_domestic** ([*TransportMode*](transport_mode.md#pod_lca.transportation.TransportMode)) -- The foreign transportation mode to filter by.
  * **mode_foreign** ([*TransportMode*](transport_mode.md#pod_lca.transportation.TransportMode)) -- The domestic transportation mode to filter by.
* **Returns:**
  The filtered FAF dataset.
* **Return type:**
  [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- If no data is found for the provided SCTG code, destination, or mode.

#### filter_cfaf(sctg)

Filter Canadian Freight Analysis Framework (CFAF) dataset by material SCTG code.

* **Parameters:**
  **sctg** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Two-digit SCTG code of the material.
* **Returns:**
  Filtered CFAF dataset.
* **Return type:**
  [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Material not found in cfaf dataset.

#### filter_marine(destination=None, origin=None)

Filter marine data.

* **Parameters:**
  * **destination** ([*Location*](location_module.md#pod_lca.location.Location)) -- Final destination of the product.
  * **origin** ([*Location*](location_module.md#pod_lca.location.Location)) -- Origin of the travel.
  * **scenario** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Transportation scenario considered.
* **Returns:**
  Filtered marine dataset.
* **Return type:**
  [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- No data for the selected origin in marine dataset

#### *static* get_distance_estimate(fltered_datasets, destination, origin, mode_name)

Get the average travel distance based on shipping destination, origin, and mode of transportation.

* **Parameters:**
  * **filtered_datasets** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) -- Filtered datasets as pandas dataframes.
  * **destination** ([*Location*](location_module.md#pod_lca.location.Location)) -- Final destination of the product.
  * **origin** ([*Location*](location_module.md#pod_lca.location.Location)) -- Origin of the travel.
  * **mode_name** ( *{'Truck'* *,*  *'Rail'* *,*  *'Ocean'* *,*  *'Air'}*) -- Transportation mode
* **Returns:**
  * [`float`](https://docs.python.org/3/library/functions.html#float) -- Travel distance of the domestic leg of travel.
  * [`float`](https://docs.python.org/3/library/functions.html#float) -- Travel distance of the foreign leg of travel.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Invalid mode of transportation.

### *class* pod_lca.transportation.EOLTransportDataset

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

A class to handle end-of-life transportation dataset.

#### filter_datasets(origin=None, eol_pathway=None)

Filter the CFS dataset based on the provided parameters.

* **Parameters:**
  * **sctg** ([*int*](https://docs.python.org/3/library/functions.html#int) *,* *optional*) -- The Standard Classification of Transported Goods (SCTG) code to filter by.
  * **origin** ([*Location*](location_module.md#pod_lca.location.Location) *,* *optional*) -- The origin location to filter by.
  * **eol_pathway** ([*TransportMode*](transport_mode.md#pod_lca.transportation.TransportMode) *,* *optional*) -- The transportation mode to filter by.
* **Returns:**
  The filtered dataset.
* **Return type:**
  [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)

#### *static* get_distance_estimate(dataset, scenario)

Get the average distance from the CFS dataset based on the scenario.

* **Parameters:**
  * **dataset** ([*pandas.DataFrame*](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)) -- The filtered dataset.
  * **scenario** ( *{'Min'* *,*  *'Average'* *,*  *'High'}*) -- The scenario to filter the distances by.
* **Returns:**
  The average distance for the specified scenario.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- If the scenario is not recognized or if no data is found for the scenario.
