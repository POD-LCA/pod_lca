
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..building import Assembly
from ...utilities import config
from ...utilities import DataImporter


class StructuralElement(Assembly):
    """ Super class for all types of structural elements.
    
    Attributes
    ----------
    element_type : str
        Element type.
    floor :
        Floor to which the element belong.
    material : list of ~pod_lca.building.BuildingMaterial
        List of materials the building assembly made up of.
    geometry :
        Geometry of the structural element.
    supports :
        Supports of the structural element.
    loading : 
        Loading on the structural element.
    """

    def __init__(self):
        super().__init__()
        self.element_type = None
        self.floor = None
        self.material = None
        self.geometry = None
        self.supports = None
        self.loading = None

    @classmethod
    def from_template(cls, service_life, volume, materials):
        pass

    @classmethod
    def from_geometry(cls, geometry):
        pass

    @classmethod
    def create(cls, name, materials):
        """Create a structural element."""
        structural_element = super().create(name, materials)

        return structural_element
    
    def set_floor(self):
        pass

    def set_building(self):
        """Set data from building level."""
        building = self.get_building()
        if building is not None:
            building.add_assembly(self)
            self.set_service_life(self.get_service_life_category())

            for material in self.get_materials():
                material.set_building()

    def set_service_life(self, part):
        """ Set the service life of the assembly.

        Parameters
        ----------
        part : {'superstructure', 'substructure'}
            Part of the structure the assembly belongs to
        """
        building = self.get_building()
        if building is not None:
            building_standard = building.get_building_data_standard()

            match building_standard:
                case 'RICS':
                    data = DataImporter.csv_to_dict(config['file_paths']['building']['RICS_SERVICE_LIFE'], 'POD|LCA RSL Category')
                case 'ASHRAE':
                    data = DataImporter.csv_to_dict(config['file_paths']['building']['ASHRAE_SERVICE_LIFE'], 'POD|LCA RSL Category')

            service_life = data[part]['service_life']
            
            return super().set_service_life(service_life)
        else:
            return None
    
    def get_capacity(self):
        pass

    def size_member(self):
        pass

    def get_element_type(self):
        return self.element_type


class Foundation(StructuralElement):


    def __init__(self):
        super().__init__()
        self.service_life_category = "substructure"
        self.element_type = "foundations"


class LateralStabilitySystem(StructuralElement):

    def __init__(self):
        super().__init__()
        self.service_life_category = 'superstructure'


class Beam(StructuralElement):

    def __init__(self):
        super().__init__()
        self.service_life_category = 'superstructure'
        self.element_type = "beams"


class Column(StructuralElement):

    def __init__(self):
        super().__init__()
        self.service_life_category = 'superstructure'
        self.element_type = "columns"


class Slab(StructuralElement):

    def __init__(self):
        super().__init__()
        self.service_life_category = 'superstructure'
        self.element_type = "slabs"


class Wall(StructuralElement):

    def __init__(self):
        super().__init__()
        self.service_life_category = 'superstructure'
        self.element_type = "structural_walls"


class RoofStructure(StructuralElement):

    def __init__(self):
        super().__init__()
        self.service_life_category = 'superstructure'
        self.element_type = "roof_structure"


if __name__ == '__main__':
    pass
