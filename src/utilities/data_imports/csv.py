
from lca_modules.impacts.impact_categories import IMPACT_CATEGOREIS

from pandas import read_csv

class CSV_Importer:

    def import_as_pandas(file_path, headers=None, multipliers=None):
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
