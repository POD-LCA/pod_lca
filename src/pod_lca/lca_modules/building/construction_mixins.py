
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import EOLImpactsDatabase
from ..impacts import Impacts
from ..impacts import TranportationModeImpactsDatabase
from ..transportation import EOLTransportDataset


class ConstructionMixins:

    def set_transportation_impact_database(self, file_path):
        """ Set the impact database for end-of-life impacts.
        
        Parameters
        ----------
        file_path :str
            Filepath to the csv file containing impact data.
        """
        if isinstance(file_path, str):
            impact_database = TranportationModeImpactsDatabase.new("impact database")
            impact_database.set_data(file_path)
            self.transport_impact_database = impact_database
        else:
            raise TypeError("Database input not recognized")

        return self

if __name__ == '__main__':
    pass