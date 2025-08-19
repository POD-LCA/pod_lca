# Dynamic Radiative Forcing Record

[`DynamicRadiativeForcingRecord`](#pod_lca.dynamic_radiative_forcing.DynamicRadiativeForcingRecord) class object will keep track of assigned `Emission` objects ([`add_emission_records()`](#pod_lca.dynamic_radiative_forcing.DynamicRadiativeForcingRecord.add_emission_records)) and create dynamic radiative forcing time series data ([`get_data()`](#pod_lca.dynamic_radiative_forcing.DynamicRadiativeForcingRecord.get_data)).

---

### *class* pod_lca.dynamic_radiative_forcing.DynamicRadiativeForcingRecord

This record keeps a timeseries record of the dynamic radiative forcing from emissions.

#### start_year

Start year of the emissions record.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### time_horizon

Time horizon in years.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### time_step

Time step of the record. The same time step is used for both for integration and for reporting.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int) or [float](https://docs.python.org/3/library/functions.html#float)

#### emissions_lst

List of emissions considered in the record.

* **Type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Emissions*](impact_records.md#pod_lca.impacts.Emissions)

#### data_years

Years in the record.

* **Type:**
  numpy.array of [int](https://docs.python.org/3/library/functions.html#int) or [float](https://docs.python.org/3/library/functions.html#float)

#### data_emission_intensity

Emission intensity (in kg/yr); {**greenhous gas** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [**emission intensity** ([`float`](https://docs.python.org/3/library/functions.html#float))]}.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### data_concentrations

Atmospheric concentration (in kg); {**greenhous gas** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [**atmospheric concenration** ([`float`](https://docs.python.org/3/library/functions.html#float))]}.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### data_irf

Instantaneous radiative forcing values at the time steps (in W/m^2); {**greenhous gas** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [**irf** ([`float`](https://docs.python.org/3/library/functions.html#float))]}.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### data_crf

Cumulative radiative forcing values at the time steps (in W/m^2); {**greenhous gas** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [**crf** ([`float`](https://docs.python.org/3/library/functions.html#float))]}.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### *classmethod* from_emissions(emissions, start_year=2025, time_horizon=100, time_step=0.08333333333333333)

Create a dynamic radiative forcing (DRF) record from emissions.

* **Parameters:**
  * **emissions** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*Emissions*](impact_records.md#pod_lca.impacts.Emissions) *or* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Emissions in the record.
  * **start_year** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Start year of the record.
  * **time_horizon** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Time horizon of the record, in years.
  * **time_step** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Time step of the record, in years.
* **Returns:**
  DRF record object.
* **Return type:**
  [*DynamicRadiativeForcingRecord*](#pod_lca.dynamic_radiative_forcing.DynamicRadiativeForcingRecord)

#### *classmethod* from_products(products, start_year=2025, time_horizon=100, time_step=0.08333333333333333)

Create a dynamic radiative forcing (DRF) record from products, inheriting from Master Obj.

* **Parameters:**
  * **products** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*Product*](products.md#pod_lca.materials_screening.Product) *or* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Products in the record.
  * **start_year** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Start year of the record.
  * **time_horizon** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Time horizon of the record, in years.
  * **time_step** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Time step of the record, in years.
* **Returns:**
  DRF record object.
* **Return type:**
  [*DynamicRadiativeForcingRecord*](#pod_lca.dynamic_radiative_forcing.DynamicRadiativeForcingRecord)

#### set_start_year(year)

Set the start year of the dynamic radiative forcing record.

* **Parameters:**
  **start_year** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Start year of the emissions record.

#### set_time_horizon(years)

Set the time horizon (in years) of the dynamic radiative forcing record.

* **Parameters:**
  **time_horizon** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Time horizon in years.

#### set_time_step(time_step)

Set the time step for time series record.

* **Parameters:**
  **time_step** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Time step of the record.

#### set_data()

Set dynamic radiative forcing data.

* **Returns:**
  * [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`int`](https://docs.python.org/3/library/functions.html#int) -- Time steps in the record.
  * [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`float`](https://docs.python.org/3/library/functions.html#float) -- Radiative forcing values at the time steps.

#### get_start_year()

Get the start year of the dynamic radiative forcing record.

* **Returns:**
  Start year of the emissions record.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_time_horizon()

Get the time horizon (in years) of the dynamic radiative forcing record.

* **Returns:**
  Time horizon in years.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_emissions_list()

Get the list of emissions assigned to the dynamic radiative forcing record.

* **Returns:**
  List of emissions considered in the record.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Emissions*](impact_records.md#pod_lca.impacts.Emissions)

#### get_time_step()

Set the time step for time series record.

* **Returns:**
  Time step of the record.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_data(data_category='radiative forcing', xy_pairs=True)

Get the dynamic radiative forcing data.

* **Parameters:**
  * **data_category** ( *{'emission intensity'* *,*  *'atmospheric concentration'* *,*  *'instantaneous radiative forcing'* *,*  *'cumulative radiative forcing'}*) -- Category of data to be reported. Default is 'radiative forcing'.
  * **xy_pairs** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, provide data as xy pairs, else as sperate lists. Default is True.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Data category is not recognized.

#### add_emission_records(emissions)

Assign an emission to the dynamic radiative forcing record.

* **Parameters:**
  **emissions** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *or* *Emissions*) -- Emission(s) to be assigned to the record

#### plot(to_plot='atmospheric concentration', plot_type='lineplot', plot_time_step=10, colors=None)

Plot the dynamic radiative forcing record.

* **Parameters:**
  * **to_plot** ( *{'atmospheric concentration'* *,*  *'emission'* *,*  *'instantaneous radiative forcing'* *,*  *'Cumulative Dynamic Radiative Forcing Record'}*) -- Parameter to be ploted.
  * **plot_type** ( *{'lineplot'* *,*  *'stackplot'}*) -- Type of the plot.
  * **plot_time_step** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Time step for ticks along x axis.
  * **colors** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Colors of each line or stack.
* **Raises:**
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Parameter to be plotted is not recognized.
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Plot type is not recognized.

#### save(file_path, emission_intensity=True, concentration=True, irf=True, crf=True)

Write the data to a file.

* **Parameters:**
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the save file.
  * **emission_intensity** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, save emission intensity values of greenhouse gases.
  * **concentration** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- if true, save atmospheric concentration of greenhouse gases.
  * **irf** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, save the Instantaneous Radiative Forcing (IRF) values of greenhouse gases.
  * **crf** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, save the Cumulative Radiative Forcing (IRF) values of greenhouse gases.
