# Mathematical Functions

[`MathFuncs`](#pod_lca.utilities.MathFuncs) class is a collection of mathematical functions.

---

### *class* pod_lca.utilities.MathFuncs

#### *static* round_to_significant(values, sig_figs=3)

Round a list of numbers to the given number of significant figures.

* **Parameters:**
  * **values** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Numbers to be rounded off.
  * **sig_fig** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Number of significant digits.

#### *static* integrate_exp(a, b, coeff=1.0, pow_coeff=1.0)

Evaluate the integral of (coeff) \* e \*\* (pow_coeff \* x), from a to b, with respect to x.

* **Parameters:**
  * **a** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Start of integral evaluation.
  * **b** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- End of integral evaluation.
  * **coeff** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Coeffecient on the exponent.
  * **pow_coeff** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Power of the exponent.
