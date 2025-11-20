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
    def dict_to_csv(input_dict, file_path, append=False):
        """Transfer data from a dictionary to a CSV file.

        Parameters
        ----------
        input_dict : dict
            A dictionary with the column header as key and row as the value.
        file_path : str
            Location of the CSV file.
        append : bool
            If true, append to the file, otherwise overwrite.
        """
        fieldnames = list(next(iter(input_dict.values())).keys())
        mode = "a" if append else "w"

        ignore_header = True if append and DataExporter.csv_has_headers(file_path) else False

        with open(file_path, mode, newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not ignore_header:
                writer.writeheader()
            for data in input_dict.values():
                writer.writerow(data)

    def list_to_csv(input_list, file_path, append=False):
        """Write data to a CSV file from a list of str.

        Parameters
        ----------
        input_list : list of str
            List of strings to be written to the CSV file.
        file_path : str
            Location of the CSV file.
        append : bool
            If true, append to the file, otherwise overwrite.
        """
        mode = "a" if append else "w"
        with open(file_path, mode, newline="") as file:
            writer = csv.writer(file)
            writer.writerows(input_list)

    def lists_to_csv(input_lists, file_path, as_columns=False, headers=None):
        """Write data to a CSV file from a list of str.

        Parameters
        ----------
        input_list : list of list
            Lists to be written to the CSV file.
        file_path : str
            Location of the CSV file.
        as_columns : bool
            If true, each list will be written as a column.
        headers : list
            Data headers.
        """
        rows = list(zip(*input_lists)) if as_columns else input_lists

        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            if headers is not None:
                writer.writerow(headers)
            writer.writerows(rows)

    def csv_has_headers(file_path):
        """ Check if CSV file has data in it.
        
        Parameters
        ----------
        file_path : str
            Location of the CSV file.

        Returns
        -------
        bool
            True, if the file already has data: false,  otherwise.      
        """ 
        try:
            with open(file_path, 'r', newline='') as csvfile:
                sample = csvfile.read(2048) # read a large enough chunk to capture headers
                if not sample:
                    return False
                
                has_header = csv.Sniffer().has_header(sample)
                return has_header
            
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return False
        except csv.Error:
            return False
    
    # ========================
    # JSON
    # ========================
    def dict_to_json(input_dict, file_path):
        """Transfer data from a dictionary to a JSON file.

        Parameters
        ----------
        input_dict : dict
            A dictionary with the column header as key and row as the value.
        file_path : str
            Location of the JSON file.
        """
        with open(file_path, "w") as file:
            json.dump(input_dict, file)


if __name__ == "__main__":
    pass
