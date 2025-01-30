
from pandas import read_csv
import csv
import json


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; mhtaba@uw.edu"
__version__ = "0.1.0"


class DataHandler:

    def csv_to_pandas(file_path, headers=None, multipliers=None):
        """ Import data to database from a CSV file.
        
            Parameters
            ----------
            file_path : str
                Location of the CSV file
            headers : list of str
                The headers of the CSV file as they would be mapped to the database.
            multipliers : list of float
                Values of each column of the CSV will be multiplied by these values.
        """
        
        data_frame = read_csv(filepath_or_buffer=file_path, usecols=headers)

        if not multipliers == None:
            n = len(headers)
            for i in range(n):
                if multipliers[i] is not None:
                    data_frame[headers[i]] *= multipliers[i]

        return data_frame
    
    def csv_to_dict(file_path, primary_key):
        """ Import data to dictionary from a CSV file.
        
            Parameters
            ----------
            file_path : str
                Location of the CSV
            primary_key : str
                The column name that will be used as the primary key in the dictionary.
            
            Returns
            -------
            dict
                A dictionary with the UUID as the key and the row as the
        """

        data = {}
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row[primary_key]
                data[id] = {key: value for key, value in row.items()} 

        return data
    
    def dict_to_csv(input_dict, file_path):
        """ Transfer data from a dictionary to a CSV file.
        
            Parameters
            ----------
            input_dict : dict
                A dictionary with the UUID as the key and the row as the value.
            file_path : str
                Location of the CSV file.
        """

        fieldnames = list(next(iter(input_dict.values())).keys())

        with open(file_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for data in input_dict.values():
                writer.writerow(data)


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

    def json_to_dict(file_path):
        """ Import data to dictionary from a JSON file.
        
            Parameters
            ----------
            file_path : str
                Location of the JSON file.
            
            Returns
            -------
            dict
                A dictionary with the UUID as the key and the row as the value.
        """

        with open(file_path, "r") as file:
            data = json.load(file)

        return data
    