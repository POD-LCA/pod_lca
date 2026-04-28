
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class Structure:
    """ The definition of a structural floor.
    
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
    def create(cls, structural_material, floor_plan):
        """ Create a structure definition.
        
        Parameters
        ----------
        structural_material : {'Concrete', 'Steel', 'CLT'}
            Primary structural material of the building.
        floor_plan : ~pod_lca.building.BuildingFloor
            Building floor configuration.
        """
        structure = cls()

        structure.set_floor_plan(floor_plan)
        structure.set_structural_material(structural_material)

        floor_plan.set_structure(structure)

        return structure

    # ================================
    # Setters
    # ================================
    def set_floor_plan(self, floor_plan):
        """ Set floor plan of the structure.
        
        Parameters
        ----------
        floor_plan : ~pod_lca.building.BuildingFloor
            Building floor configuration.
        """
        self.floor_plan = floor_plan

    def set_structural_material(self, structural_material):
        """ Set structural material of the strucure
        
        Parameters
        ----------
        structural_material : {'Concrete', 'Steel', 'CLT'}
            Primary structural material of the building.
        """
        self.structural_material = structural_material

    # ================================
    # Getters
    # ================================
    def get_floor_plan(self):
        """ Get floor plan of the structure.
        
        Returns
        -------
        ~pod_lca.building.BuildingFloor
            Building floor configuration.
        """
        return self.floor_plan

    def get_structural_material(self):
        """ Get structural material of the strucure
        
        Returns
        -------
        str
            Primary structural material of the building.
        """
        return self.structural_material

    # ================================
    # Methods
    # ================================
    def update_structure(self, structural_element, **kwargs):
        """ Update the structure with the given structural element and its properties.

        Parameters
        ----------
        structural_element : str
            The type of structural element to update.
        **kwargs : dict
            Additional keyword arguments for the structural element.
        """
        if structural_element == "Slab":
            # Update slab properties
            pass
        elif structural_element == "Wall":
            # Update wall properties
            pass
        elif structural_element == "Roof":
            # Update roof properties
            pass


if __name__ == '__main__':
    pass    
            