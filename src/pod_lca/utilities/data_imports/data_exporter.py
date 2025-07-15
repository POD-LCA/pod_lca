
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; mhtaba@uw.edu"
__version__ = "0.1.0"

import csv
import json


class DataExporter:

    # ========================
    # CSV
    # ========================
    def dict_to_csv(input_dict, file_path):
        """ Transfer data from a dictionary to a CSV file.
        
        Parameters
        ----------
        input_dict : dict
            A dictionary with the row as the value.
        file_path : str
            Location of the CSV file.
        """
        fieldnames = list(next(iter(input_dict.values())).keys())

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for data in input_dict.values():
                writer.writerow(data)

    def list_to_csv(input_list, file_path):
        """ Write data to a CSV file from a list of str.
        
        Parameters
        ----------
        input_list : list of str
            List of strings to be written to the CSV file. 
        file_path : str
            Location of the CSV file.
        """
        with open(file_path, "w", newline = "") as file:
            writer = csv.writer(file)
            writer.writerows(input_list)

    def lists_to_csv(input_lists, file_path, as_columns=False, headers=None):
        """ Write data to a CSV file from a list of str.
        
        Parameters
        ----------
        input_list : list of lists
            Lists to be written to the CSV file.
        file_path : str
            Location of the CSV file.
        as_columns : bool
            If true, each list will be written as a column.
        headers : list
            Data headers.
        """
        rows = list(zip(*input_lists)) if as_columns else input_lists

        with open(file_path, "w", newline = "") as file:
            writer = csv.writer(file)
            if headers is not None:
                writer.writerow(headers)
            writer.writerows(rows)

    # ========================
    # JSON
    # ========================    
    def dict_to_json(input_dict, file_path):
        """ Transfer data from a dictionary to a JSON file.
        
        Parameters
        ----------
        input_dict : dict
            A dictionary with the UUID as the key and the row as the value.
        file_path : str
            Location of the JSON file.
        """
        with open(file_path, "w") as file:
            json.dump(input_dict, file)


if __name__ == '__main__':
    pass
