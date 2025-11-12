
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; mhtaba@uw.edu"
__version__ = "0.1.0"

import csv
import json

from pandas import read_csv


class DataImporter:
  
    # ========================
    # CSV
    # ========================
    def csv_to_pandas(file_path, headers=None, multipliers=None):
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
        df_headers = read_csv(file_path, nrows=0)
        if headers is None:
            headers_present = df_headers.columns.tolist()
        else:
            headers_present = [col for col in headers if col in df_headers.columns.tolist()]

        data_frame = read_csv(filepath_or_buffer=file_path, usecols=headers_present)

        if not multipliers == None:
            n = len(headers)
            for i in range(n):
                if multipliers[i] is not None and headers[i] in headers_present:
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
        with open(file_path, mode='r', encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row[primary_key]
                data[id] = {key: value for key, value in row.items()} 

        return data

    def csv_to_list(file_path, column_header=None):
        """ Import data to list from a CSV file. The first row of the CSV file is used as the header. Only one column identified by the column header is imported. If the column header is not provided, the first column of the CSV file is imported.
        
        Parameters
        ----------
        file_path : str
            Location of the CSV file.
        column_header : str
            Header of the column from where the data to be read to the list, when the file has headers.
        
        Returns
        -------
        list 
            A list of data.
        """
        data = []
        column_index = 0 if column_header is None else None
        current_row = 0
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            if not (column_header is None):
                headers = next(reader, None)
                column_index = headers.index(column_header)
            for row in reader:
                data.append(row[column_index])

                current_row += 1

        return data

    # ========================
    # JSON
    # ========================    
    @staticmethod
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


if __name__ == '__main__':

    # Example usage
    file_path = "data/transportation_dataset/transportation_faf_domestic-region.json"
    data = DataImporter.json_to_dict(file_path)
    print(data)
