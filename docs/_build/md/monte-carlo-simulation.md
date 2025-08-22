# Monte Carlo Simulation

[`MonteCarloSimulator`](#pod_lca.uncertainty.MonteCarloSimulator) object facilitates runing of Monte Carlo Simulations on the materials screening or Building model.

---

### *class* pod_lca.uncertainty.MonteCarloSimulator

MonteCarloSimulation object carries out Monte Carlo Simulation.

#### model

Model on which the Monte Carlo Simulation is performed.

* **Type:**
  [*Model*](model.md#pod_lca.materials_screening.Model)

#### iterations

No of iterations.

* **Type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### impact_cat

Impact category considered for the impact calculation.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### var_param

List of Distribution objects.

* **Type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*DataDistribution*](data-distributions.md#pod_lca.uncertainty.DataDistribution)

#### scenario

Dictionary of objects and the scenario set to them; {**object** ([`Master`](products-and-processes.md#pod_lca.materials_screening.Master)): **scenario** ([`str`](https://docs.python.org/3/library/stdtypes.html#str))}.
Scenario values are 'low', 'med', and 'high'.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### run_time

CPU time of the simulation.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### result

Data from the Monte Carlo Simulation

* **Type:**
  [*MonteCarloResults*](#pod_lca.uncertainty.MonteCarloResults)

#### *classmethod* from_model(model, no_iter=10000, impact_cat='GWP')

Create a Monte Carlo Simulator for a model.

* **Parameters:**
  **model** ([*Model*](model.md#pod_lca.materials_screening.Model)) -- Model on which the Monte Carlo Simulation is performed.
* **Returns:**
  Simulator object.
* **Return type:**
  [*MonteCarloSimulator*](#pod_lca.uncertainty.MonteCarloSimulator)

#### set_model(model)

Set a model to the Simulator.

* **Parameters:**
  **model** ([*Model*](model.md#pod_lca.materials_screening.Model)) -- Model on which the Monte Carlo Simulation is performed.

#### set_iterations(no_iters)

Set the number of iterations of the simulation.

* **Parameters:**
  **no_iters** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Number of iterations of the simulations.

#### set_impact_cat(impact_cat)

Set the impact category considered for the simulation.

* **Parameters:**
  **impact_cat** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Impact category considered for the impact calculation.

#### set_var_params(params=None, set_all=True)

Find and set the variable parameters within the model.

* **Parameters:**
  * **params** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of distributions to be considered in the MCS.
  * **set_all** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, set all the parameters in the model with a distribution.
* **Raises:**
  [**NotImplementedError**](https://docs.python.org/3/library/exceptions.html#NotImplementedError) -- No parameters set to vary.

#### set_scenario(dict)

Set scenarios for a simulation.

* **Parameters:**
  **scenario** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- Dictionary of objects and the scenario set to them; {**object** ([`Master`](products-and-processes.md#pod_lca.materials_screening.Master)): **scenario** ([`str`](https://docs.python.org/3/library/stdtypes.html#str))}.
  Scenario values are 'low', 'med', and 'high'.

#### set_result(results, is_cts)

Sets the results of the Monte Carlo Simulation.

* **Parameters:**
  * **results** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*float*](https://docs.python.org/3/library/functions.html#float)) -- A list of impact data from each iteration of the simulation.
  * **is_cts** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- True, if the results are in a continous scale.

#### get_model()

Get the model for which the simulation will be run.

* **Returns:**
  Model on which the Monte Carlo Simulation is performed.
* **Return type:**
  [*Model*](model.md#pod_lca.materials_screening.Model)

#### get_iterations()

Get the number of iterations of the simulation.

* **Returns:**
  Number of iterations of the simulations.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_impact_cat()

Get the impact category considered for the simulation.

* **Returns:**
  Impact category considered for the impact calculation.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_var_params()

Get variable parameters within the model.

#### get_scenario()

Get scenarios set for the simulation.

* **Returns:**
  Dictionary of objects and the scenario set to them; {**object** ([`Master`](products-and-processes.md#pod_lca.materials_screening.Master)): **scenario** ([`str`](https://docs.python.org/3/library/stdtypes.html#str))}.
  Scenario values are 'low', 'med', and 'high'.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### get_result()

Sets the results of the Monte Carlo Simulation.

* **Returns:**
  Data from the Monte Carlo Simulation.
* **Return type:**
  [*MonteCarloResults*](#pod_lca.uncertainty.MonteCarloResults)

#### run()

Run a Monte Carlo Simulation.

#### update_all_distributions()

Set distribution objects to all data objects in the project objects with dataset.

### *class* pod_lca.uncertainty.MonteCarloResults

Bases: [`DataDistribution`](data-distributions.md#pod_lca.uncertainty.DataDistribution)
