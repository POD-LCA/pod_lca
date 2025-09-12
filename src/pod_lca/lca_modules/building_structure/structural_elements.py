
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..building import BuildingComponent


class StructuralElement(BuildingComponent):
    """ Super class for all types of structural elements.
    
    Attributes
    ----------
    floor :
        Floor to which the element belong.
    material : list of ~pod_lca.building.BuildingMaterial
        List of materials the building component made up of.
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
        structure.beams.append(beam)

        return beam

class Column(StructuralElement):

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, name, structure, materials):

        column = super().create(name, structure.get_parent(), materials)
        structure.columns.append(column)

        return column

class Slab(StructuralElement):

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, name, structure, materials):

        slab = super().create(name, structure.get_parent(), materials)
        structure.slabs.append(slab)

        return slab

if __name__ == '__main__':
    pass
