
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import EOLImpactsDatabase
from ..impacts import TranportationModeImpactsDatabase


class EndOfLifeMixins:

    def set_transportation_impact_database(self, database):
        """ Set the impact database for end-of-life impacts.
        
        Parameters
        ----------
        database : ~pod_lca.impacts.TranportationModeImpactsDatabase or str
            Impact database object or if a string, filepath to the corresponding csv file containing impact data.
        """
        if isinstance(database, TranportationModeImpactsDatabase):
            self.transport_impact_database = database
        elif isinstance(database, str):
            impact_database = TranportationModeImpactsDatabase.new("impact database")
            impact_database.set_data(database)
            self.set_transportation_impact_database(impact_database)
        else:
            raise TypeError("Database input not recognized")

        return self
    
    def set_eol_database(self, database):
        """ Set the impact database for end-of-life impacts.
        
        Parameters
        ----------
        database : ~pod_lca.impacts.EOLImpactsDatabase or str
            Impact database object or if a string, filepath to the corresponding csv file containing impact data.
        """
        if isinstance(database, EOLImpactsDatabase):
            self.eol_impact_database = database
        elif isinstance(database, str):
            impact_database = EOLImpactsDatabase.new("impact database")
            impact_database.set_data(database)
            self.set_eol_database(impact_database)
        else:
            raise TypeError("Database input not recognized")
    
    def set_eol_transport_dataset(self, dataset):
        """ Set transportation dataset for the end-of-life impacts.

        Parameters
        ----------
        dataset : ~pod_lca.transportation.TransportDataset
            End-of-life transportation dataset.
        """
        self.eol_transport_dataset = dataset

        return self
    
    def get_transportation_impact_database(self):
        """ Set the impact database for end-of-life impacts.
        
        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            End-of-Life impacts database.
        """
        return self.transport_impact_database
    
    def get_eol_database(self):
        """ Get the impact database for end-of-life impacts.
        
        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            End-of-Life impacts database.
        """
        return self.eol_impact_database

    def get_eol_transport_dataset(self):
        """ Get transportation dataset for the end-of-life impacts.

        Returns
        -------
        ~pod_lca.transportation.TransportDataset
            End-of-life transportation dataset.
        """
        return self.eol_transport_dataset
    
    # ================================
    # EOL Methods
    # ================================ 
    def deconstruct(self):

        pass # TODO: write method to deconstruct the building and add C1 impacts

    def demolish(self):

        pass # TODO: write method to demolish the building and add C1 impacts


if __name__ == '__main__':
    pass
