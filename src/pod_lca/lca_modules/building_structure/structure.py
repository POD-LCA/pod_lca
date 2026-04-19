
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class Structure:
    """ The configuration of a structural floor.
    
    Attributes
    ----------
    building : ~pod_lca.building.Building
        The building to which the structure belong.
    structural_material : {'Concrete', 'Steel', 'CLT'}
        Primary structural material of the building.
    floor_plan : ~pod_lca.building.BuildingFloor
        Building floor configuration.
    """

    def __init__(self):
        self.building = None
        self.structural_material = None
        self.floor_plan = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def create(cls, stype, floor_plan):
        structure = cls()

        structure.floor_plan = floor_plan
        structure.structural_material = stype

        floor_plan.set_structure(structure)

        return structure


if __name__ == '__main__':
    pass    
            