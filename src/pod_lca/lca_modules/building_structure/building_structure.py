
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class BuildingStructure:
    """ The structural assemblies of the building.
    
    Attributes
    ----------
    building : ~pod_lca.building.Building
        The building to which the structure belong.
    structures : dict of dict
        A dictionary of structures belonging to the building structure keyed by an id.
        Interior dict: {"structure": <`~pod_la.building_structure.Structure '>, "no_floors": <int>}
    structural_system :
        Major vertical gravity system of the structure.
    foundations : list of ~pod_lca.building_structure.Foundation
        Structural foundation elements.
    beams : list of ~pod_lca.building_structure.Beam
        Beam and other framing elements in the structure.
    columns : list of ~pod_lca.building_structure.Column
        Column elements in the structure.
    slabs : list of ~pod_lca.building_structure.Slab
        Floor slabs in the structure.
    structural_walls : list of ~pod_lca.building_structure.Wall
        Structural walls in the structure.
    roof_structure : list of ~pod_lca.building_structure.RoofStructure
        Roof structure of the building.
    unclassified : list of ~pod_lca.building_structure.StructuralElement
        Structural elements not classified under any of the above.
    """

    def __init__(self):
        self.building = None
        self.structures = {}
        self.structural_system = None
        
        # structural elements
        self.foundations = []
        self.beams = []
        self.columns = []
        self.slabs = []
        self.structural_walls = []
        self.roof_structure = []
        self.unclassified = [] 

    # ================================
    # Constructors
    # ================================
    @classmethod
    def create(cls, structures, no_floors):
        """ Create building structure from structure configurations.
        
        Parameters
        ----------
        structures : (list of) ~pod_la.building_structure.Structure 
            Definition  of the structure at floor levels
        no_floors : (list of) int
            Number of flows subject to the structure defintion.

        Returns
        -------
        ~pod_lca.building_structure.BuildingStructure
            The structure of the building
        """
        building_structure = cls()

        building_structure.set_structure(structures, no_floors)

        return building_structure
    
    # ================================
    # Setters
    # ================================
    def set_building(self, building):
        """ Set the parent building of the structure.
        
        Parameters
        ----------
        building : ~pod_lca.building.Building
            The building to which the structure belong.
        """
        self.building = building

        for structural_element in self.get_structural_elements():     
            structural_element.set_building()

        return self

    def set_structure(self, structures, no_floors):
        """ Set structure definitions of the building structure.

        Parameters
        ----------
        structures : (list of) ~pod_la.building_structure.Structure 
            Definition  of the structure at floor levels
        no_floors : (list of) int
            Number of flows subject to the structure defintion.
        """
        if not isinstance(structures, list):
            structures = [structures]
        if not isinstance(no_floors, list):
            no_floors = [no_floors]

        id = 0
        for structure, num in zip(structures, no_floors):
            self.structures[id] = {
                "structure": structure,
                "no_floors": num
            }
            id += 1

        return self
    # ================================
    # Getters
    # ================================
    def get_building(self):
        """ Get the parent building of the structure.
        
        Returns
        -------
        ~pod_lca.building.Building
            The building to which the structure belong.
        """
        return self.building
    
    def get_structures(self):
        """ Set structure definitions of the building structure.

        Returns
        -------
        dict of dict
            A dictionary of structures belonging to the building structure keyed by an id.
            Interior dict: {"structure": <`~pod_la.building_structure.Structure '>, "no_floors": <int>}            
        """
        return self.structures

    def get_structural_elements(self):
        """ Get a list of all structural elements (i.e., assemblies) of the building.
        
        Returns
        -------
        list of ~pod_lca.building_structure.StructuralElement
            All the structural elements in the structure.
        """
        return self.foundations + \
               self.beams + \
               self.columns + \
               self.slabs + \
               self.structural_walls + \
               self.roof_structure + \
               self.unclassified

    # ================================
    # Add
    # ================================
    def build(self):
        """ Build the building structure. (implemented at inherited classes)
        """
        pass

    def add_structural_elements(self, structural_elements):
        """Add assemblies to the building structure.
        
        Parameters
        ----------
        structural_elements : list of ~pod_lca.buildings.StructuralElement
            Structural elements to be added to the building structure.
        """
        for structural_element in structural_elements:
            self.add_structural_element(structural_element)

    def add_structural_element(self, structural_element):
        """Add structural element to the building structure.
        
        Parameters
        ----------
        structural_element : ~pod_lca.buildings.StructuralElement
            Assembly to be added to the building structure.        
        """
        getattr(self, structural_element.get_element_type()).append(structural_element)
        structural_element.set_parent(self)

        return self
    

if __name__ == '__main__':
    pass    
            