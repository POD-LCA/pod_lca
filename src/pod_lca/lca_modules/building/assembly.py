
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

import gc

from ..eol.waste import Waste
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class Assembly:
    """ Assemblies which the building is made up of.

    Attributes
    ----------
    name : str
        Name of the building.
    building : Building Obj.
        Building to which the assembly belong.
    materials : list of ~pod_lca.building.BuildingMaterial
        Materials making up the assembly.
    service_life : float
        Service life of the assembly in years.
    """

    def __init__(self):
        self.name = None
        self.building = None
        self.materials = []
        self.service_life = None

    # ================================
    # Constructors
    # ================================        
    @classmethod
    def create(cls, name, building, materials=None):
        """ Create a building assembly from its constituent materials.
        
        Parameters
        ----------
        name : str
            Name of the assembly.
        building : ~pod_lca.building.Building
            Building to which the assembly belong
        materials : list of material.Model  or Product Objs
            Materials making up the assembly.

        Returns
        -------
        ~pod_lca.building.Assembly
            Building assembly created.
        """
        assembly = cls()

        assembly.set_name(name)
        if materials is not None:
            assembly.set_materials(materials)

        building.add_assembly(assembly)

        return assembly

    # ================================
    # Setters
    # ================================  
    def set_name(self, name):
        """ Set the name of the building assembly.

        Parameters
        ----------
        name : str
            Name of the building assembly.
        """
        self.name = name

        return self
    
    def set_building(self, building):
        """ Set the building of the assembly.
        
        Parameters
        ----------
        building : ~pod_lca.building.Building
            Building to which the assembly belong.
        """
        self.building = building

        return self
    
    def set_materials(self, materials):
        """ Set the materials constituiting the building assembly.
        
        Parameters
        ----------
        materials : list of ~pod_lca.building.BuildingMaterial
            Materials making up the assembly.
        """
        for material in materials:
            self.add_material(material)
        return self

    # ================================
    # Getters
    # ================================
    def get_name(self):
        """ Get the name of the building assembly.

        Returns
        -------
        str
            Name of the building assembly.
        """
        return self.name

    def get_building(self):
        """ Get the building of the assembly.
        
        Returns
        -------
        ~pod_lca.building.Building
            Building to which the assembly belong.
        """
        return self.building
    
    def get_materials(self):
        """ Get the materials constituiting the building assembly.
        
        Returns
        -------
        list of ~pod_lca.building.BuildingMaterial
            Materials making up the assembly.
        """
        return self.materials
    
    # ================================
    # Methods
    # ================================
    def add_material(self, material):
        """ Add a material to the building assembly.
        
        Parameters
        ----------
        material : ~pod_lca.building.BuildingMaterial
            Material from whcih the assembly is composed of.
        """
        self.materials.append(material)

        if material.get_parent() is None:
            material.set_parent(self.get_building())
        material.set_transportation()

        # TODO set A1-A3 impacts / material could be a Model object or a product
        # TODO: add a output product to material models
        return self

    # ================================
    # EOL Methods
    # ================================ 
    def get_eol_manager(self):
        """ Return the place where end-of-life transport dataset reside.
        """
        return self.get_building()


if __name__ == '__main__':
    pass
