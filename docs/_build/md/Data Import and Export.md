# Data Import and Export

[`DataImporter`](#pod_lca.utilities.DataImporter) and [`DataExporter`](#pod_lca.utilities.DataExporter) class manage importing and exporting data from and to CSv and JSON files.

---

### *class* pod_lca.utilities.DataImporter

#### csv_to_pandas(headers=None, multipliers=None)

Import data to database from a CSV file.

* **Parameters:**
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the CSV file
  * **headers** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- The headers of the CSV file as they would be mapped to the dataset.
  * **multipliers** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*float*](https://docs.python.org/3/library/functions.html#float)) -- Values of each column of the CSV will be multiplied by these values.

#### csv_to_dict(primary_key=None)

Import data to dictionary from a CSV file.

* **Parameters:**
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the CSV
  * **primary_key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- The column name that will be used as the primary key in the dictionary.
* **Returns:**
  A dictionary with the UUID as the key and the row as the
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### csv_to_list(column_header=None)

Import data to list from a CSV file. The first row of the CSV file is used as the header. Only one column identified by the column header is imported. If the column header is not provided, the first column of the CSV file is imported.

* **Parameters:**
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the CSV file.
  * **column_header** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Header of the column from where the data to be read to the list, when the file has headers.
* **Returns:**
  A list of data.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)

#### *static* json_to_dict(file_path)

Import data to dictionary from a JSON file.

* **Parameters:**
  **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the JSON file.
* **Returns:**
  A dictionary with the UUID as the key and the row as the value.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

### *class* pod_lca.utilities.DataExporter

#### dict_to_csv(file_path, append=False)

Transfer data from a dictionary to a CSV file.

* **Parameters:**
  * **input_dict** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- A dictionary with the column header as key and row as the value.
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the CSV file.
  * **append** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, append to the file, otherwise overwrite.

#### list_to_csv(file_path, append=False)

Write data to a CSV file from a list of str.

* **Parameters:**
  * **input_list** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- List of strings to be written to the CSV file.
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the CSV file.
  * **append** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, append to the file, otherwise overwrite.

#### lists_to_csv(file_path, as_columns=False, headers=None)

Write data to a CSV file from a list of str.

* **Parameters:**
  * **input_list** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- Lists to be written to the CSV file.
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the CSV file.
  * **as_columns** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, each list will be written as a column.
  * **headers** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- Data headers.

#### csv_has_headers()

Check if CSV file has data in it.

* **Parameters:**
  **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the CSV file.
* **Returns:**
  True, if the file already has data: false,  otherwise.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### dict_to_json(file_path)

Transfer data from a dictionary to a JSON file.

* **Parameters:**
  * **input_dict** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- A dictionary with the column header as key and row as the value.
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Location of the JSON file.
