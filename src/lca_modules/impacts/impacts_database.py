from lca_modules.impacts.impact_categories import IMPACT_CATEGOREIS
from lca_modules.impacts.units_map import UNITS_MAP
from utilities.data_imports.csv import CSV_Importer

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
    data : pandas DataFrame Obj.
        Impact data, with following headings.
            'Flow' (str) : name of impact
            'Declared Unit' (str) : impacts per this unit of measure
            impact catergory (float) : quantity of impact
    """

    def __init__(self):
        self.name = None
        self.data = DataFrame(columns=['Flow','Unit'] + list(IMPACT_CATEGOREIS.keys()))

    # =================================
    # Constructors
    # =================================

    @classmethod
    def new(cls, name):
        """ Create a new database.
        
        Parameters
        ----------
        name : str
            Name of the database.
        
        Returns
        -------
        ImpactsDatabase Obj.
            Database created.
        """

        new_db = cls()
        new_db.set_name(name)

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

        default_headers = ['Flow','Unit'] + list(IMPACT_CATEGOREIS.keys())
        if headers == None:
            headers = default_headers
        if multipliers == None:
            multipliers = [1.0] * len(headers)
        multipliers = [None, None] + multipliers

        data = CSV_Importer.import_as_pandas(file_path, headers, multipliers)

        data.columns = default_headers
        data['Unit'] = data['Unit'].map(UNITS_MAP)

        if self.get_data_all().empty:
            self.data = data
        else:
            self.data = concat([self.get_data_all(), data], ignore_index=True)

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

        if list(IMPACT_CATEGOREIS.keys()) + ['Flow', 'Unit'] == list(tmp_data.keys()) :
            self.data.loc[len(self.data)] = tmp_data
        else:
            raise KeyError(f"The impact cateogrized provided are incompatible with the database.\n Impact categories in database: {IMPACT_CATEGOREIS.keys()}")

        return self.data
    
    def get_name(self):
        """ Get the name of the database.
        
        Returns
        -------
        str
            Name of the database.
        """

        return self.name
    
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