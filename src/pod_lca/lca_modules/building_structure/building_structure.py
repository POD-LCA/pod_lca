
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Foundation
from . import Beam
from . import Column
from . import Slab
from ..building import BuildingMaterial
from ...utilities import DataImporter
from ...units import UNITS_MAP


class BuildingStructure:
    """ The structural components of the building.
    
    Attributes
    ----------
    parent : ~pod_lca.building.Building
        The building to which the structure belong.
    structural_system :
        Major vertical gravity system of the structure.
    structural_material : {'Concrete', 'Steel', 'CLT'}
        Primary structural material of the building.
    foundations : list of ~pod_lca.building_structure.Foundation
        Structural foundation elements.
    beams : list of ~pod_lca.building_structure.Beam
        Beam and other framing elements in the structure.
    columns : list of ~pod_lca.building_structure.Column
        Column elements in the structure.
    slabs : list of ~pod_lca.building_structure.Slab
        Floor slabs in the structure.
    """

    def __init__(self):
        self.parent = None
        self.structural_system = None
        self.structural_material = None
        self.foundations = []
        self.beams = []
        self.columns = []
        self.slabs = []

    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_template(cls, building, bom_file_path):
        """ Create a structure from a template model.
        
        Parameters
        ----------
        building : ~pod_lca.building.Building
            Building for which the structure belong.
        bom_file_path : str
            File path to bill of materials

        Returns
        -------
        ~pod_lca.building_structure.BuildingStructure
            Structure created.
        """
        structure = cls()
        structure.set_parent(building)

        bill_of_materials = DataImporter.csv_to_dict(bom_file_path)

        superstructure_floors = Slab.create('superstructure floors', structure, None)
        substructure_floors = Slab.create('substructure floors', structure, None)
        columns = Column.create('columns', structure, None)
        beams = Beam.create('structural framing', structure, None)
        foundation = Foundation.create('structural foundation', structure, None)

        for key in bill_of_materials:
            item = bill_of_materials[key]
            if item['Building Component'] in ['Structure', 'Superstructure', 'Substructure']:
                building_element = item['Building element']
                building_material = BuildingMaterial.new_structural_material(parent=structure,
                                                                             name=item['material'] + '_in_' + building_element, 
                                                                             qty=float(item['qty']),
                                                                             unit=UNITS_MAP[item['unit']],
                                                                             material_database_entry=item['material'])
                
                if building_element in ['Structural Foundations']:
                    component_obj = foundation
                elif building_element in ["Structural Framing"]:
                    component_obj = beams
                elif building_element in ["Structural Columns"]:
                    component_obj = columns
                elif building_element in ["Floors"]:
                    if item['Building Component'] in ["Superstructure"]:
                        component_obj = superstructure_floors
                    elif item['Building Component'] in ["Substructure"]:
                        component_obj = substructure_floors
                    else:
                        raise NotImplementedError
                else:
                    raise NotImplementedError
                    
                component_obj.add_material(building_material)

        return structure

    @classmethod
    def from_geometry(cls, building):
        pass

    # ================================
    # Setters
    # ================================
    def set_parent(self, parent):
        """ Set the parent building of the structure.
        
        Parameters
        ----------
        parent : ~pod_lca.building.Building
            The building to which the structure belong.
        """
        self.parent = parent

        return self

    # ================================
    # Getters
    # ================================
    def get_parent(self):
        """ Get the parent building of the structure.
        
        Returns
        -------
        ~pod_lca.building.Building
            The building to which the structure belong.
        """
        return self.parent
    
    def get_components(self):
        """ Get a list of all structural elements (i.e., structural components) of the building.
        
        Returns
        -------
        list of ~pod_lca.building_structure.StructuralElement
            All the structural elements in the structure.
        """
        return  self.foundations + self.beams + self.columns + self.slabs
    

if __name__ == '__main__':
    pass    
            