# Object Array Methods

[`ArrayMethods`](#pod_lca.utilities.ArrayMethods) class is a collection of methods to retrieve/manage object attributes with lists/arrays of values.

---

### *class* pod_lca.utilities.ArrayMethods

#### *static* get_attribute_as_list(objects, attr_name)

Get a specified attribute from objects in a list, and returns the attribute entries in a list.

* **Parameters:**
  * **objects** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*object*](https://docs.python.org/3/library/functions.html#object)) -- List of objects.
  * **attr_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Attribute to be retrieved in a list.
* **Returns:**
  List of the attribute entries
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)

#### *static* sort_by_attribute(objects, attr_name, descending=True)

Sort a list of objects by a specified attribute value.

* **Parameters:**
  * **objects** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*object*](https://docs.python.org/3/library/functions.html#object)) -- List of objects.
  * **attr_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Attribute to be retrieved in a list.
  * **descending** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, the list is ordered in the descending order of the attribute value.
* **Returns:**
  List of the attribute entries
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)

#### *static* set_value(objects, attr_name, value)

Sort a list of objects by a specified attribute value.

* **Parameters:**
  * **objects** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*object*](https://docs.python.org/3/library/functions.html#object)) -- List of objects.
  * **attr_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Attribute to be retrieved in a list.
  * **value** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* [*int*](https://docs.python.org/3/library/functions.html#int) *or* [*float*](https://docs.python.org/3/library/functions.html#float) *or* [*bool*](https://docs.python.org/3/library/functions.html#bool)) -- Value to be given to the attribute.
