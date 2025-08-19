# Inventory Records

Inventory records are containers for [`Impacts`](#pod_lca.impacts.Impacts), [`Emissions`](#pod_lca.impacts.Emissions), and [`CarbonStorage`](#pod_lca.impacts.CarbonStorage) data. They all inherit from [`Records`](#pod_lca.impacts.Records).

---

### *class* pod_lca.impacts.Records

Records object keep record of the inventory (e.g., impacts, emissions, carbon storage) created by a product or a process.

#### parent

The product or process object to which this record belong.

* **Type:**
  [*Master*](products.md#pod_lca.materials_screening.Master)

### <record_category>

Record categories are dynamically set based on the class.
Class variable 'record_attr_dict' keep track of the record category names and corresponding units.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### *classmethod* from_parent(parent)

Create an record object from a parent object.

* **Parameters:**
  **parent** ([*Master*](products.md#pod_lca.materials_screening.Master)) -- The product or process object to which this record belong.
* **Returns:**
  Record created.
* **Return type:**
  [*Records*](#pod_lca.impacts.Records)

#### *classmethod* from_dict(record_dict)

Create an record object from a dictionary.

* **Parameters:**
  **record_dict** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- Dictionary of records {**record catergory** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **record quantity** ([`float`](https://docs.python.org/3/library/functions.html#float))}
* **Returns:**
  Record created.
* **Return type:**
  [*Records*](#pod_lca.impacts.Records)

#### *classmethod* copy(record_obj)

Make a copy of the record object.

* **Returns:**
  Copy of the object.
* **Return type:**
  [*Records*](#pod_lca.impacts.Records)

#### set_parent(parent)

Set the parent object.

* **Parameters:**
  **parent** () -- The product or process object to which this record belong.

#### get_parent()

Retrieve the product or process object to which this record belong.

* **Returns:**
  Product or process object to which this record belong.
* **Return type:**
  [*Master*](products.md#pod_lca.materials_screening.Master)

#### get_categories(units=False)

Retrieves the categories (i.e., entry names) in the record.

* **Parameters:**
  **units** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, returns a dictionary of categories and corresponding units.
* **Returns:**
  * [`list`](https://docs.python.org/3/library/stdtypes.html#list) -- list of categories.
  * [`dict`](https://docs.python.org/3/library/stdtypes.html#dict) -- Dictionary of units, keyed by category name.

#### clear_qty()

Set all record quantities to zero.

#### update_qty(records)

Update the record quantities.

* **Parameters:**
  **records** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- Dictionary of records - { **record catergory** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **record quantity** ([`float`](https://docs.python.org/3/library/functions.html#float))}

#### get_record(attr)

Get the quantity of a specific record attribute.

* **Parameters:**
  **attr** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the record attribute of concern (e.g., impact category, emission gas).
* **Returns:**
  Quantity of the record attribute.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_record_dict()

Get the record as a dictionary.

* **Returns:**
  Dictionary of impacts - { **impact catergory** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **impact quantity** ([`float`](https://docs.python.org/3/library/functions.html#float))}
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

### *class* pod_lca.impacts.Impacts

Bases: [`Records`](#pod_lca.impacts.Records)

Impacts object keep record of the impacts created by a product or a process.

#### parent

The product or process object to which this impacts record belong.

* **Type:**
  [*Master*](products.md#pod_lca.materials_screening.Master)

### <impact_category>

Impact categories are dynamically set based on the class variable 'record_attr_dict'.
This is set to the IMPACT_CATEGORIES in the config file.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_weighted_impact(method='TRACI_EPA')

Get a normalized and weighted value for impacts.

#### NOTE
Reference: The Carbon Leadership Forum. (2018) Life Cycle ASssesment of Buildings: A Practice Guide. DOI: [http://hdl.handle.net/1773/41885](http://hdl.handle.net/1773/41885)

* **Parameters:**
  **method** ( *{'TRACI_EPA'* *,*  *'TRACI_NIST'}*) -- 

  Weightages to be used:
  - 'TRACI_EPA': From Ref [1].
  - 'TRACI_NIST': From Ref [1].

  Default is 'TRACI_EPA'.
* **Returns:**
  The weighted impact.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)
* **Raises:**
  [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- Weighing method not recognied.

#### get_adjusted_GWP()

Get GWP values adjusted for biogenic and accelerated carbonation effects.

* **Returns:**
  Adjusted GWP value
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)
* **Raises:**
  [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- Impact category not recognied.

### *class* pod_lca.impacts.Emissions

Bases: [`Records`](#pod_lca.impacts.Records)

Emissions object keep record of the emissions created by a product or a process.

#### parent

The product or process object to which this emissions record belong.

* **Type:**
  [*Master*](products.md#pod_lca.materials_screening.Master)

### <emission_name>

Emission names are dynamically set based on the class variable 'record_attr_dict'.
Currently, this is set to the EMISSION_INVENTORIES in the config file.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### temporal_emission_profile

Function describing the dynamic emission profile.

* **Type:**
  [*DataDistribution*](datasets.md#pod_lca.uncertainty.DataDistribution)

#### methane_bio_oxidation

Percentage of biogenic methane oxidating to CO2.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### *classmethod* from_parent(parent)

Create an record object from a parent object.

* **Parameters:**
  **parent** ([*Master*](products.md#pod_lca.materials_screening.Master)) -- The product or process object to which this record belong.
* **Returns:**
  Record created.
* **Return type:**
  [*Emissions*](#pod_lca.impacts.Emissions)

#### *classmethod* from_dict(record_dict)

Create an record object from a dictionary.

* **Parameters:**
  **record_dict** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- Dictionary of records {**record catergory** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): **record quantity** ([`float`](https://docs.python.org/3/library/functions.html#float))}
* **Returns:**
  Records created.
* **Return type:**
  *Record*

#### set_temporal_emission_profile(time_profile)

Set the dyanamic emissions function.

* **Parameters:**
  **time_profile** ([*DataDistribution*](datasets.md#pod_lca.uncertainty.DataDistribution)) -- Function describing the dynamic emission profile.
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Data distribution type not recognized.

#### get_temporal_emission_profile()

Get the dyanamic emissions function.

* **Returns:**
  Function describing the dynamic emission profile.
* **Return type:**
  [*DataDistribution*](datasets.md#pod_lca.uncertainty.DataDistribution)

#### get_start_year()

Set year of the emission.

* **Returns:**
  Year of the emission occuring.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_emission_duration()

Get the duration of emissions.

* **Returns:**
  Duration of emission, in years.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

### *class* pod_lca.impacts.CarbonStorage

Bases: [`Records`](#pod_lca.impacts.Records)

CarbonStorage object keep record of the carbon storage records created by a product or a process.

#### parent

The product or process object to which this carbon storage record belong.

* **Type:**
  [*Master*](products.md#pod_lca.materials_screening.Master)

### <category>

Carbon storage categories are dynamically set based on the class variable 'record_attr_dict'.
Currently, this is set to the CARBON_STORAGE in the config file.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)
