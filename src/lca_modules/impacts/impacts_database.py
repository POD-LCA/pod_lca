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
        self.primary_key = 'Flow'
        self.unit_key = 'Unit'
        self.qty_key = 'Qty'
        self.data = DataFrame(columns=[self.get_primary_key(), self.get_unit_key()] + list(IMPACT_CATEGOREIS.keys()))

    def __str__(self):
        str = "="*75 + "\n" + f"Impact Database: {self.get_name()}\n" + "="*75 + "\n"
        str += f"{self.get_data_all()}"
        return str
    
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

    def set_data(self, file_path, impact_headers=None, additional_headers=None, multipliers=None):
        """ Set the database data.
        
        Parameters
        ----------
        file_path : str
            Location of the CSV file
        impact_headers : list of str
            The headers of the CSV file as they would be mapped to the database.
        additional_headers : list of str
            Headers of the columns to be imported, other than name, unit, and impact categories.
        multipliers : list of float
            Values of each column of the CSV will be multiplied by these values.
        """

        if impact_headers == None:
            impact_headers = list(IMPACT_CATEGOREIS.keys())
        data_headers = [self.get_primary_key(), self.get_qty_key(), self.get_unit_key()] +  impact_headers
        if not (additional_headers ==  None):
            data_headers = data_headers + additional_headers
        
        no_headers = len(data_headers)

        if multipliers == None:
            multipliers = [1.0] * len(impact_headers)

        multipliers = [None, None, None] + multipliers + [None] * (no_headers - 3 - len(multipliers))

        data = CSV_Importer.import_as_pandas(file_path, data_headers, multipliers)

        data[self.get_unit_key()] = data[self.get_unit_key()].map(UNITS_MAP)

        # loading data to existing dataset
        if self.get_data_all().empty:
            self.data = data
        else:
            self.data = concat([self.get_data_all(), data], ignore_index=True)

        return self

    def set_data_entry(self, flow, qty, unit, impacts, add_data=None):
        """ Add a custom entry the database.

            Parameters
            ----------
            flow : str
                Name of the impact.
            qty : float
                Quantity of the flow.
            unit : str
                Unit of measurement for which the impacts are applied.
            impacts : dict
                Dictionary of impacts {impact catergory (str): impact (float)}
            add_data : dict
                Dictionary of additional data {header (str): value (str / float/ int)}

        """

        tmp_data = impacts
        tmp_data[self.get_primary_key()] = flow
        tmp_data[self.get_qty_key()] = qty
        tmp_data[self.get_unit_key()] = unit

        if list(IMPACT_CATEGOREIS.keys()) + [self.get_primary_key(), self.get_qty_key(), self.get_unit_key()] == list(tmp_data.keys()) :
            self.data.loc[len(self.data)] = tmp_data
        else:
            raise KeyError(f"The impact cateogrized provided are incompatible with the database.\n Impact categories in database: {IMPACT_CATEGOREIS.keys()}")

        # TODO: check if the additional headers exist/ if not create them and add the new data

        return self.data

    def set_primary_key(self, key):

        self.primary_key = key

        return self
    
    def set_unit_key(self, key):

        self.unit_key = key

        return self
    
    def set_qty_key(self, key):

        self.qty_key = key

        return self
        
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
            row_id = self.data.index[self.data[self.get_primary_key()] == flow_name]
            if len(row_id) == 1:
                return self.data.iloc[row_id[0]]
            else:
                raise ImportError("Multiple matching entries exist...")

    def get_primary_key(self):

        return self.primary_key
    
    def get_unit_key(self):

        return self.unit_key
    
    def get_qty_key(self):

        return self.qty_key
    
class EOLImpactsDatabase(ImpactsDatabase):

    def __init__(self):
        super().__init__()
        self.process_key = 'Process'

    def set_data(self, file_path, impact_headers=None, additional_headers=None, multipliers=None):
        """ Set the database data.
        
        Parameters
        ----------
        file_path : str
            Location of the CSV file
        impact_headers : list of str
            The headers of the CSV file as they would be mapped to the database.
        additional_headers : list of str
            Headers of the columns to be imported, other than name, unit, and impact categories.
        multipliers : list of float
            Values of each column of the CSV will be multiplied by these values.
        """

        if impact_headers == None:
            impact_headers = list(IMPACT_CATEGOREIS.keys())
        data_headers = [self.get_primary_key(), self.get_qty_key(), self.get_unit_key(), self.get_process_key()] +  impact_headers
        if not (additional_headers ==  None):
            data_headers = data_headers + additional_headers
        
        no_headers = len(data_headers)

        if multipliers == None:
            multipliers = [1.0] * len(impact_headers)

        multipliers = [None] * 4 + multipliers + [None] * (no_headers - 4 - len(multipliers))

        data = CSV_Importer.import_as_pandas(file_path, data_headers, multipliers)

        data[self.get_unit_key()] = data[self.get_unit_key()].map(UNITS_MAP)

        # loading data to existing dataset
        if self.get_data_all().empty:
            self.data = data
        else:
            self.data = concat([self.get_data_all(), data], ignore_index=True)

        return self

    def set_data_entry(self, flow, qty, unit, process, impacts, add_data=None):
        """ Add a custom entry the database.

            Parameters
            ----------
            flow : str
                Name of the impact.
            qty : float
                Quantity of the flow.
            unit : str
                Unit of measurement for which the impacts are applied.
            process : str
                End-of-Life process.
            impacts : dict
                Dictionary of impacts {impact catergory (str): impact (float)}
            add_data : dict
                Dictionary of additional data {header (str): value (str / float/ int)}

        """

        tmp_data = impacts
        tmp_data[self.get_primary_key()] = flow
        tmp_data[self.get_qty_key()] = qty
        tmp_data[self.get_unit_key()] = unit
        tmp_data[self.get_process_key()] = process

        if list(IMPACT_CATEGOREIS.keys()) + [self.get_primary_key(), self.get_qty_key(), self.get_unit_key(), self.get_process_key()] == list(tmp_data.keys()) :
            self.data.loc[len(self.data)] = tmp_data
        else:
            raise KeyError(f"The impact cateogrized provided are incompatible with the database.\n Impact categories in database: {IMPACT_CATEGOREIS.keys()}")

        # TODO: check if the additional headers exist/ if not create them and add the new data

        return self.data

    def set_process_key(self, key):

        self.process_key = key

        return self

    def get_data_entry(self, material_name, process_name):
        """ Retrieve impacts for given flow.
        
            Parameters
            ----------
            material_name : str
                Name of the material
            process_name: str
                End-of-Life process name.
            
            Returns
            -------
            Pandas Series
                Databse entry corresponding to the flow.
        """

        if self.data is not None:
            row_id = self.data.index[(self.data[self.get_primary_key()] == material_name) & (self.data[self.get_process_key()] == process_name)]
            if len(row_id) == 1:
                return self.data.iloc[row_id[0]]
            else:
                raise ImportError("Multiple matching entries exist...")
            
    def get_process_key(self):

        return self.process_key

if __name__ == '__main__':
    pass