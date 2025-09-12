
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import Impacts
from ..impacts import TranportationModeImpactsDatabase


class ConstructionMixins:

    # ================================
    # Database Methods
    # ================================   
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

    # ================================
    # Inventory Records Methods
    # ================================ 
    def get_construction_impacts(self, lc_stage=None):
        """ Get A4-A5 impacts of the building.

        Parameters
        ----------
        lc_stage: {'A4', 'A5', None}
            Life cycle stage for which the impacts to be calculated. 
            If None, gives impacts for all the relevant life cycle stages. 
            Default is None.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            A4-A5 impacts of the building.
        """
        impacts = Impacts.from_parent(self)

        # TODO add logic

        return impacts

    def get_construction_emissions(self, lc_stage=None):
        """ Get A4-A5 impacts of the building.

        Parameters
        ----------
        lc_stage: {'A4', 'A5', None}
            Life cycle stage for which the emissions to be calculated. 
            If None, gives emissions for all the relevant life cycle stages. 
            Default is None.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions
            A4-A5 emissions of the building.
        """
        emissions = Emissions.from_parent(self)

        # TODO add logic

        return emissions


if __name__ == '__main__':
    pass