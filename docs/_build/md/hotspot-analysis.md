# Hotspot Analysis

[`HotSpotAnalysis`](#pod_lca.uncertainty.HotSpotAnalysis) object carries out the hotspot analysis for a model and would return hotspot entries: [`get_hotspots_by_impact_category()`](#pod_lca.uncertainty.HotSpotAnalysis.get_hotspots_by_impact_category).

---

### *class* pod_lca.uncertainty.HotSpotAnalysis

HotSpotAnalysis object carries out hotspot analysis and stores data.

#### model

Model on which the hotspot analysis is performed.

* **Type:**
  [*Model*](model.md#pod_lca.materials_screening.Model)

#### hotspots

{**impact_category** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`Master`](products-and-processes.md#pod_lca.materials_screening.Master)}.

* **Type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict) of [list](https://docs.python.org/3/library/stdtypes.html#list)

#### *classmethod* from_model(model)

Create a hotspot analyis from a a model.

* **Parameters:**
  **model** ([*Model*](model.md#pod_lca.materials_screening.Model)) -- Model on which the hotspot analysis is performed.

#### set_model(model)

Set a model to the analyser.

* **Parameters:**
  **model** ([*Model*](model.md#pod_lca.materials_screening.Model)) -- Model on which the hotspot analysis is performed.

#### set_hotspots(hotspots, impact_category)

Set attribute in hotspots to identify as hotspots.

* **Parameters:**
  * **hotspots** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*Master*](products-and-processes.md#pod_lca.materials_screening.Master)) -- List of hotspot object of the model.
  * **impact_category** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Impact category for which the hotspot analysis was run.

#### get_model()

Get the model for which the analsysis will be run.

* **Returns:**
  Model on which the hotspot analysis is performed.
* **Return type:**
  [*Model*](model.md#pod_lca.materials_screening.Model)

#### get_hotspots()

Get hotspots of the model.

* **Returns:**
  {**impact_category** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`Master`](products-and-processes.md#pod_lca.materials_screening.Master)}
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### get_hotspots_by_impact_category(impact_category)

Get hotspots of the model, by the impact category.

* **Parameters:**
  **impact_category** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Impact category.
* **Returns:**
  List of hotspot object of the model.None if hotspots are not set.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Master*](products-and-processes.md#pod_lca.materials_screening.Master)

#### run(impact_category='GWP')

Determines the hotspot of the model.
: The hotspots are the largest group out of
  <br/>
  - top 20% contributors to the impact or
  - the smallest group of contributors to the 80% (or more) of the impact category specified.

* **Parameters:**
  * **model** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the model considered.
  * **impact_category** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Impact category considered.
* **Returns:**
  Hotspot objects.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) of [*Master*](products-and-processes.md#pod_lca.materials_screening.Master)
