
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import Impacts
from ..impacts import TranportationModeImpactsDatabase
from ..transportation import TransportationManager
from ..transportation import USDomesticTransportationManager
from ..transportation import USGlobalTransportationManager

class TransportationMixins:
    """ Methods for calculation of A4 impacts
    """

    def set_transportation_manager(self, logistic_type='local'):
        """ Set the logistics manager of the building project.
        
        Parameters
        ----------
        logistic_type : {'local', 'global'}
            Transportation scope of the building project.

        Raises
        ------
        ValueError
            Logistic type not recognized.
        """
        if self.get_location() is None:
            self.transportation_manager = TransportationManager.new('transportation')
        elif self.get_location().get_country_code() == 'US':
            if logistic_type == 'local':
                self.transportation_manager = USDomesticTransportationManager.new('transportation')
            elif logistic_type == 'global':
                self.transportation_manager = USGlobalTransportationManager.new('transportation')
            else: 
                raise ValueError(f"Logistic type {logistic_type} not recognized.")
        else:
            self.transportation_manager = TransportationManager.new('transportation')

        if self.get_transportation_mode_impact_database() is not None:
            self.get_transportation_manager().set_impact_database(self.get_transportation_mode_impact_database())

        return self

    def get_transportation_manager(self):
        """ Get the transportation manager of the project.
        
        Returns
        -------
        ~pod_lca.transportation.TransportationManager
            Transportation manager of the project.
        """
        return self.transportation_manager
    
    # ================================
    # Database Methods
    # ================================   
    def set_transportation_mode_impact_database(self, file_path):
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

    def get_transportation_mode_impact_database(self):
        """ Get the impact database for end-of-life impacts.
        
        Returns
        -------
        ~pod_lca.impacts.TranportationModeImpactsDatabase
            Filepath to the csv file containing impact data.
        """
        return self.transport_impact_database
    
    # ================================
    # Inventory Records Methods
    # ================================ 
    def get_transportation_impacts(self):
        """ Get A4-A5 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            A4-A5 impacts of the building.
        """
        impacts = Impacts.from_parent(self)

        for transportaion_leg in self.get_transportation_manager().get_transportation_legs():
            impacts += transportaion_leg.get_impacts()

        return impacts

    def get_transportation_emissions(self):
        """ Get A4-A5 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions
            A4-A5 emissions of the building.
        """
        emissions = Emissions.from_parent(self)

        for transportaion_leg in self.get_transportation_manager().get_transportation_legs():
            emissions += transportaion_leg.get_emissions()

        return emissions


if __name__ == '__main__':
    pass