
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pandas import concat

from ...units import UNITS_MAP
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class ImpactsDatabase:
    """ Database manager maintains the impact database.

    Attributes
    ----------
    name : str
        Name of the database.
    primary_key : str
        Primary key organizing the database.
    unit_key : str
        Data header corresponding to the units of the database entries.
    qty_key : str
        Data header corresponding to the quantity of the database entries.
    data : pandas.DataFrame
        Impact data, with following headings;
        - **primary_key** (:class:`str`): Name of the impact.
        - **qty_key** (:class:`str`): Impacts per unit of measure.
        - **unit_key** (:class:`str`): The unit of measure.
        - **impact category** (:class:`float`): Quantity of impact.
    """

    DATA_IMPORTS = {    
                        'impacts': config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES'],
                        'emissions': config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES'],
                        'carbon_storage': config['setup']['INVENTORY_ITEMS']['CARBON_STORAGE'],
                    }
    
    def __init__(self):
        self.name = None
        self.primary_key = None
        self.unit_key = None
        self.qty_key = None
        self.required_headers = None
        self.data = None

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
        file_path : str
            Location of the impact categories json file.
        
        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            Database created.
        """
        new_db = cls()
        new_db.set_name(name)
        new_db.set_primary_key('Flow')
        new_db.set_unit_key('Unit') 
        new_db.set_qty_key('Qty')

        return new_db

    # =================================
    # Setters
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

    def set_data(self, file_path, **kwargs):
        """ Set the database data.
        
        Parameters
        ----------
        file_path : str
            Location of the CSV file.

        Other Parameters
        ----------------
        impact_headers_map : dict
            The headers of the CSV file as they would be mapped to the impacts in the database: {**header** (:class:`str`): **impact category** (:class:`str`)}.
        emission_headers_map : dict
            The headers of the CSV file as they would be mapped to the emission inventories in the database: {**header** (:class:`str`): **inventory** (:class:`str`)}.
        carbon_storage_headers_map : dict
            The headers of the CSV file as they would be mapped to the carbon storage in the database: {**header** (:class:`str`): **carbon storage** (:class:`str`)}.
        grouped_data : str
            Prefix used in the grouped data.
        additional_headers : list of str
            Headers of the columns to be imported, other than name, unit, and impact categories.
        multipliers : list of float
            Values of each column of the CSV will be multiplied by these values, in the order given in impact headers first and then additional headers.
        
        Raises
        ------
        KeyError
            Category not recognized.
        """
        # map headers
        mapped_headers = []
        for data_type, DATA_HEADERS_DICT in self.__class__.DATA_IMPORTS.items():
            map_name = data_type[:-1] + '_headers_map'
            if map_name in kwargs: # remove 's' at the end of data type
                for cat, mapped_cat in kwargs[map_name].items():
                    if mapped_cat not in DATA_HEADERS_DICT:
                        raise KeyError(f"{cat} {data_type} not recognized.")
                mapped_headers.extend(list(kwargs[map_name].keys()))
            else:
                mapped_headers.extend(list(DATA_HEADERS_DICT.keys()))

        data_headers = self.get_required_headers() + mapped_headers
        if 'additional_headers' in kwargs:
            if isinstance(kwargs['additional_headers'], list):
                data_headers = data_headers + kwargs['additional_headers']
            elif isinstance(kwargs['additional_headers'], str):
                data_headers = data_headers + [kwargs['additional_headers']]
                
        if 'grouped_data' in kwargs:
            new_headers = []
            for data_type, DATA_HEADERS_DICT in self.__class__.DATA_IMPORTS.items():
                for cat in DATA_HEADERS_DICT:
                    new_headers.append(kwargs['grouped_data'] + '_' + cat)
                
            new_headers.append(kwargs['grouped_data'] + '_' + self.get_qty_key())
            new_headers.append(kwargs['grouped_data'] + '_' + self.get_unit_key())
            
            data_headers = data_headers + new_headers

        # multipliers
        no_headers = len(data_headers)
        if 'multipliers' not in kwargs:
            multipliers = [1.0] * len(mapped_headers)
        multipliers = [None] * len(self.get_required_headers()) + multipliers + [None] * (no_headers - 3 - len(multipliers))

        # import data
        data = DataImporter.csv_to_pandas(file_path, data_headers, multipliers)

        data[self.get_unit_key()] = data[self.get_unit_key()].map(UNITS_MAP)

        # rename mapped headers
        for data_type, DATA_HEADERS_DICT in self.__class__.DATA_IMPORTS.items():
            map_name = data_type[:-1] + '_headers_map'
            if map_name in kwargs: 
                data.rename(columns=kwargs[map_name], inplace=True)

        # set missing data to 0.0
        for data_categroy, DATA_HEADERS_DICT in self.__class__.DATA_IMPORTS.items():
            for header in DATA_HEADERS_DICT:
                if header not in data.columns:
                    data[header] = 0.0
                    log(f"{header} {data_categroy} not found in the data. Setting to 0.0.", level="Warn")      

        # loading data to existing dataset
        if self.get_data_all() is None:
            self.data = data
        else:
            self.data = concat([self.get_data_all(), data], ignore_index=True)

        return self

    def set_data_entry(self, flow, qty, unit, **kwargs):
        """ Add a custom entry the database.

        Parameters
        ----------
        flow : str
            Name of the impact.
        qty : float
            Quantity of the flow.
        unit : str
            Unit of measurement for which the impacts are applied.

        Other Parameters
        ----------------
        impacts : dict
            Dictionary of impacts {**impact catergory** (:class:`str`): **impact** (:class:`float`)}.
        emissions : dict
            Dictionary of emissions {**emission inventory** (:class:`str`): **emission** (:class:`float`)}.
        carbon_storage : dict
            Dictionary of carbon storage {**carbon storage** (:class:`str`): **carbon quantity** (:class:`float`)}.
        additional_data : dict
            Dictionary of additional data {**header** (:class:`str`): **value** (:class:`str` / :class:`float`/ :class:`int`)}.
        
        Raises
        ------
        KeyError
            Category not recognized.
        """
        # check input data
        if flow in self.data[self.get_primary_key()].tolist():
            raise ImportError(f"Flow name {flow} already exists in the database. Please use a different name.")
        
        for data_type, category_dict in kwargs.items():
            if data_type in self.__class__.DATA_IMPORTS:
                valid_categories = self.__class__.DATA_IMPORTS[data_type]
                for category in category_dict:
                    if category not in valid_categories:
                        raise KeyError(f"{category} in {data_type} is not recognized.")
            elif data_type == 'additional_data':
                pass # TODO: check if the additional headers exist/ if not create them and add the new data
            else:
                raise KeyError(f"{data_type} not recognized as a key word argument.")
        
        # organize data
        tmp_data = {k: v for d in kwargs.values() for k, v in d.items()}
        tmp_data[self.get_primary_key()] = flow
        tmp_data[self.get_qty_key()] = qty
        tmp_data[self.get_unit_key()] = unit
     
        # set missing data to 0.0
        for data_type, DATA_HEADERS_DICT in self.__class__.DATA_IMPORTS.items():
            for category in DATA_HEADERS_DICT:
                if category not in tmp_data:
                    tmp_data[category] = 0.0
                    log(f"{category} {data_type} not found in the data. Setting to 0.0.", level="Warn")   
        
        # set data to database
        self.data.loc[len(self.data)] = tmp_data
        
        return self.data

    def set_primary_key(self, key):
        """ Set primary key of the database.
        
        Parameters
        ----------
        key : str
            Primary key organizing the database.
        """
        self.primary_key = key

        return self
    
    def set_unit_key(self, key):
        """ Set unit key of the database.
        
        Parameters
        ----------
        key : str
            Data header corresponding to the units of the database entries.
        """
        self.unit_key = key

        return self
    
    def set_qty_key(self, key):
        """ Set quantity key of the database.
        
        Parameters
        ----------
        key : str
            Data header corresponding to the quantity of the database entries.
        """
        self.qty_key = key

        return self

    # =================================
    # Getters
    # =================================    
    def get_name(self):
        """ Get the name of the database.
    
        Returns
        -------
        str
            Name of the database.
        """
        return self.name
    
    def get_impact_category_units(self):
        """ Get the units of the impact categories.
        
        Returns
        -------
        list of str
            List of units of the impact categories.
        """
        units = []
        for key, value in config['setup']['impacts']['IMPACT_CATEGORIES'].items():
            units.append(value['refUnit'])

        return units
    
    def get_data_all(self):
        """ Retrieve impact data in the database.
        
        Returns
        -------
        pandas.DataFrame
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
        pandas.Series
            Databse entry corresponding to the flow.

        Raises
        ------
        ImportError
            Multiple matching entries.
        """
        if self.data is not None:
            row_id = self.data.index[self.data[self.get_primary_key()] == flow_name]
            if len(row_id) == 1:
                return self.data.iloc[row_id[0]]
            else:
                raise ImportError("Multiple matching entries exist...")

    def get_primary_key(self):
        """ Get primary key of the database.
        
        Returns
        -------
        str
            Primary key organizing the database.
        """
        return self.primary_key
    
    def get_unit_key(self):
        """ Get unit key of the database.
        
        Returns
        -------
        str
            Data header corresponding to the units of the database entries.
        """
        return self.unit_key
    
    def get_qty_key(self):
        """ Get quantity key of the database.
        
        Returns
        -------
        str
            Data header corresponding to the quantity of the database entries.
        """
        return self.qty_key
    
    def get_required_headers(self):
        """ Get the required headers of the database.
        
        Returns
        -------
        list of str
            Headers of the columns to be imported, other than name, unit, and impact categories.
        """
        return [self.get_primary_key(), self.get_qty_key(), self.get_unit_key()]


if __name__ == '__main__':
    pass
