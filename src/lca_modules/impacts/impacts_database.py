from lca_modules.impacts.units_map import UNITS_MAP
from utilities.data.transfer import DataHandler

from pandas import DataFrame
from pandas import concat


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class ImpactsDatabase:
    """
    Database manager maintains the impact database.

    Attributes
    ----------
    name : str
        Name of the database.
    impact_categories : dict
        Dictionary of impact categories and other data.
    data : pandas DataFrame Obj.
        Impact data, with following headings.
            'Flow' (str) : name of impact
            'Declared Unit' (str) : impacts per this unit of measure
            impact catergory (float) : quantity of impact
    """

    def __init__(self):
        self.name = None
        self.impact_ceteogries = None
        self.data = None

    def __str__(self):
        str = "="*75 + "\n" + f"Impact Database: {self.get_name()}\n" + "="*75 + "\n"
        str += f"{self.get_data_all()}"
        return str
    
    # =================================
    # Constructors
    # =================================
    @classmethod
    def new(cls, name, file_path):
        """ Create a new database.
        
        Parameters
        ----------
        name : str
            Name of the database.
        file_path : str
            Location of the impact categories json file.
        
        Returns
        -------
        ImpactsDatabase Obj.
            Database created.
        """

        new_db = cls()
        new_db.set_name(name)

        impact_categories = DataHandler.json_to_dict(file_path)

        new_db.set_impact_categories(impact_categories)
        new_db.data = DataFrame(columns=['Flow','Unit'] + new_db.get_impact_categories_names())

        return new_db

    # =================================
    # Getters and Setters
    # =================================
    def set_name(self, name):
        """ Set the name of the database.
        
        Parameters
        ----------
        name : str
            Name of the database.
        """

        self.name = name

        return self

    def set_data(self, file_path, headers=None, multipliers=None):
        """ Set the database data.
        
        Parameters
        ----------
        file_path : str
            Location of the CSV file
        headers : list of str
            The headers of the CSV file as they would be mapped to the database.
        multipliers : list of float
            Values of each column of the CSV will be multiplied by these values.
        """

        default_headers = ['Flow','Unit'] + list(self.get_impact_categories_names())
        if headers == None:
            headers = default_headers
        if multipliers == None:
            multipliers = [1.0] * len(headers)
        multipliers = [None, None] + multipliers

        data = DataHandler.csv_to_pandas(file_path, headers, multipliers)

        data.columns = default_headers
        data['Unit'] = data['Unit'].map(UNITS_MAP)

        if self.get_data_all().empty:
            self.data = data
        else:
            self.data = concat([self.get_data_all(), data], ignore_index=True)

        return self
    
    def set_impact_categories(self, impact_categories):
        """ Set the impact categories.
        
        Parameters
        ----------
        impact_categories : list
            List of impact categories.
        """

        self.impact_ceteogries = impact_categories

        return self

    def set_data_entry(self, flow, unit, impacts):
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

        if list(self.get_impact_categories_names()) + ['Flow', 'Unit'] == list(tmp_data.keys()) :
            self.data.loc[len(self.data)] = tmp_data
        else:
            raise KeyError(f"The impact cateogrized provided are incompatible with the database.\n Impact categories in database: {self.get_impact_categories_names()}")

        return self.data
    
    def get_name(self):
        """ Get the name of the database.
        
            Returns
            -------
            str
                Name of the database.
        """

        return self.name
    
    def get_impact_categories_names(self):
        """ Get the impact categories.
        
            Returns
            -------
            list of str
                List of impact categories.
        """

        return list(self.impact_ceteogries.keys())
    
    def get_impact_category_units(self):
        """ Get the units of the impact categories.
        
            Returns
            -------
            list of str
                List of units of the impact categories.
        """

        units = []
        for key, value in self.impact_ceteogries.items():
            units.append(value['refUnit'])

        return units
    
    def get_data_all(self):
        """ Retrieve impact data in the database.
        
            Returns
            -------
            Pandas DataFrame Obj.
                Impact data.
        """

        return self.data

    def get_data_entry(self, flow_name):
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

if __name__ == '__main__':
    pass