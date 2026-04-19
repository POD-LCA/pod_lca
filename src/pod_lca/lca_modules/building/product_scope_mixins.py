
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pathlib import Path

from ..impacts import Emissions
from ..impacts import Impacts
from ..impacts import BuildingMaterialImpactsDatabase
from ...utilities import config


class ProductScopeMixins:
    """ Methods for calculation of A1-A3 impacts
    """

    # ================================
    # Database Methods
    # ================================
    def set_material_database(self, file_path=None):
        """ Set the impact database for materials (A1-A3). If file path is not provided, the default database will be used.
        
        Parameters
        ----------
        file_path : str
            Filepath to the csv file containing impact data. The csv file must contain headers 'sctg code' and 'eol material' in addition to the 
        """
        if file_path is None:
            file_path = config['file_paths']['building']['DEFAULT_IMPACT_DATABASE']
        if isinstance(file_path, (str, Path)):
            impact_database = BuildingMaterialImpactsDatabase.new("impact database")
            impact_database.set_primary_key('product')
            impact_database.set_qty_key('Declared qty')
            impact_database.set_unit_key('Declared unit')
            impact_database.set_variability_key('Value')
            impact_database.set_geography_key('Geography')
            impact_database.set_data(file_path, additional_headers=['sctg code',
                                                                    'eol material',
                                                                    'waste_rate_category',
                                                                    'bio-based',
                                                                    'DRF Category',
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
    def get_product_impacts(self, objs=False):
        """ Get A1-A3 impacts of the building.

        Parameters
        ----------
        objs : bool, optional
            If True, return a list of impacts objects for each material. 
            If False, return a single impacts object for the entire building. Default is False.

        Returns
        -------
        ~pod_lca.impacts.Impacts or list of ~pod_lca.impacts.Impacts
            A1-A3 impacts of the building. List of impacts if Objs is True.
        """
        impacts = [] if objs else Impacts.from_parent(self)
        assemblies = self.get_assemblies()
        for assembly in assemblies:
            materials = assembly.get_materials()
            for material in materials:
                if objs:
                    impacts.append(material.get_impacts())
                else:
                    impacts += material.get_impacts()

        return impacts

    def get_product_emissions(self, objs=False):
        """ Get A1-A3 emissions of the building.

        Parameters
        ----------
        objs : bool, optional
            If True, return a list of emissions objects for each material. 
            If False, return a single emissions object for the entire building. Default is False.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions, list of ~pod_lca.impacts.Emissions
            A1-A3 emissions of the building. List of emissions if Objs is True.
        """        
        emissions = [] if objs else Emissions.from_parent(self)
        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                if objs:
                    emissions.append(material.get_emissions())
                else:
                    emissions += material.get_emissions()

        return emissions


if __name__ == '__main__':
    pass
