
import csv
import json
from pandas import read_csv


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; mhtaba@uw.edu"
__version__ = "0.1.0"


class CSV_Importer:

    def import_as_pandas(file_path, headers=None, multipliers=None):
        """ Import data to database from a CSV file.
        
            Parameters
            ----------
            file_path : str
                Location of the CSV file
            headers : list of str
                The headers of the CSV file as they would be mapped to the dataset.
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

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for data in input_dict.values():
                writer.writerow(data)

    def csv_to_list(file_path, column_header=None):
        """ Import data to list from a CSV file. The first row of the CSV file is used as the header. Only one column identified by the column header is imported. If the column header is not provided, the first column of the CSV file is imported.
        
            Parameters
            ----------
            file_path : str
                Location of the CSV file.
            
            Returns
            -------
            list 
                A list of data.
        """

        data = []
        column_id = 0 if column_header is None else None
        current_row = 0
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if current_row ==0 and column_id:
                    column_id = row.index(column_header)
                
                if current_row >0:
                    data.append(row[column_id])

                current_row += 1

        return data

if __name__ == '__main__':
    pass
