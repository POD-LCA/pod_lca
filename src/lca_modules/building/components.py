from lca_modules.eol.waste import Waste
from lca_modules.eol import EOL_DEFAULT_MIXES
from utilities.data_imports.data_importer import Data_Importer
from lca_modules.eol import EOL_DEFAULT_KEY

import gc

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class BuildingComponent:
    """
    Building object to keep track of the building materials flow (i.e., embodied energy component).

    Attributes
    ----------
    name : str
        Name of the building.
    building : Building Obj.
        Building to which the component belong.
    materials : list of material.Model Objs. or Product Objs
        Materials making up the component.
    deconstructed_to : list of Waste Obj.
        Waste objects to which the component converted to at deconstruction and/or demolition.
    """
    def __init__(self):
        self.name = None
        self.building = None
        self.materials = []
        self.deconstructed_to = []

    # ================================
    # Constructors
    # ================================        
    @classmethod
    def create(cls, name, materials):
        """ Create a building component from its constituent materials.
        
            Parameters
            ----------
            name : str
                Name of the component.
            materials : list of material.Model Objs. or Product Objs
                Materials making up the component.

            Returns
            -------
            BuildingComponent Obj.
                Building component created.
        """

        component = cls()

        component.set_name(name)
        component.set_materials(materials)

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
            building : Building Obj.
                Building to which the component belong.
        """
        self.building = building

        return self
    
    def set_materials(self, materials):
        """ Set the materials constituiting the building component.
        
            Parameters
            ----------
            materials : list of material.Model Objs. or Product Objs
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
            Building Obj.
                Building to which the component belong.
        """
        return self.building

    def get_materials(self):
        """ Get the materials constituiting the building component.
        
            Returns
            -------
            list of material.Model Objs. or Product Objs
                Materials making up the component.
        """
        return self.materials
    
    def get_waste_products(self):
        """ Get the waste products the component was deconstructed/demolished to.
        """

        if self.deconstructed_to:
            return self.deconstructed_to
        else:
            raise ValueError(f"The component is not deconstructed and therefore no waste products exist.")
    
    # ================================
    # Methods
    # ================================
    def add_material(self, material):

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
    def deconstruct(self, deconstruction_map):
        """ Deconstruct the building component to waste products as specified in the deconstruction map.
        
            Parameters
            ----------
            deconstruction_map : dict
                Deconstruction map in the form of { End-of-Life product (str) : {'qty': (float), 'unit': (Unit Obj.)}}
        
        """
        eol_mix_data = Data_Importer.import_as_pandas(EOL_DEFAULT_MIXES)
        
        for key, value in deconstruction_map.items():
            if eol_mix_data['Material'].isin([key]).any():
                eol_mix = eol_mix_data[eol_mix_data['Material']== key].drop(labels='Material', axis=1).to_dict(orient='records')[0] 
            elif  eol_mix_data['Material'].isin([EOL_DEFAULT_KEY]).any():
                eol_mix = eol_mix_data[eol_mix_data['Material']== EOL_DEFAULT_KEY].drop(labels='Material', axis=1).to_dict(orient='records')[0]
            else:
                print("A mix doesnt exist") # TODO: test this sequence / shall a hardcode default set here

            if 'bio_based' in value.keys():
                waste_obj = Waste.new(self, database_item=key, qty=value['qty'], unit=value['unit'], process_mix=eol_mix, bio_based=value['bio_based'])
            else:
                waste_obj = Waste.new(self, database_item=key, qty=value['qty'], unit=value['unit'], process_mix=eol_mix)
            self.deconstructed_to.append(waste_obj)

        # delete data
        del eol_mix_data
        gc.collect()

        return self

if __name__ == '__main__':
    pass
