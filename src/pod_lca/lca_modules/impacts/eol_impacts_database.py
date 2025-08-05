
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import ImpactsDatabase


class EOLImpactsDatabase(ImpactsDatabase):
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
        self.process_key = None
        self.life_cycle_stage_key = None

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
        new_db.set_primary_key('Flow')
        new_db.set_unit_key('Unit') 
        new_db.set_qty_key('Qty')
        new_db.set_process_key('Process')
        new_db.set_life_cycle_stage_key('Life Cycle Stage')

        return new_db

    # =================================
    # Setters
    # =================================
    def set_process_key(self, key):
        """ Set process key of the database.
        
        Parameters
        ----------
        key : str
            Data header corresponding to the end-of-life pathway corresponding to the database entry.
        """
        self.process_key = key

        return self
    
    def set_life_cycle_stage_key(self, key):
        """ Set life cycle stage key of the database.
        
        Parameters
        ----------
        key : str
            Data header corresponding to the life cycle stage corresponding to the database entry.
        """
        self.life_cycle_stage_key = key

        return self

    # =================================
    # Getters
    # ================================= 
    def get_process_key(self):
        """ Get process key of the database.
        
        Returns
        -------
        str
            Data header corresponding to the end-of-life process corresponding to the database entry.
        """
        return self.process_key
    
    def get_life_cycle_stage_key(self):
        """ Get life cycle stage key of the database.
        
        Returns
        -------
        str
            Data header corresponding to the life cycle stage corresponding to the database entry.
        """
        return self.life_cycle_stage_key
    
    def get_required_headers(self):
        """ Get the required headers of the database.

        Returns
        -------
        list of str
            Database headers.
        """
        return  [self.get_primary_key(), self.get_qty_key(), self.get_unit_key(), self.get_process_key(), self.get_life_cycle_stage_key()] 
    
    def get_data_entry(self, material_name, process_name, life_cycle_stage):
        """ Retrieve impacts for given flow.
        
        Parameters
        ----------
        material_name : str
            Name of the material
        process_name : {'Landfill', 'Recycle', 'Compost', 'Incinerate'}
            End-of-life pathway:

            - 'Landfill': transporting waste to a landfill.
            - 'Recycle': transporting waste to a recycler.
            - 'Compost': transporting to a composting facility.
            - 'Incinerate': transporting to an incinerator.
        life_cycle_stage : {'C3', 'C4', 'D'}
            Life cycle stage.

            - 'C3': waste processing
            - 'C4': disposal
            - 'D': reuse
        
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
            row_id = self.data.index[(self.data[self.get_primary_key()] == material_name) & (self.data[self.get_process_key()] == process_name) & (self.data[self.get_life_cycle_stage_key()] == life_cycle_stage)]
            if len(row_id) == 1:
                return self.data.iloc[row_id[0]]
            elif len(row_id) == 0:
                raise ImportError(f"Data for {material_name} {process_name} process ({life_cycle_stage}) not in database.")
            else:
                raise ImportError("Multiple matching entries exist...")


if __name__ == '__main__':
    pass
