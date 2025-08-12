
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import BuildingStructure


class ConcreteStructure(BuildingStructure):


    def __init__(self):
        self.structural_system = None
        self.structural_material = None
        self.foundation = []
        self.lateral_stability_system = []
        self.beams = []
        self.columns = []
        self.slabs = []


    @classmethod
    def from_geometry(cls, building):
        structure = cls()

        # TODO: write the logic of making the structure.


        return structure


if __name__ == '__main__':
    pass    
            