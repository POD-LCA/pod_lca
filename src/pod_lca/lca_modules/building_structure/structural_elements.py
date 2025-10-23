
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

    def set_floor(self):
        pass

    def set_service_life(self, part):
        """ Set the service life of the assembly.

        Parameters
        ----------
        part : {'superstructure', 'substructure'}
            Part of the structure the assembly belongs to
        """
        building = self.get_building()
        building_standard = building.get_building_data_standard()

        match building_standard:
            case 'RICS':
                data = DataImporter.csv_to_dict(config['file_paths']['building']['RICS_SERVICE_LIFE'], 'POD|LCA RSL Category')
            case 'ASHRAE':
                data = DataImporter.csv_to_dict(config['file_paths']['building']['ASHRAE_SERVICE_LIFE'], 'POD|LCA RSL Category')

        service_life = data[part]['service_life']
        
        return super().set_service_life(service_life)

    def get_capacity(self):
        pass

    def size_member(self):
        pass


class Foundation(StructuralElement):


    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, name, structure, materials):

        foundation_element = super().create(name, structure.get_parent(), materials)
        foundation_element.set_service_life('substructure')
        structure.foundations.append(foundation_element)

        return foundation_element

class LateralStabilitySystem(StructuralElement):

    def __init__(self):
        super().__init__()

class Beam(StructuralElement):

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, name, structure, materials):

        beam = super().create(name, structure.get_parent(), materials)
        beam.set_service_life('superstructure')
        structure.beams.append(beam)

        return beam

class Column(StructuralElement):

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, name, structure, materials):

        column = super().create(name, structure.get_parent(), materials)
        column.set_service_life('superstructure')
        structure.columns.append(column)

        return column

class Slab(StructuralElement):

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, name, structure, materials):

        slab = super().create(name, structure.get_parent(), materials)
        slab.set_service_life('superstructure')
        structure.slabs.append(slab)

        return slab

class Wall(StructuralElement):

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, name, structure, materials):

        wall = super().create(name, structure.get_parent(), materials)
        wall.set_service_life('superstructure')
        structure.columns.append(wall)

        return wall
    
if __name__ == '__main__':
    pass
