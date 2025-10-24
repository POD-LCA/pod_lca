
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Foundation
from . import Beam
from . import Column
from . import Slab
from . import Wall
from . import StructuralMaterial
from ...units import UNITS_MAP
from ...utilities import DataImporter
from ...utilities import config


class BuildingStructure:
    """ The structural assemblies of the building.
    
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
        default_database_entry_map = DataImporter.csv_to_dict(config['file_paths']['building']['TEMPLATE_MATERIALS_DEFAULT_MAP'], 'template model material')

        column_foundation = Foundation.create('wall foundation', structure, None)
        wall_foundation = Foundation.create('column foundation', structure, None)
        slab_on_grade = Slab.create('slab on grade', structure, None)
        elevated_slab = Slab.create('elevated slab', structure, None)
        structural_beam = Beam.create('structural framing: beams', structure, None)
        structural_girders = Beam.create('structural framing: girders', structure, None)
        structural_columns = Column.create('structural walls', structure, None)
        structural_walls = Wall.create('structural columns', structure, None)

        for key in bill_of_materials:
            item = bill_of_materials[key]
                
            building_assembly = item['assembly'].lower().replace(" ", "_")
            match building_assembly:
                case 'column_foundation':
                    assembly_obj = column_foundation
                case 'wall_foundation':
                    assembly_obj = wall_foundation
                case 'slab_on_grade':
                    assembly_obj = slab_on_grade
                case 'elevated_slabs':
                    assembly_obj = elevated_slab
                case 'structural_framing:_beams':
                    assembly_obj = structural_beam
                case 'structural_framing:_girders':
                    assembly_obj = structural_girders
                case 'structural_columns':
                    assembly_obj = structural_columns
                case 'structural_walls':
                    assembly_obj = structural_walls
                case _:
                    ValueError("Building assmebly not recognized.")

            building_material = StructuralMaterial.new(
                parent=assembly_obj,
                name=item['material'] + '_in_' + building_assembly, 
                qty=float(item['qty']),
                unit=UNITS_MAP[item['unit']],
                material_database_entry=default_database_entry_map[item['material']]['impact database entry'],
                product_year=building.get_built_year()
            )
            
            assembly_obj.add_material(building_material)

        # remove unused assembly
        del_list = [comp for comp in building.get_assemblies() if not comp.get_materials()]
        for assembly in del_list:
            building.remove_assembly(assembly)

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
    
    def get_assemblies(self):
        """ Get a list of all structural elements (i.e., structural assemblies) of the building.
        
        Returns
        -------
        list of ~pod_lca.building_structure.StructuralElement
            All the structural elements in the structure.
        """
        return  self.foundations + self.beams + self.columns + self.slabs
    

if __name__ == '__main__':
    pass    
            