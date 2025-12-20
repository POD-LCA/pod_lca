# Dynamic Radiative Forcing Calculator

[`DynamicRadiativeForcing`](#pod_lca.dynamic_radiative_forcing.DynamicRadiativeForcing) class is a collection of methods for calculation of dynamic radiative forcing and associate parameters.

---

### *class* pod_lca.dynamic_radiative_forcing.DynamicRadiativeForcing(ipcc_ar=None)

Computation methods related to dynamic radiative forcing methods.

#### calculator

Methods specified in IPCC Annual Reports.

* **Type:**
  *ARXCalculator*

#### get_radiative_efficiency(greenhouse_gas, ref_unit='Wm-2ppb-1', adjust_for_indirect_effects=True)

Get the radiative efficiency of given greenhouse_gas.

* **Parameters:**
  * **greenhouse_gas** ( *{'CO2'* *,*  *'CH4'* *,*  *'N2O'}*) -- Name of the greenhouse gas.
  * **ref_unit** ( *{'Wm-2ppb-1'* *,*  *'Wm-2kg-1'}*) -- Output unit.
  * **adjust_for_indirect_effects** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- Adjust radiative efficiency to account for indirect effects.
* **Returns:**
  Radiative efficiency, in the reference unit.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Reference unit not recognized.

#### get_pertubation_lifetime(greenhouse_gas)

Get the pertubation lifetime of the greenhouse_gas in question.

* **Parameters:**
  **greenhouse_gas** ( *{'CO2'* *,*  *'CH4'* *,*  *'N2O'}*) -- Name of the greenhouse gas.
* **Returns:**
  Pertubation lifetime in years.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_atmospheric_concentration(greenhouse_gas, at_year, cumulative=False)

Get the concentration of the greenhouse gas in the atmosphere at a given year, given that a 1kg of gas emitted on start of year 0.

* **Parameters:**
  * **greenhouse_gas** ( *{'CO2'* *,*  *'CH4'* *,*  *'N2O'}*) -- Name of the greenhouse gas.
  * **at_year** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) -- Year(s) at which concentration computed, given that a 1kg of gas emitted on start of year 0.
  * **cumulative** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- Cumulative values if true, else instantaneous values.
* **Returns:**
  Concentration of the greenhouse gas, in kg (if not cumulative) or in kg-yrs (if cumulative).
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_radiative_forcing(greenhouse_gas, at_year, cumulative=False, CH4_oxidation=False, alpha=0.5, convolution_time_step=0.01)

Get the radiative forcing (in W/m^2) of the greenhouse gas at a given year, given that a 1kg of gas emitted on start year.

* **Parameters:**
  * **greenhouse_gas** ( *{'CO2'* *,*  *'CH4'* *,*  *'N2O'}*) -- Name of the greenhouse gas.
  * **at_year** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) -- Year(s) at which concentration computed, given that a 1kg of gas emitted on start of year 0.
  * **cumulative** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- Cumulative values if true, else instantaneous values.
  * **CH4_oxidation** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, account for oxidation of CH4 to CO2.
  * **alpha** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Fraction of CH4 oxidized: 0.5-1.0.
  * **convolution_time_step** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Time step for CH4 oxidation.
* **Returns:**
  radiative forcing, in W/m2.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_concentration_time_series(greenhouse_gas, time_horizon, time_step, cumulative=False)

Get the concentration of the greenhouse gas in the atmosphere as a time-series.

#### NOTE
Noting the behaviour of numpy.arange with floats, the end value of years is checked against time horizon.

* **Parameters:**
  * **greenhouse_gas** ( *{'CO2'* *,*  *'CH4'* *,*  *'N2O'}*) -- Name of the greenhouse gas.
  * **time_horizon** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Time horizon in years.
  * **time_step** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Time step in years.
  * **cumulative** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- Cumulative radiative forcing if true, else instantaneous values.
* **Returns:**
  * [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) -- years of the time series
  * [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) -- concentration values at the end of the year.
  * [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) -- concentration values at the end of the year #TODO: double check this

#### get_radiative_forcing_time_series(greenhouse_gas, time_horizon, time_step, cumulative=True, CH4_oxidation=False, alpha=0.5)

Get the daynamic radiative forcing values (in W/m^2) as a time-series, given that a 1kg of gas emitted on start year.

* **Parameters:**
  * **greenhouse_gas** ( *{'CO2'* *,*  *'CH4'* *,*  *'N2O'}*) -- Name of the greenhouse gas.
  * **time_horizon** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Time horizon in years.
  * **time_step** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Time step in years.
  * **cumulative** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- Cumulative radiative forcing if true, else instantaneous values.
  * **CH4_oxidation** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, account for oxidation of CH4 to CO2
  * **alpha** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Fraction of CH4 oxidized: 0.5-1.0
* **Returns:**
  * [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) -- Years of the time series
  * [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) -- Atmospheric concentration values at the end of the year
  * [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) -- Radiative forcing values at the end of the year
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Reference unit not recognized.

#### get_AGWP(greenhouse_gas, time_horizon)

Get the Absolute Global Warming Potential (AGWP) of a greenhouse gas, for the given time_horizon.

#### NOTE
Convolution time step of 0.01 is used.

* **Parameters:**
  * **greenhouse_gas** ( *{'CO2'* *,*  *'CH4'* *,*  *'N2O'* *,*  *'CH4 fossil'}*) -- Name of the greenhouse gas.
  * **time_horizon** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Time horizon in years.

#### get_GWP(greenhouse_gas, time_horizon)

Get the Global Warming Potential (GWP) of a greenhouse gas, for the given time_horizon.

#### NOTE
Convolution time step of 0.01 is used.

* **Parameters:**
  * **greenhouse_gas** ( *{'CO2'* *,*  *'CH4'* *,*  *'N2O'* *,*  *'CH4 fossil'}*) -- Name of the greenhouse gas.
  * **time_horizon** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Time horizon in years.
* **Returns:**
  GWP value.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)
