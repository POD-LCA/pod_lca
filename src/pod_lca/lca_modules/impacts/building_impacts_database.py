
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import ImpactsDatabase


class BuildingMaterialImpactsDatabase(ImpactsDatabase):
    """ Database manager to handle End-of-Life impacts.

    Attributes
    ----------
    process_key : str
        Data header corresponding to the end-of-life pathway corresponding to the database entry.
    life_cycle_stage_key : str
        Data header corresponding to the life cycle stage corresponding to the database entry.
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
            Data header corresponding to the end-of-life process corresponding to the database entry.
        """
        return self.variablility_key
    
    def get_geography_key(self):
        """ Get life cycle stage key of the database.
        
        Returns
        -------
        str
            Data header corresponding to the life cycle stage corresponding to the database entry.
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
        geography_representation : {'C3', 'C4', 'D'}
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
                return self.data.iloc[row_id[0]]
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


if __name__ == '__main__':
    pass
