
from pandas import DataFrame
from pandas import concat, read_csv

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class DatabaseManager:
    """
    Database manager maintains the impact database.

    Attributes
    ----------
    impact_categories : dict.
        Dictionary {impact category (str): }.
    data : pandas DataFrame Obj.
        Impact data, with following headings.
            'Flow' (str) : name of impact
            'Unit' (str) : impacts per this unit of measure
            impact catergory (float) : quantity of impact
    """

    def __init__(self):
        self.impact_categories = {'GWP':0.0, 'acid_pot':0.0, 'eutro_pot':0.0, 'ozone_dep':0.0, 'smog':0.0}
        self.data = DataFrame(columns=['Flow','Unit'] + list(self.impact_categories.keys()))

    def __reduce__(self):
        
        return (self.__class__, (), {"data": self.data, 
                                         "impact_categories": self.impact_categories})
    
    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_data(self, data):
        """ Set the database data.
        
        Parameters
        ----------
        data : pandas DataFrame Obj.
            Impact data, with following headings.
                'Flow' (str) : name of impact
                'Unit' (str) : impacts per this unit of measure
                impact catergory (float) : quantity of impact
        """

        self.data = data

    def set_impact_categories(self, impact_cats):
        """ Change the names of impacts.
            This is only intended to be done at the begining of a project.

            Parameters
            ----------
            impact_cats : list of str
                New impact category names.
        """

        old_headers =  ['Flow','Unit'] + list(self.impact_categories.keys())
        self.impact_categories = dict.fromkeys(impact_cats, 0.0)

        new_headers = ['Flow','Unit'] + list(self.impact_categories.keys())
        header_map = dict(zip(old_headers, new_headers))
        self.data = self.data.rename(columns=header_map)

    def get_data(self):
        """ Retrieve impact data in the database.
        
            Returns
            -------
            Pandas DataFrame Obj.
                Impact data.
        """

        return self.data
    
    def get_impact_categories(self):
        """ Retrieve impact categories.
        
            Returns
            -------
            list of str
                Names of the impact categories.
        """

        return list(self.impact_categories.keys())  

    def get_impact_data(self, flow_name):
        """ Retrieve impacts for given flow.
        
            Parameters
            ----------
            flow_name : str
                Name of the flow
            
            Returns
            -------
            Pandas Series
                Databse entry corresponding to the flow.
        """

        if self.data is not None:
            row_id = self.data.index[self.data['Flow'] == flow_name][0]
            return self.data.iloc[row_id]

    # =================================
    # DATA IMPORT METHODS
    # =================================
    def import_data_from_CSV(self, file_path, headers=None, multipliers=None):
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
        
        default_headers = ['Flow','Unit'] + list(self.impact_categories.keys())
        if headers == None:
            headers = default_headers
        header_map = dict(zip(headers, default_headers))

        new_data = read_csv(filepath_or_buffer=file_path)
        new_data = new_data.rename(columns=header_map)

        if not multipliers == None:
            n = len(headers)
            for i in range(n):
                if i>1:
                    new_data[header_map[headers[i]]] = new_data[header_map[headers[i]]] * multipliers[i-2]

        if self.get_data().empty:
            self.set_data(new_data)
        else:
            self.set_data(concat([self.get_data(), new_data], ignore_index=True))

    def set_custom_entry(self, flow, unit, impacts):
        """ Add a custom entry the database.

            Parameters
            ----------
            flow : str
                Name of the impact.
            unit : str
                Unit of measurement for which the impacts are applied.
            impacts : dict
                Dictionary of impacts {impact catergory (str): impact (float)}

        """

        tmp_data = impacts
        tmp_data['Flow'] = flow
        tmp_data['Unit'] = unit

        self.data.loc[len(self.data)] = tmp_data
