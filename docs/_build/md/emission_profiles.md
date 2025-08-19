# Emission Profiles

---

### *class* pod_lca.dynamic_radiative_forcing.temporal_emission_profiles.TemporalEmissionProfiles

Bases: [`DataDistribution`](datasets.md#pod_lca.uncertainty.DataDistribution)

Temporal emission profiles for the purpose of calculating dynamic radiative forcing.

#### start

starting point of the temporal emission profile.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int) or [float](https://docs.python.org/3/library/functions.html#float)

#### duration

Duration of the temporal emission profile.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int) or [float](https://docs.python.org/3/library/functions.html#float)

#### set_start(start)

Set the starting point of the temporal emission profile.

* **Parameters:**
  **start** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- starting point of the temporal emission profile.

#### set_duration(duration)

Set the duration of the temporal emission profile.

* **Parameters:**
  **duration** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Duration of the temporal emission profile.

#### get_start()

Get the starting point of the temporal emission profile.

* **Returns:**
  starting point of the temporal emission profile.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int) or [float](https://docs.python.org/3/library/functions.html#float)

#### get_duration()

Get the duration of the temporal emission profile.

* **Returns:**
  duration of the temporal emission profile in years.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int) or [float](https://docs.python.org/3/library/functions.html#float)

#### discrete_from_continous(start, range, step, integrate_point='left', cutoff=True, unitize=True)

Create a discrete data set from the continous distribution.

* **Parameters:**
  * **start** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Starting value of the discrete data set.
  * **range** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Range of the data set.
  * **step** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Step of the discrete data series.
  * **integrate_point** ( *{'left'* *,*  *'middle'* *,*  *'right'}*) -- Point to which the data is grouped.
  * **cutoff** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- Set distribution values before and after the range to zero.
* **Returns:**
  Discrete sequence of data.
* **Return type:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)
