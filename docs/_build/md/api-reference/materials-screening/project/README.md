# Project

A material screening [`Project`](#pod_lca.materials_screening.Project) maintain the project metadata (e.g., year, [`Location`](location.md#pod_lca.location.Location)), [`ImpactsDatabase`](impacts-database.md#pod_lca.impacts.ImpactsDatabase), and the alternative [`Model`](model.md#pod_lca.materials_screening.Model) objects.

This also is a point to retrive the LCA output (e.g., [`get_impacts_by_category_models()`](#pod_lca.materials_screening.Project.get_impacts_by_category_models))

---

### *class* pod_lca.materials_screening.Project

Project class which maintains the process models and a link to the impact database.

#### name

Name of the project.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### models

All models created/compared in the current project: {**model name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [`Model`](model.md#pod_lca.materials_screening.Model)}.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### year

Year of material production project.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### location

Location of the project.

* **Type:**
  [*Location*](location.md#pod_lca.location.Location)

#### impact_database

Maintains input impact data.

* **Type:**

#### transport_mode_impact_database

Maintains impact data of transportation.

* **Type:**

#### *classmethod* new(name=None)

Create a new project.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the project.
* **Returns:**
  Project created.
* **Return type:**
  [*Project*](#pod_lca.materials_screening.Project)

#### set_name(name: [str](https://docs.python.org/3/library/stdtypes.html#str))

Set the name of the project.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the project.

#### set_databases()

Set databases and datasets to be used in the LCA computations.

#### set_material_database(file_path=None)

Set the impact database. If file path is not provided, the default database will be used.

* **Parameters:**
  **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Filepath to the csv file containing impact data. The csv file must contain headers 'sctg code' and 'eol material' in addition to the

#### set_transportation_mode_impact_database(file_path=None)

Set the impact database for end-of-life impacts. If file path not given, the default database will be used.

* **Parameters:**
  **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Filepath to the csv file containing impact data.

#### set_eol_process_impact_database(file_path=None, \*\*kwargs)

Set the impact database for end-of-life impacts. If file path not given, default database will be used.

* **Parameters:**
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Filepath of the csv file containing impact data.
  * **primary_key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Header of the primary identifier column in the csv file. Default is 'Material'.
  * **process_key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Header of the process identifier column in the csv file. Default is 'Process'.
  * **lc_stage_key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Header of the life cycle stage identifier column in the csv file. Default is 'LCA Stage'.
  * **transport_dataset** ([*TransportDataset*](transport_datasets.md#pod_lca.transportation.TransportDataset)) -- Transportation dataset corresponding to the end-of-life impacts.

#### set_eol_transport_dataset(dataset=None)

Set transportation dataset for the end-of-life impacts.

* **Parameters:**
  **dataset** ([*TransportDataset*](transport_datasets.md#pod_lca.transportation.TransportDataset)) -- End-of-life transportation dataset.

#### set_location(location)

Set the location of the project.

* **Parameters:**
  **location** ([*Location*](location.md#pod_lca.location.Location)) -- Location of the project.

#### set_year(year)

Set manufacturing year.

* **Parameters:**
  **year** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Year of material production process.

#### get_name()

Retrieve the name of the project.

* **Returns:**
  Name of the project.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_impact_database()

Get the impacts database of the project.

* **Returns:**
  Impact database of the project.
* **Return type:**
  [*ImpactsDatabase*](impacts-database.md#pod_lca.impacts.ImpactsDatabase)

#### get_transportation_mode_impact_database()

Get the impacts database of the project.

* **Returns:**
  Impact database of the tranportation modes.
* **Return type:**
  [*TranportationModeImpactsDatabase*](impacts-database.md#pod_lca.impacts.TranportationModeImpactsDatabase)

#### get_location()

Retrieve the location of the project.

* **Returns:**
  Location of the project.
* **Return type:**
  [*Location*](location.md#pod_lca.location.Location)

#### get_year()

Retrieve manufacturing year.

* **Returns:**
  Year of material production process.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### add_model(model_name, file_path=None)

Create and add a model to the current project.

* **Parameters:**
  **model_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the model to be created.

#### get_model(model_name)

Retrieve a model.

* **Parameters:**
  **model_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the model to be retrieved.
* **Returns:**
  Current working model.
* **Return type:**
  [*Model*](model.md#pod_lca.materials_screening.Model)
* **Raises:**
  [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- A model by such name does not exist in the current project.

#### get_model_names()

Get all names of all the models in the project.

* **Returns:**
  List of model names.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [str](https://docs.python.org/3/library/stdtypes.html#str)

#### clear_project(model=True, database=True)

Remove all existing models and the impact database of the project.

* **Parameters:**
  * **model** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- True if all the models are to be cleared.
  * **database** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- True if the database is to be cleared.

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

#### get_impacts_by_LCstages_models(impact_category, model_lst=None)

Return impact data by life cycle stage for given multiple model and impact category.

* **Parameters:**
  * **impact_category** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the Impact category.
  * **model_lst** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- list of the names of models.
* **Returns:**
  Impacts dictionary where {**model_name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): {**stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **quantity of impact** ([`float`](https://docs.python.org/3/library/functions.html#float))}}.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### get_impacts_by_category_models(model_lst=None)

Return impact data by impact category for given multiple models.

* **Parameters:**
  **model_lst** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- List of the names of models.
* **Returns:**
  Impacts dictionary where {**model_name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): {**impact_category** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : **quantity of impact** ([`float`](https://docs.python.org/3/library/functions.html#float))}}.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### get_normalized_impacts_by_category_models(model_lst=None)

Return impact data by impact category for given multiple models.

* **Parameters:**
  **model_lst** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- List of the names of models.
* **Returns:**
  Impacts dictionary where {**model_name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): {**impact_category** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : **quantity of impact** ([`float`](https://docs.python.org/3/library/functions.html#float))}}.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### get_impacts_by_LCstages_models_items(impact_category, model_lst=None)

Return impact data by life cycle stage for given multiple model and impact category, with impacts
: identifieable by individaul item.

* **Parameters:**
  * **impact_category** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the Impact category.
  * **model_lst** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- List of the names of models.
* **Returns:**
  Impacts dictionary where {**model_name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): {**stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): {**item_name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **quantity of impact** ([`float`](https://docs.python.org/3/library/functions.html#float))}}.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### get_impacts_by_impactcategorys_models_LCstage(impact_categories, model_lst=None)

Return data for a barchart.

* **Parameters:**
  * **impact_categories** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- List of impact categories.
  * **model_lst** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- List of the names of models.
* **Returns:**
  Impacts dictionary where {**model_name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): {**impact_category** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): {**stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **quantity of impact** ([`float`](https://docs.python.org/3/library/functions.html#float))}}.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)
