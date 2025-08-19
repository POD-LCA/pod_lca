# Data Distributions

[`DataDistribution`](#pod_lca.uncertainty.DataDistribution) objects holds underlying [`data`](#pod_lca.uncertainty.DataDistribution.data) or `distribution` corresponding to an `attribute` of another [`object`](#pod_lca.uncertainty.DataDistribution.parent) (e.g., [`Master`](products.md#pod_lca.materials_screening.Master))

A selected set of distributions of known distribution parameters are available for use: [`Uniform`](#pod_lca.uncertainty.Uniform), [`Normal`](#pod_lca.uncertainty.Norm), [`Log Normal`](#pod_lca.uncertainty.LogNorm), and [`Exponential Decay`](#pod_lca.uncertainty.ExponentDecay).

---

### *class* pod_lca.uncertainty.DataDistribution

Dataset object with the corresponding distribution fitted from Scipy.stats package.
: A Dataset is a collection (list) of data points.

#### name

Name of the data set.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### data

The data set.

* **Type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [float](https://docs.python.org/3/library/functions.html#float) (or [str](https://docs.python.org/3/library/stdtypes.html#str))

#### dist_name

Distribution name as used in `scipy.stats`.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### dist

Fitted distribution object from Scipy.

* **Type:**
  [scipy.stats.rv_continuous](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html#scipy.stats.rv_continuous) or [scipy.stats.rv_discrete](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_discrete.html#scipy.stats.rv_discrete)

#### parent

Object to which the dataset is attached.

* **Type:**
  [object](https://docs.python.org/3/library/functions.html#object)

#### attr

Attribute to which dataset is attached.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### scenarios

Definition of quartile points for scenarios.
For continous variables values are numbers between 0-1.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### is_cts

If true, the data are from a contrinous variable, otherwise a discrete variable.

* **Type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### *classmethod* from_data(data, is_cts, name='unspecified', del_data=False, set_dist=True)

Create a Dataset object from data input.

* **Parameters:**
  * **data** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*float*](https://docs.python.org/3/library/functions.html#float)) -- The data set.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the data set.
  * **is_cts** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, the data are from a contrinous variable, otherwise a discrete variable.
* **Returns:**
  Data distribution created.
* **Return type:**
  [*DataDistribution*](#pod_lca.uncertainty.DataDistribution)

#### *classmethod* from_distributions(dist, is_cts, name='unspecified')

Create a Dataset object from data input.

* **Parameters:**
  * **dist** ([*scipy.stats.rv_continuous*](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html#scipy.stats.rv_continuous)) -- Fitted distribution object from Scipy.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the data set.
  * **is_cts** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, the data are from a contrinous variable, otherwise a discrete variable.
* **Returns:**
  Data distribution created.
* **Return type:**
  [*DataDistribution*](#pod_lca.uncertainty.DataDistribution)

#### set_data(data)

Set data to the Data distribution.

* **Parameters:**
  **data** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*float*](https://docs.python.org/3/library/functions.html#float)) -- The data set.

#### set_name(name)

Set name to the data distribution.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the data set.

#### set_distribution(dist=None)

Set a distribution function to the data distribution.

* **Parameters:**
  **dist** ([*scipy.stats.rv_continuous*](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html#scipy.stats.rv_continuous) *or* [*scipy.stats.rv_discrete*](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_discrete.html#scipy.stats.rv_discrete)) -- Fitted distribution.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- A valid distribution could not be fitted.

#### set_parent(obj)

Set parent of the dataset.

* **Parameters:**
  **obj** ([*object*](https://docs.python.org/3/library/functions.html#object)) -- Object to which the dataset correspond.

#### set_attr_name(attr)

Set attribute to which the dataset belong.

* **Parameters:**
  **attr** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Attribute to which the dataset correspond.

#### set_scenario(scenario_name, value)

Set the statistic for a given scenario.

* **Parameters:**
  * **scenario_name** ( *{'high'* *,*  *'med'* *,*  *'low'}*) -- Scenario.
  * **value** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Scenario value given as a value between 0 and 1.

#### get_data()

Get data list.

* **Returns:**
  The data set.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [float](https://docs.python.org/3/library/functions.html#float)

#### get_name()

Get the name of the data distribution.

* **Returns:**
  Name of the data distribution.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_distribution()

Get the distribution fitted to the dataset.

* **Returns:**
  Fitted distribution.
* **Return type:**
  [scipy.stats.rv_continuous](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html#scipy.stats.rv_continuous) or [scipy.stats.rv_discrete](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_discrete.html#scipy.stats.rv_discrete)

#### get_dist_name()

Get the name of the distribution fitted.

* **Returns:**
  Distribution name as used in `scipy.stats`.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_attr()

Get the attribute to which the dataset belong.

* **Returns:**
  Attribute to which the dataset correspond.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_parent()

Get parent of the dataset.

* **Returns:**
  Object to which the dataset correspond.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

#### get_scenario(scenario_name)

Get the statistic for a given scenario.

* **Parameters:**
  **scenario_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Scenario name given as 'high', 'med', or 'low'.

#### delete_data()

Delete data from the dataset.

#### find_best_fit(is_cts=True, fit_method='MLE')

Find the best fit probability distribution for the data, considering the Kolmogorov–Smirnov (KS) test.

* **Parameters:**
  * **data** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- Data to be fitted.
  * **is_cts** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- True, if the data comes from a continous variable.
  * **fit_methods** ( *{'MLE'* *,*  *'MSE'}*) -- 

    Best fitting method:
    - 'MLE' - Maximum Likelihood Estimate
    - 'MSE' - Mean Squared Error
* **Returns:**
  Name of the selected distribution.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)
* **Raises:**
  [**NotImplementedError**](https://docs.python.org/3/library/exceptions.html#NotImplementedError) -- Could not discrimenate between eaqually good best-fits.

#### validate_dist_fit(dist_name, params)

Validate a distribution fitted to a dataset.

* **Parameters:**
  * **dist_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Distribution name as used in `scipy.stats`.
  * **params** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) -- Parameters corresponding to the fit.
* **Returns:**
  True if validated, otherwise False.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### fit_cts_distribution(dist_fit, fit_method='MLE')

Fit a distribution to the data.

* **Parameters:**
  * **dist_fit** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the distribution fitted to the data set, following Scipy.stats module.
  * **fit_methods** ( *{'MLE'* *,*  *'MSE'}*) -- 

    Best fitting method:
    - 'MLE' - Maximum Likelihood Estimate
    - 'MSE' - Mean Squared Error
* **Returns:**
  * [`scipy.stats.rv_continuous`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html#scipy.stats.rv_continuous) -- The fitted distribtuion to the data set.
  * [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple) -- Parameters of the fitted distribution.

#### generate_discrete_distribution()

Generate a discrete distribution from the data.

* **Returns:**
  Scipy discrete distribution.
* **Return type:**
  [scipy.stats.rv_discrete](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_discrete.html#scipy.stats.rv_discrete)

#### pick_data_point_from_distribution()

Pick a random variate from the distibution.

* **Returns:**
  A random variate from the distribution.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float) or [str](https://docs.python.org/3/library/stdtypes.html#str)

#### pick_data_points_from_distribution(n)

Pick a random variate from the distibution.

* **Parameters:**
  **n** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Number of points to pick.
* **Returns:**
  A list of random variates from the distribution.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)

#### prob_of(x)

Get the probability density at the given random variate.

* **Parameters:**
  **x** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Random variate picked.
* **Returns:**
  Probability density.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### percentile(p)

Get the percentile of the distribution.

* **Parameters:**
  **p** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Percentile to be calculated.
* **Returns:**
  Percentile of the distribution.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### discrete_from_continous(start, range, step, integrate_point='left')

Create a discrete data set from the continous distribution.

* **Parameters:**
  * **start** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Starting value of the discrete data set.
  * **range** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Range of the data set.
  * **step** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Step of the discrete data series.
  * **integrate_point** ( *{'left'* *,*  *'middle'* *,*  *'right'}*) -- Point to which the data is grouped.
* **Returns:**
  Discrete sequence of data.
* **Return type:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Integrate point not recognized.

### *class* pod_lca.uncertainty.Uniform

Bases: [`DataDistribution`](#pod_lca.uncertainty.DataDistribution)

A uniform data distribution.

#### *classmethod* from_params(start, step, name='unspecified')

Create a uniform distribution from parameters specified.

* **Parameters:**
  * **start** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Starting point of uniform distribution.
  * **step** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Width of the distributions (distribution ends at start + step).
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the data distribution.

### *class* pod_lca.uncertainty.Norm

Bases: [`DataDistribution`](#pod_lca.uncertainty.DataDistribution)

A normal data distribution.

#### *classmethod* from_params(mean, std_dev, name='unspecified')

Create a normal distribution from parameters (mean and standard deviation) specified.

* **Parameters:**
  * **mean** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Mean of the normal distribution.
  * **std_dev** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Standard deviation of the normal distribution.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the data distribution.

### *class* pod_lca.uncertainty.LogNorm

Bases: [`DataDistribution`](#pod_lca.uncertainty.DataDistribution)

A log-normal data distribution.

#### *classmethod* from_params(mean, std_dev, start, name='unspecified')

Create a log-normal distribution from parameters specified. Parameters specified are the mean and standard deviation of the corresponding normal distribution, and the starting point of the log-normal distribution.

* **Parameters:**
  * **mean** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Mean of the corresponding normal distribution, relative to start of the log-normal distribution.
  * **std_dev** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Standard deviation of the corresponding normal distribution.
  * **start** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Starting point of the log-normal distribution.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the data distribution.

### *class* pod_lca.uncertainty.ExponentDecay

Bases: [`DataDistribution`](#pod_lca.uncertainty.DataDistribution)

A exponential decay distribution.

#### *classmethod* from_params(start, decay_rate, name='unspecified')

Create a exponential distribution from parameters specified.

* **Parameters:**
  * **start** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Starting point of the exponential decay function.
  * **decay_rate** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Decay rate of the exponential function.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the data distribution.
