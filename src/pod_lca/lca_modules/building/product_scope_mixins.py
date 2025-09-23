
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import Impacts
from ..impacts import ImpactsDatabase


class ProductScopeMixins:
    """ Methods for calculation of A1-A3 impacts
    """

    # ================================
    # Database Methods
    # ================================
    def set_material_database(self, file_path):
        """ Set the impact database for materials (A1-A3).
        
        Parameters
        ----------
        file_path : str
            Filepath to the csv file containing impact data. The csv file must contain headers 'sctg code' and 'eol material' in addition to the 
        """
        if isinstance(file_path, str):
            impact_database = ImpactsDatabase.new("impact database")
            impact_database.set_data(file_path, additional_headers=['sctg code',
                                                                    'eol material', 
                                                                    'bio-based',
                                                                    'random test',
                                                                    'Density', 
                                                                    'Density unit'])
            self.material_impact_database = impact_database
        else:
            raise TypeError("Database input not recognized")
        
    def get_material_impact_database(self):
        """ Get the impact database for materials (A1-A3).
        
        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            Impact database object.
        """
        return self.material_impact_database

    # ================================
    # Inventory Records Methods
    # ================================        
    def get_product_impacts(self):
        """ Get A1-A3 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            A1-A3 impacts of the building.
        """
        impacts = Impacts.from_parent(self)
        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                impacts += material.get_impacts()
        # TODO: test with the envelope assemblies

        return impacts

    def get_product_emissions(self):
        """ Get A1-A3 emissions of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions
            A1-A3 emissions of the building.
        """        
        emissions = Emissions.from_parent(self)
        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                emissions += material.get_emissions()
        # TODO: test with the envelope assemblies

        return emissions


if __name__ == '__main__':
    pass
