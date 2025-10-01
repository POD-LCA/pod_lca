
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import Impacts


class UseMixins:
    """ Methods for calculation of B1-B4 impacts
    """
    
    # ================================
    # Inventory Records Methods
    # ================================ 
    def get_replacement_impacts(self, objs=False):
        """ Get B4 impacts of the building.

        Parameters
        ----------
        objs : bool, optional
            If True, return a list of impacts objects for each material. 
            If False, return a single impacts object for the entire building. Default is False.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts or list of ~pod_lca.impacts.Impacts
            B6 impacts of the building. List of impacts if objs is True.
        """
        impacts = [] if objs else Impacts.from_parent(self)

        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                replacements = material.get_replacement_materials()
                if replacements is not None:
                    for replacement in replacements:
                        if objs:
                            replacement_impact = [replacement.get_product_impacts(),
                                                  *replacement.get_transportation_impacts(objs=True),
                                                  *replacement.get_eol_impacts(objs=True),
                                                  replacement.get_construction_impacts()]
                            impacts.extend(replacement_impact)
                        else:
                            replacement_impact = (replacement.get_product_impacts() + 
                                                  replacement.get_transportation_impacts() + 
                                                  replacement.get_eol_impacts() + 
                                                  replacement.get_construction_impacts())
                            impacts += replacement_impact

        return impacts

    def get_replacement_emissions(self, objs=False):
        """ Get B4 emissions of the building.

        Parameters
        ----------
        objs : bool, optional
            If True, return a list of impacts objects for each material. 
            If False, return a single impacts object for the entire building. Default is False.
                
        Returns
        -------
        ~pod_lca.impacts.Emissions or list of ~pod_lca.impacts.Emissions
            B6 emissions of the building. List of emissions if objs is True.
        """
        emissions = [] if objs else Emissions.from_parent(self)

        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                replacements = material.get_replacement_materials()
                if replacements is not None:
                    for replacement in replacements:
                        if objs:
                            replacement_emissions = [replacement.get_product_emissions(),
                                                     *replacement.get_transportation_emissions(objs=True),
                                                     *replacement.get_eol_emissions(objs=True),
                                                     replacement.get_construction_emissions()]
                            emissions.extend(replacement_emissions)
                        else:
                            replacement_emissions = (replacement.get_product_emissions() + 
                                                    replacement.get_transportation_emissions() + 
                                                    replacement.get_eol_emissions() + 
                                                    replacement.get_construction_emissions())
                            emissions += replacement_emissions

        return emissions


if __name__ == '__main__':
    pass
