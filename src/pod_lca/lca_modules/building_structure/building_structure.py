
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
from . import RoofStructure
from . import StructuralMaterial
from ...units import UNITS_MAP
from ...utilities import DataImporter
from ...utilities import config
from ...utilities import log


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
        self.roof_structure = []

    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_template(cls, building, building_type, structure_type):
        """ Create a structure from a template model.
        
        Parameters
        ----------
        building : ~pod_lca.building.Building
            Building for which the structure belong.
        building_type : {'Commercial', 'Residential'}
            Type of building.
        structure_type : {'BP_Steel'. 'LS_steel', 'SS_Steel', "BP_Concrete', 'LS_Concrete', 'SS_Concrete', 'BP_Wood', 'LS_Wood', 'SS_Wood'}
            Template used for building structure.  

        Returns
        -------
        ~pod_lca.building_structure.BuildingStructure
            Structure created.
        """
        structure = cls()
        structure.set_parent(building)

        bill_of_materials_all = DataImporter.csv_to_pandas(config['file_paths']['building']['TEMPLATE_BOM_STRUCTURE'])
        bill_of_materials = bill_of_materials_all[(bill_of_materials_all['building_type'].str.lower() == building_type.lower()) & 
                                                  (bill_of_materials_all['structure_type'].str.lower() == structure_type.lower())].drop(['building_type', 'structure_type'], axis=1).to_dict('index')
        if not bill_of_materials:
            log("The structure is empty.", 'warn')


        default_database_entry_map = DataImporter.csv_to_dict(config['file_paths']['building']['TEMPLATE_MATERIALS_DEFAULT_MAP'], 'template model material')

        column_foundation = Foundation.create('wall foundation', structure, None)
        wall_foundation = Foundation.create('column foundation', structure, None)
        slab_on_grade = Slab.create('slab on grade', structure, None)
        elevated_slab = Slab.create('elevated slab', structure, None)
        structural_beam = Beam.create('structural framing: beams', structure, None)
        structural_girders = Beam.create('structural framing: girders', structure, None)
        structural_columns = Column.create('structural walls', structure, None)
        structural_walls = Wall.create('structural columns', structure, None)
        roof_structure = RoofStructure.create('roof structure', structure, None)

        for item in bill_of_materials.values():
                
            building_assembly = item['assembly'].lower().replace(" ", "_")
            match building_assembly:
                case 'column_foundation' | 'concrete_footing':
                    assembly_obj = column_foundation
                case 'wall_foundation':
                    assembly_obj = wall_foundation
                case 'slab_on_grade':
                    assembly_obj = slab_on_grade
                case 'elevated_slabs' | 'floor_framing':
                    assembly_obj = elevated_slab
                case 'structural_framing:_beams':
                    assembly_obj = structural_beam
                case 'structural_framing:_girders':
                    assembly_obj = structural_girders
                case 'structural_columns':
                    assembly_obj = structural_columns
                case 'structural_walls':
                    assembly_obj = structural_walls
                case 'roof_framing' | 'roof_decking':
                    assembly_obj = roof_structure
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
            