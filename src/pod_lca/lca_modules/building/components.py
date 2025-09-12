
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


class BuildingComponent:
    """ Building object to keep track of the building materials flow (i.e., embodied energy component).

    Attributes
    ----------
    name : str
        Name of the building.
    building : Building Obj.
        Building to which the component belong.
    materials : list of ~pod_lca.building.BuildingMaterial
        Materials making up the component.
    service_life : float
        Service life of the component in years.
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
        """ Create a building component from its constituent materials.
        
        Parameters
        ----------
        name : str
            Name of the component.
        building : ~pod_lca.building.Building
            Building to which the component belong
        materials : list of material.Model  or Product Objs
            Materials making up the component.

        Returns
        -------
        ~pod_lca.building.BuildingComponent
            Building component created.
        """
        component = cls()

        component.set_name(name)
        if materials is not None:
            component.set_materials(materials)

        building.add_component(component)

        return component

    # ================================
    # Setters
    # ================================  
    def set_name(self, name):
        """ Set the name of the building component.

        Parameters
        ----------
        name : str
            Name of the building component.
        """
        self.name = name

        return self
    
    def set_building(self, building):
        """ Set the building of the component.
        
        Parameters
        ----------
        building : ~pod_lca.building.Building
            Building to which the component belong.
        """
        self.building = building

        return self
    
    def set_materials(self, materials):
        """ Set the materials constituiting the building component.
        
        Parameters
        ----------
        materials : list of ~pod_lca.building.BuildingMaterial
            Materials making up the component.
        """
        for material in materials:
            self.add_material(material)
        return self

    # ================================
    # Getters
    # ================================
    def get_name(self):
        """ Get the name of the building component.

        Returns
        -------
        str
            Name of the building component.
        """
        return self.name

    def get_building(self):
        """ Get the building of the component.
        
        Returns
        -------
        ~pod_lca.building.Building
            Building to which the component belong.
        """
        return self.building

    def get_materials(self):
        """ Get the materials constituiting the building component.
        
        Returns
        -------
        list of ~pod_lca.building.BuildingMaterial
            Materials making up the component.
        """
        return self.materials
    
    # ================================
    # Methods
    # ================================
    def add_material(self, material):
        """ Add a material to the building component.
        
        Parameters
        ----------
        material : ~pod_lca.building.BuildingMaterial
            Material from whcih the component is composed of.
        """
        self.materials.append(material)

        # TODO set A1-A3 impacts / material could be a Model object or a product
        # TODO: add a output product to material models
        return self

    # ================================
    # Transportation Methods
    # ================================ 
    def set_transportation_inward(self, material):

        pass # TODO: pick ProjectLogisticManager Obj. and set transportation link to each of the material inputs
             # and add them to the impacts directory of the components

    def set_transportation_outward(self, waste):

        pass # TODO: pick ProjectLogisticManager Obj. and set transportation link to each of the material inputs
             # and add them to the impacts directory of the components    

    # ================================
    # EOL Methods
    # ================================ 
    def get_eol_manager(self):
        """ Return the place where end-of-life transport dataset reside.
        """
        return self.get_building()

    def get_waste_products(self):
        """ Deconstruct the building component to waste products as specified in the deconstruction map.
        """
        eol_mix_data = DataImporter.csv_to_pandas(config['file_paths']['eol']['EOL_DEFAULT_MIXES'])
        waste_products = []
        for material in self.get_materials():
            eol_material = material.get_eol_material()
            waste_qty = material.get_weight()
            waste_unit = material.get_weight_unit()
            
            if eol_mix_data['Material'].isin([eol_material]).any():
                eol_mix = eol_mix_data[eol_mix_data['Material']== eol_material].drop(labels='Material', axis=1).to_dict(orient='records')[0] 
            elif  eol_mix_data['Material'].isin([config['setup']['eol']['EOL_DEFAULT_KEY']]).any():
                eol_mix = eol_mix_data[eol_mix_data['Material']== config['setup']['eol']['EOL_DEFAULT_KEY']].drop(labels='Material', axis=1).to_dict(orient='records')[0]
            else:
                log("A mix doesnt exist", 0)

            if material.get_bio_based() is not None:
                waste_obj = Waste.new(self, 
                                      database_item=eol_material, 
                                      qty=waste_qty, 
                                      unit=waste_unit, 
                                      process_mix=eol_mix, 
                                      bio_based=material.get_bio_based())
            else:
                waste_obj = Waste.new(self, 
                                        database_item=eol_material, 
                                        qty=waste_qty, 
                                        unit=waste_unit, 
                                        process_mix=eol_mix)
            waste_products.append(waste_obj)

        # delete data
        del eol_mix_data
        gc.collect()

        return waste_products


if __name__ == '__main__':
    pass
