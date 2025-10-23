
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from numpy import isnan

from . import ImpactsDatabase
from ...utilities import config
from ...utilities import DataImporter


class BuildingMaterialImpactsDatabase(ImpactsDatabase):
    """ Database manager to handle building material impacts.

    Attributes
    ----------
    variablility_key : str
        Data header identifying the level of variability to the database entry.
    geography_key : str
        Data header geographical representation of the database entry.
    """

    def __init__(self):
        super().__init__()
        self.variablility_key = None
        self.geography_key = None

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
        ~pod_lca.impacts.EOLImpactsDatabase
            Database created.
        """
        new_db = cls()
        new_db.set_name(name)
        new_db.set_primary_key('Product')
        new_db.set_unit_key('Unit') 
        new_db.set_qty_key('Qty')
        new_db.set_variability_key('value')
        new_db.set_geography_key('Geography')

        return new_db

    # =================================
    # Setters
    # =================================
    def set_variability_key(self, key):
        """ Set the header identifying the level of variability of the database entry.
        
        Parameters
        ----------
        key : str
            Data header identifying the level of variability to the database entry.
        """
        self.variablility_key = key

        return self
    
    def set_geography_key(self, key):
        """ Set the geography key of the database.
        
        Parameters
        ----------
        key : str
            Data header geographical representation of the database entry.
        """
        self.geography_key = key

        return self

    # =================================
    # Getters
    # ================================= 
    def get_variability_key(self):
        """ Get process key of the database.
        
        Returns
        -------
        str
            Data header identifying the level of variability to the database entry.
        """
        return self.variablility_key
    
    def get_geography_key(self):
        """ Get life cycle stage key of the database.
        
        Returns
        -------
        str
            Data header geographical representation of the database entry.
        """
        return self.geography_key
    
    def get_required_headers(self):
        """ Get the required headers of the database.

        Returns
        -------
        list of str
            Database headers.
        """
        return  [self.get_primary_key(), self.get_qty_key(), self.get_unit_key(), self.get_variability_key(), self.get_geography_key()] 
    
    def get_data_entry(self, material_name, variability_level='Baseline', geography_representation='US'):
        """ Retrieve impacts for given flow.
        
        Parameters
        ----------
        material_name : str
            Name of the material
        variability_level : {'Baseline', 'High-80th%', 'Low-20th%'}
            The percintile of the value used.
        geography_representation : str
            geography representation of the place.
        
        Returns
        -------
        pandas.Series
            Databse entry corresponding to the flow.

        Raises
        ------
        ImportError
            Data not in database or multiple matching entries.
        """
        if self.data is not None:
            row_id = self.data.index[(self.data[self.get_primary_key()] == material_name)]
            
            if len(row_id) > 1:
                row_id = self.data.index[(self.data[self.get_primary_key()] == material_name) &
                                         (self.data[self.get_variability_key()] == variability_level)]

            if len(row_id) > 1:
                pass 
                # TODO: add geographical representation

            if len(row_id) == 1:
                data = self.data.iloc[row_id[0]].copy(deep=False)
                if 'DRF Category' in data and not isnan(data["DRF Category"]):
                    data = BuildingMaterialImpactsDatabase.emissions_from_drf_category(data)
                return data
            elif len(row_id) == 0:
                raise ImportError(f"Data for {material_name} {variability_level} representing ({geography_representation}) not in database.")
            else:
                raise ImportError("Multiple matching entries exist...")
            
    # =================================
    # Other methods
    # =================================         
    def check_database_entry(self, material):
        """ Check if the database contains the given item.

        Parameters
        ----------
        material : str
            The name of the database item which gives the item impacts.

        Returns
        -------
        bool
            True, if the database contains the item.
        """
    
        row_id = self.data.index[(self.data[self.get_primary_key()] == material)]
        if len(row_id) == 0:
            return False
        else:
            return True
        
    @staticmethod
    def emissions_from_drf_category(data):
        """ Missing emission data replaced with emissions computed based in DRF categories.
        """
        drf_categories = DataImporter.csv_to_dict(config['file_paths']['building']['DRF_CATEGORIES'], "DRF_Category")
        drf_category = data["DRF Category"]

        impacts_cat = drf_categories['CF']['Value']
        impact_val = data[impacts_cat]
        for emission in config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES']:
            if emission in drf_categories['CF'] and isnan(data[emission]):
                data.loc[emission] = impact_val * (float(drf_categories[str(drf_category)][emission]) / 100) / float(drf_categories['CF'][emission])

        # TODO: incorporate 'Value' variable
        return data  


if __name__ == '__main__':
    pass
