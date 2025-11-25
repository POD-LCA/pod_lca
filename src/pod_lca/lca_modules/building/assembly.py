
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


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
    def create(cls, name, building, **kwargs):
        """ Create a building assembly from its constituent materials.
        
        Parameters
        ----------
        name : str
            Name of the assembly.
        building : ~pod_lca.building.Building
            Building to which the assembly belong.

        Other Parameters
        ----------------
        materials : list of material.Model  or Product Objs
            Materials making up the assembly.
        service_life : float
            Service life of the assembly in years.

        Returns
        -------
        ~pod_lca.building.Assembly
            Building assembly created.
        """
        assembly = cls()

        building.add_assembly(assembly)
        assembly.set_name(name)
        if "materials" in kwargs:
            assembly.set_materials(kwargs["materials"])
        if "service_life" in kwargs:
            assembly.set_service_life(kwargs["service_life"])

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

    def get_service_life(self):
        """ Get the service life of the assembly.
        
        Returns
        -------
        float
            Service life of the material in years.
        """
        if self.service_life is None:
            tmp_service_life = self.get_building().get_life_span()
            for material in self.get_materials():
                if material.get_service_life() is not None:
                    tmp_service_life = min(tmp_service_life, material.get_service_life())
            
            return tmp_service_life
        
        else:
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

        if material.get_production_year() is None:
            material.set_production_year(self.get_building().get_built_year())
        if material.get_service_life() is None:
            material.set_service_life(self.get_service_life())

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
