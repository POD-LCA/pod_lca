
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ...utilities import DataImporter
from ...utilities import config


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
    service_life_category : str
        Service life category at assembly level. A temporary parameter for use when assembly is added to a building.
    service_life : float
        Service life of the assembly in years.
    """

    def __init__(self):
        self.name = None
        self.parent = None
        self.materials = []
        self.service_life_category = None
        self.service_life = None

    # ================================
    # Constructors
    # ================================        
    @classmethod
    def from_materials(cls, name, materials=None):
        """ Create a building assembly from its constituent materials.
        
        Parameters
        ----------
        name : str
            Name of the assembly.
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
    
    def set_parent(self, parent):
        """ Set the parent (structure/envelope) of the assembly.
        
        Parameters
        ----------
        parent : ~pod_lca.building.Envelope or ~pod_lca.building.BuildingStructure
            Building to which the assembly belong.
        """
        self.parent = parent
        self.set_building()

        return self
    
    def set_building(self):
        """Set data from building level."""
        pass
    
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

    def set_service_life_category(self, service_life_category):
        """ Set the service life category.
        
        Parameters
        ----------       
        service_life_category : str
            Service life category at assembly level.
        """
        self.service_life_category = service_life_category
    
    def set_service_life(self, service_life):
        """ Set the service life of the material.
        
        Parameters
        ----------
        service_life : float
            Service life of the material in years.
        """
        building = self.get_building()
        if service_life in ['Life of Building']:
            service_life = building.get_life_span()    
        
        # TODO: how to handle updating assembly/material service life

        self.service_life = min(float(service_life), building.get_life_span())

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

    def get_parent(self):
        """ Set the parent (structure/envelope) of the assembly.

        Returns
        -------
        ~pod_lca.building.Envelope or ~pod_lca.building.BuildingStructure
            Structure/envelope to which the assembly belong.
        """
        return self.parent

    def get_building(self):
        """ Get the building of the assembly.
        
        Returns
        -------
        ~pod_lca.building.Building
            Building to which the assembly belong.
        """
        from .building import Building
        
        if self.parent is not None:
            if isinstance(self.parent, Building):
                return self.parent
            else:
                return self.parent.get_building()
        else:
            return None

    def get_materials(self):
        """ Get the materials constituiting the building assembly.
        
        Returns
        -------
        list of ~pod_lca.building.BuildingMaterial
            Materials making up the assembly.
        """
        return self.materials

    def get_service_life_category(self):
        """ Get the service life category.
        
        Returns
        -------        
        str
            Service life category at assembly level.        
        """
        return self.service_life_category
    
    def get_service_life(self):
        """ Get the service life of the assembly.
        
        Returns
        -------
        float
            Service life of the material in years.
        """
        if (self.service_life is None)and self.get_service_life_category():
            service_life = self.get_service_life_category()

            building_standard = self.get_building().get_building_data_standard()
            service_life_mapping = DataImporter.csv_to_dict(config['file_paths']['building'][building_standard.upper() + '_SERVICE_LIFE'], 'POD|LCA RSL Category')
            
            if service_life in service_life_mapping:
                if isinstance(service_life_mapping[service_life]['service_life'], (int, float)):
                    self.service_life = float(service_life_mapping[service_life]['service_life'])
                elif isinstance(service_life_mapping[service_life]['service_life'], str):
                    if service_life_mapping[service_life]['service_life'].lower() in ['life of building', 'building life span', 'building lifespan']:
                        self.service_life = self.get_building().get_life_span()
                    else:
                        try:
                            self.service_life = float(service_life_mapping[service_life]['service_life'])
                        except ValueError:
                            raise ValueError(f"Service life value '{service_life_mapping[service_life]['service_life']}' not recognized for category '{service_life}' in '{building_standard}' service life database.")
                else:
                    raise ValueError(f"Service life value type not recognized for category '{service_life}' in '{building_standard}' service life database.")

        return self.service_life
    
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
        
        material.set_parent(self)
        
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
