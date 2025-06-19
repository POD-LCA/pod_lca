
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import ImpactsDatabase


class ElectricityImpactsDatabase(ImpactsDatabase):
    """ Database manager to handle electricity impacts.

    Attributes
    ----------
    process_key : str
        Data header corresponding to the end-of-life process corresponding to the database entry.
    life_cycle_stage_key : str
        Data header corresponding to the life cycle stage corresponding to the database entry.
    """

    def __init__(self):
        super().__init__()
        self.region_key = None
        self.technology_key = None

    # =================================
    # Constructors
    # =================================
    @classmethod
    def new(cls, name, geographical_scope=None):
        """ Create a new database.
        
        Parameters
        ----------
        name : str
            Name of the database.
        file_path : str
            Location of the impact categories json file.
        geographical_scope : str
            Geographical scope of the database. Recognized values are 'National' and 'Regional'.
        
        Returns
        -------
        ImpactsDatabase Obj.
            Database created.
        """
        new_db = cls()
        new_db.set_name(name)
        new_db.set_unit_key('Unit') 
        new_db.set_qty_key('Qty')

        if geographical_scope == 'National':
            new_db.set_region_key('Country code')
        elif geographical_scope == 'Regional' or geographical_scope == 'Local':
            new_db.set_region_key('Region')
        else:
            raise ValueError(f"Geographical scope {geographical_scope} not recognized. Recognized spatial resolutions are: 'National' and 'Regional'.")

        new_db.set_technology_key('Technology Type')

        return new_db
    
    # =================================
    # Setters
    # =================================
    def set_region_key(self, key):
        """ Set region key of the database.
        
        Parameters
        ----------
        key : str
            Data header corresponding to the end-of-life process corresponding to the database entry.
        """
        self.region_key = key

        return self
    
    def set_technology_key(self, key):
        """ Set technology key of the database.
        
        Parameters
        ----------
        key : str
            Data header corresponding to the end-of-life process corresponding to the database entry.
        """
        self.technology_key = key

        return self

    # =================================
    # Getters
    # =================================    
    def get_region_key(self):
        """ Get region key of the database.
        
        Returns
        -------
        str
            Data header corresponding to the end-of-life process corresponding to the database entry.
        """
        return self.region_key
    
    def get_technology_key(self):
        """ Get technology key of the database.
        
        Returns
        -------
        str
            Data header corresponding to the end-of-life process corresponding to the database entry.
        """
        return self.technology_key

    def get_required_headers(self):
        """ Get the required headers of the database.
        """
        return  [self.get_qty_key(), self.get_unit_key(), self.get_region_key(), self.get_technology_key()]

    def get_data_entry(self, region, technology):
        """ Retrieve impacts for given flow.
        
        Parameters
        ----------
        material_name : str
            Name of the material
        process_name: str
            End-of-Life process name.
        life_cycle_stage : str
            Life cycle stage.
        
        Returns
        -------
        Pandas Series
            Databse entry corresponding to the flow.
        """
        if self.data is not None:
            if region in self.data[self.get_region_key()].values:
                impact_data_tmp = self.data[self.data[self.get_region_key()] == region].drop([self.get_region_key(), self.get_qty_key(), self.get_unit_key()], axis='columns')
                impact_data_dict = impact_data_tmp[impact_data_tmp[self.get_technology_key()] == technology].drop([self.get_technology_key()], axis='columns').squeeze().to_dict()
                return impact_data_dict
            else:
                raise KeyError(f"{region} not in the database.")  
         
            
if __name__ == '__main__':
    pass
