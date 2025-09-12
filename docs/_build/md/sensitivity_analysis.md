# Sensitivity Analysis

[`SensitivityAnalysis`](#pod_lca.uncertainty.SensitivityAnalysis) object contains methods for the calculation of sensitivity of LCA output to changes in parameters in [`Product`](products.md#pod_lca.materials_screening.Product) objects.

---

### *class* pod_lca.uncertainty.SensitivityAnalysis

#### compute_sensitivity_of_param(param, impact_cat='weighted', sensitivity_type='relative', printout=True, \*\*kwargs)

Compute the sensitivity of a parameter of an object.

* **Parameters:**
  * **obj** ([*Master*](products.md#pod_lca.materials_screening.Master)) -- Entry on which the sensitivity is tested.
  * **param** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Parameter varied. This must be an attribute of the object.
  * **impact_cat** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Impact category considered.  Weighted impact, if 'weighted'
  * **sensitivity_type** ( *{'relative'* *,*  *'symmetric'}*) -- 

    Type of sensitivity analysis.
    - 'relative' - relative percentage change of impact.
    - 'symmetric' - symmetric percentage change of impact.

    Default is 'relative'.
  * **printout** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- Printout results if true. Default is True
  * **\*\*kwargs** -- 
    - range - [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple)
      : Minimum and maximum value for the parameter.
        e.g., qty of a product or process.
    - options - [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`str`](https://docs.python.org/3/library/stdtypes.html#str)
      : A range of options given as strings for the parameter.
        e.g., database_item name (i.e., to change the impact value)
* **Returns:**
  Minimum and maximum percentage change of impact.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)
* **Raises:**
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Range of parameter does not include base value.
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Invalid sensitivity type.
  * [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- Keyword arguments not recognized.

#### compute_sensitivity_of_params(groups, impact_cat='weighted', printout=True)

Compute the sensitivity of a parameters of multiple objects.
: Sensitivity is computed with all effects in combination.

* **Parameters:**
  * **model** ([*Model*](model.md#pod_lca.materials_screening.Model)) -- Model in which the sensitivity is considered.
  * **groups** (*List* *of* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- 

    [{**'obj'**: [`Master`](products.md#pod_lca.materials_screening.Master), **'param'**: [`str`](https://docs.python.org/3/library/stdtypes.html#str), **'range'**: [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple)},
    {**'obj'**: [`Master`](products.md#pod_lca.materials_screening.Master),\*\*'param'**: :class:\`str\`, \*\*'options'**: [`list`](https://docs.python.org/3/library/stdtypes.html#list) of [`str`](https://docs.python.org/3/library/stdtypes.html#str)},
    ...
    ]
    where;
    > - obj - [`Master`](products.md#pod_lca.materials_screening.Master)
    >   : Entry on which the sensitivity is tested.
    > - param - [`str`](https://docs.python.org/3/library/stdtypes.html#str)
    >   : Parameter varied. This must be an attribute of the object.
    > - range - tuple
    >   : Minimum and maximum value for the parameter, in that order.e.g., qty of a product or process.
    > - options - list of str
    >   : A range of options given as strings for the parameter. e.g., database_item name (i.e., to change the impact value)
* **Returns:**
  Minimum and maximum percentage change of impact.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)
* **Raises:**
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Range of parameter does not include base value.
  * [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) -- Keyword arguments not recognized.
