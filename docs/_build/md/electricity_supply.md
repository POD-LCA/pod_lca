# Electricity Supply

[`ElectricitySupply`](#pod_lca.electricity.ElectricitySupply) manages the  electricity usage (supply and distribution) aspects including mix of electricity generation technologies. The grid mixes are predicted for future using the data produced by [Cambium](https://www.nrel.gov/analysis/cambium) which is managed via [`CambiumData`](#pod_lca.electricity.CambiumData) class.

---

### *class* pod_lca.electricity.ElectricitySupply

Electricity supplier manages the distribution of electricity from the electricity producers to the consumers.

#### name

The name of the electricity supply authority.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### geographical_scope

Geographical scope of the electricity supply.

- 'National': US average
- 'Regional': FERC region
- 'Local': Balancing Authority.

* **Type:**
  {'National', 'Regional', 'Local'}

#### location

The location of the electricity supply authority.

* **Type:**
  [*Location*](location_module.md#pod_lca.location.Location)

#### consumption_mix

The consumption mix of the electricity supply authority: {**technology**: [`str`](https://docs.python.org/3/library/stdtypes.html#str)}.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### year

The year of the electricity supply authority.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### impacts

The impacts of the electricity supply authority.

* **Type:**
  [*Impacts*](impact_records.md#pod_lca.impacts.Impacts)

### Notes

1. Location, regionality, and year determines the consumption mix.
2. Location and regionality determines the impact by technology.

#### *classmethod* from_location(location, year=None)

Create a new Electricity supplier for the given location.

* **Parameters:**
  * **location** ([*Location*](location_module.md#pod_lca.location.Location)) -- The location of the electricity supply authority.
  * **year** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Year of electricity consumption.
* **Returns:**
  Electricity supplier for the given location.
* **Return type:**
  [*ElectricitySupply*](#pod_lca.electricity.ElectricitySupply)

#### set_name(name)

Set the name of the electricity supply authority.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- The name of the electricity supply authority.

#### set_geographical_scope(geographical_scope)

Set the geographical cope of the electricity supply authority.

* **Parameters:**
  **geographical_scope** ( *{'National'. 'Regional'* *,*  *'Local'}*) -- 

  Geographical scope of the electricity supply.
  - 'National': US average
  - 'Regional': FERC region
  - 'Local': Balancing Authority.

#### set_location(location)

Set the location of the electricity supply authority.

* **Parameters:**
  **location** ([*Location*](location_module.md#pod_lca.location.Location)) -- The location of the electricity supply authority.

#### set_consumption_mix(consumption_mix)

Set the consumption mix of the electricity supply authority.

* **Parameters:**
  **consumption_mix** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- The consumption mix of the electricity supply authority: {**technology**: [`str`](https://docs.python.org/3/library/stdtypes.html#str)}.

#### set_year(year)

Set the year of the electricity supply authority.
: Changing the year changes the consumption mix based on Cambium data.

* **Parameters:**
  **year** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- The year of the electricity supply authority.

#### set_declared_unit(unit)

Set the declared unit of impacts.

* **Parameters:**
  **unit** ([*Unit*](units.md#pod_lca.units.Unit)) -- Declared unit.

#### set_scenario(scenario)

Set scenario name. This will be used with cambium data.

* **Parameters:**
  **scenario** ( *{'MidCase'* *,*  *'LowRECost'* *,*  *'HighRECost'* *,*  *'HighDemandGrowth'* *,*  *'LowNGPrice'* *,*  *'HighNGPrice'* *,*  *'Decarb95by2050'* *,*  *'Decarb100by2035'}*) -- Electricity consmuption scenario considered.

#### set_electricity_producers(geographical_scope)

Set the electricity producers for a given technology mix and corresponding impact data.

* **Parameters:**
  **geographical_scope** ( *{'National'. 'Regional'* *,*  *'Local'}*) -- 

  Geographical scope of the electricity supply.
  - 'National': US average
  - 'Regional': FERC region
  - 'Local': Balancing Authority.
* **Raises:**
  * [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- FERC region not found for location.
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Geographical scope of electricity supply is not recognized.

#### get_name()

Get the name of the electricity supply authority.

* **Returns:**
  The name of the electricity supply authority.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_geographical_scope()

Get the set geographical scope of the electricity supply authority.

* **Returns:**
  The geographical scope of the electricity supply.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_location()

Get the location of the electricity supply authority.

* **Returns:**
  The location of the electricity supply authority.
* **Return type:**
  [*Location*](location_module.md#pod_lca.location.Location)

#### get_consumption_mix()

Get the consumption mix of the electricity supply authority.

* **Returns:**
  The consumption mix of the electricity supply authority: {**technology**: [`str`](https://docs.python.org/3/library/stdtypes.html#str)}.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### get_year()

Get the year of the electricity supply authority.

* **Returns:**
  The year of the electricity supply authority.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_unit_impacts()

Get the impacts of the electricity supply authority.

* **Returns:**
  The impacts of the electricity supply authority.
* **Return type:**
  [*Impacts*](impact_records.md#pod_lca.impacts.Impacts)

#### get_unit_emissions()

Get the emissions of the electricity supply authority.

* **Returns:**
  The emissions of the electricity supply authority.
* **Return type:**
  [*Emissions*](impact_records.md#pod_lca.impacts.Emissions)

#### get_scenario()

Get the elecetricity consumption scenario.

#### get_declared_unit()

Get the declared unit of the impacts.

* **Returns:**
  Declared unit
* **Return type:**
  [*Unit*](units.md#pod_lca.units.Unit)

#### pick_region(regions, impact_database, impact_category='GWP')

Pick the region with the highest impact from a list of regions.

* **Parameters:**
  * **regions** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- List of regions to choose from.
  * **impact_data** ([*pandas.DataFrame*](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)) -- DataFrame containing impact data for the regions.
  * **impact_category** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- The impact category to consider for the selection.
* **Returns:**
  The region with the highest impact.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### update_inventory_records()

Set the impacts of the electricity supply authority.

#### get_impact_distribution()

Get the distribution of the electricity supply authority.

* **Returns:**
  * [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`Impacts`](impact_records.md#pod_lca.impacts.Impacts) -- Impact objects representing the distribution of the impacts.
  * [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`int`](https://docs.python.org/3/library/functions.html#int) -- List of weights for each impact object in the distribution.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Geographical scope of electricity supply is not recognized.

### *class* pod_lca.electricity.CambiumData

A class to operate on cambium data.

#### data

Pandas dataframe of cambium data loaded.

* **Type:**
  [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)

#### *classmethod* from_geographical_scope(geographical_scope, location)

Create cambium data object from regionalised data.

* **Parameters:**
  * **geographical_scope** ( *{'National'* *,*  *'Regional'* *,*  *'Local'}*) -- Geographical scope of data.
  * **location** ([*Location*](location_module.md#pod_lca.location.Location) *or* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of electricity supply.
    If a string is provided, it should be the country code for national level data,
    region name for regional level data, or REEDS balancing authority for local level data.
* **Raises:**
  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Location is not a string or Location object.
  * [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- Geographical scope not recognized.

#### get_mix(year, technologies, scenario='MidCase', interpolate='values')

Get technology mix of the electricity consumption by year.

### Notes

Cambium data are available for 5 year increments from 2025 to 2050. The data are linearly interpolated for the years in between.

* **Parameters:**
  * **year** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Year of electricity consumption.
  * **technologies** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of electricity generation technoclogies to be classified by.
  * **scenario** ( *{'MidCase'* *,*  *'LowRECost'* *,*  *'HighRECost'* *,*  *'HighDemandGrowth'* *,*  *'LowNGPrice'* *,*  *'HighNGPrice'* *,*  *'Decarb95by2050'* *,*  *'Decarb100by2035'}*) -- Electricity consmuption scenario considered. Default is 'MidCase'
  * **interpolate** ( *{'values'* *,*  *'percentages'}*) -- 

    Linear interpolation of electricity consumption between two years.
    - 'values': interpolate values
    - 'percentages': interpolate percentages

    Default is by 'values'.
* **Returns:**
  Dictionary of electricity generation technology in percentages.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)
* **Raises:**
  [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- Interpolation method not recognized.

#### get_load(year, scenario='MidCase')

Get electricity load of the electricity consumption by year.

* **Parameters:**
  * **year** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Year of electricity consumption.
  * **scenario** ( *{'MidCase'* *,*  *'LowRECost'* *,*  *'HighRECost'* *,*  *'HighDemandGrowth'* *,*  *'LowNGPrice'* *,*  *'HighNGPrice'* *,*  *'Decarb95by2050'* *,*  *'Decarb100by2035'}*) -- Electricity consmuption scenario considered. Default is 'MidCase'.
* **Returns:**
  Electricity load in GWh.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### delete_data()

Delete the cambium data object.
