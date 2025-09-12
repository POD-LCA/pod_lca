# Data Quality Assessment

[`PedigreeScore`](#pod_lca.uncertainty.PedigreeScore) objects are assigned to each [`Product`](products-and-processes.md#pod_lca.materials_screening.Product) object and can be accessed from [`get_pedigree_score()`](products-and-processes.md#pod_lca.materials_screening.Master.get_pedigree_score).

[`DataQualityAnalysis`](#pod_lca.uncertainty.DataQualityAnalysis) object carries out the data quality assesment for a model and would return data quality scores: [`get_model_DQS()`](#pod_lca.uncertainty.DataQualityAnalysis.get_model_DQS) and [`get_normalised_DQS()`](#pod_lca.uncertainty.DataQualityAnalysis.get_normalised_DQS).

---

### *class* pod_lca.uncertainty.PedigreeScore

PedigreeScore object contains background data for data quality scores.

#### parent

Product/Process object for which the data quality is related.

* **Type:**
  [*Master*](products-and-processes.md#pod_lca.materials_screening.Master)

#### DQS

Data quality score of the object.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

### <indicators>

Data Quality Indicators are dynamically set based on the Data Quality Analysis (DQA) used.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### *classmethod* from_parent(parent)

Create pedigree score object from parent.

* **Parameters:**
  **parent** ([*Master*](products-and-processes.md#pod_lca.materials_screening.Master)) -- Parent object.

#### set_parent(obj)

Set parent of the pedigree score.

* **Parameters:**
  **obj** ([*Master*](products-and-processes.md#pod_lca.materials_screening.Master)) -- Object to which the pedigree score correspond.

#### set_DQS()

Calculate and set the Data Quality Score of the pedigree score object.

* **Returns:**
  Data Quality Score.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_parent()

Get parent of the pedigree score.

* **Returns:**
  Object to which the pedigree score correspond.
* **Return type:**
  [*Master*](products-and-processes.md#pod_lca.materials_screening.Master)

#### get_DQS()

Get the Data Quality Score of the object.

* **Returns:**
  Data quality score of the object.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### update_pedigree_scores(\*args)

Update the pedigree score.

* **Parameters:**
  **\*args** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *or* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- An (**indicator** [`str`](https://docs.python.org/3/library/stdtypes.html#str), **score** [`float`](https://docs.python.org/3/library/functions.html#float)) pair or a dictionary of indicator-score pairs.
* **Raises:**
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- The scores are not within the score ranges specified.
  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- The scores are not in expected format.
  * [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- Indicator not recognized

### *class* pod_lca.uncertainty.DataQualityAnalysis

DataQualityAnalysis object carries out data quality analysis and stores pedigree data.

#### model

Model on which the hotspot analysis is performed.

* **Type:**
  [*Model*](model.md#pod_lca.materials_screening.Model)

#### DQS

Data Quality Score of the model.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### normalised_DQS

Normalised Data Quality Score of the model

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### *classmethod* from_model(model)

Create a data quality analysis for a model.

* **Parameters:**
  **model** ([*Model*](model.md#pod_lca.materials_screening.Model)) -- Model for whcih the analysis is created.

#### set_model(model)

Set a model to the Analyser.

* **Parameters:**
  **model** ([*Model*](model.md#pod_lca.materials_screening.Model)) -- Model on which the Data Quality Analysis is performed.

#### get_model()

Get the model for which the analysis will be run.

* **Returns:**
  Model on which the Data Quality Analysis is performed.
* **Return type:**
  [*Model*](model.md#pod_lca.materials_screening.Model)

#### get_model_DQS(impact_cat='GWP')

Get Data Quality Score of the model.

* **Parameters:**
  **impact_cat** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Impact category considered for weighing individual pedigree scores.
* **Returns:**
  Data Quality Score.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_normalised_DQS(impact_cat='GWP')

Get the normalised Data Quality Score of the model.

* **Parameters:**
  **impact_cat** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Impact category considered for weighing individual pedigree scores.
* **Returns:**
  Normalised Data Quality Score.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### set_pedigree_scores()

Set pedigree scores for all products/processes in a model.

#### set_temporal_correlation_scores()

Update all Temporal Correlation scores.

#### set_geographical_correlation_scores()

Update all Temporal Correlation scores.
