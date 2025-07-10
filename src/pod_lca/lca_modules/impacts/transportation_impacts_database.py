
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import ImpactsDatabase


class TranportationModeImpactsDatabase(ImpactsDatabase):
    """ Database manager to handle End-of-Life impacts.

    Attributes
    ----------
    fuel_type_key : str
        Data header corresponding to the fuel type corresponding to the database entry.
    mode_efficiency_key : str
        Data header corresponding to the mode efficiency corresponding to the database entry.
    """

    def __init__(self):
        super().__init__()
        self.mode_efficiency_key = None

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
        new_db.set_primary_key('mode_name')
        new_db.set_unit_key('Unit') 
        new_db.set_qty_key('Qty')
        new_db.set_mode_efficiency_key('eff')

        return new_db
    
    # =================================
    # Setters
    # =================================  
    def set_mode_efficiency_key(self, key):
        """ Set the mode efficiency key of the database.

        Parameters
        ----------
        key : str
            Data header corresponding to the mode efficiency corresponding to the database entry.
        """
        self.mode_efficiency_key = key

        return self

    # =================================
    # Getters
    # =================================
    def get_mode_efficiency_key(self):
        """ Get the mode efficiency key of the database.

        Returns
        -------
        str
            Data header corresponding to the mode efficiency corresponding to the database entry.
        """
        return self.mode_efficiency_key
    
    def get_required_headers(self):
        """ Get the required headers of the database.
        """
        return  [self.get_primary_key(), self.get_qty_key(), self.get_unit_key(), self.get_mode_efficiency_key()] 
    
    def get_data_entry(self, mode):
        """ Retrieve impacts for given flow.
        
        Parameters
        ----------
        mode : TransportMode Obj.
            Transport mode with its name, fuel type, and efficiency.
        
        Returns
        -------
        Pandas Series
            Databse entry corresponding to the flow.
        """
        mode_name = mode.get_name()
        mode_efficiency = mode.get_efficiency()

        if self.data is not None:
            row_id = self.data.index[(self.data[self.get_primary_key()] == mode_name) & (self.data[self.get_mode_efficiency_key()] == mode_efficiency)]
            if len(row_id) == 1:
                return self.data.iloc[row_id[0]]
            elif len(row_id) == 0:
                raise ImportError(f"Data for {mode_name} fuel of {mode_efficiency} efficiency not in database.")
            else:
                raise ImportError("Multiple matching entries exist...")


if __name__ == '__main__':
    pass
