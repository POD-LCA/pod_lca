
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
    building : ~pod_lca.building.Building
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
    structural_walls : list of ~pod_lca.building_structure.Wall
        Structural walls in the structure.
    roof_structure : list of ~pod_lca.building_structure.RoofStructure
        Roof structure of the building.
    """

    def __init__(self):
        self.building = None
        self.structural_system = None
        self.structural_material = None
        self.foundations = []
        self.beams = []
        self.columns = []
        self.slabs = []
        self.structural_walls = []
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
        structure.set_building(building)

        bill_of_materials_all = DataImporter.csv_to_pandas(config['file_paths']['building']['TEMPLATE_BOM_STRUCTURE'])
        bill_of_materials = bill_of_materials_all[(bill_of_materials_all['building_type'].str.lower() == building_type.lower()) & 
                                                  (bill_of_materials_all['structure_type'].str.lower() == structure_type.lower())].drop(['building_type', 'structure_type'], axis=1).to_dict('index')
        if not bill_of_materials:
            log("The structure is empty.", 'warn')


        default_database_entry_map = DataImporter.csv_to_dict(config['file_paths']['building']['TEMPLATE_MATERIALS_DEFAULT_MAP'], 'template model material')

        column_foundation = Foundation.create('wall foundation', None)
        wall_foundation = Foundation.create('column foundation', None)
        slab_on_grade = Slab.create('slab on grade', None)
        elevated_slab = Slab.create('elevated slab', None)
        structural_beam = Beam.create('structural framing: beams', None)
        structural_girders = Beam.create('structural framing: girders', None)
        structural_columns = Column.create('structural walls', None)
        structural_walls = Wall.create('structural columns', None)
        roof_structure = RoofStructure.create('roof structure', None)

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
                name=item['material'] + '_in_' + building_assembly, 
                qty=float(item['qty']),
                unit=UNITS_MAP[item['unit']],
                material_database_entry=default_database_entry_map[item['material']]['impact database entry'],
                product_year=building.get_built_year()
            )
            
            assembly_obj.add_material(building_material)

        # add assemblies
        for assembly in [column_foundation,
                         wall_foundation,
                         slab_on_grade,
                         elevated_slab,
                         structural_beam,
                         structural_girders,
                         structural_columns,
                         structural_walls,
                         roof_structure]:
            if assembly.get_materials():
                structure.add_assembly(assembly)

        return structure

    @classmethod
    def from_geometry(cls, building):
        pass

    # ================================
    # Setters
    # ================================
    def set_building(self, parent):
        """ Set the parent building of the structure.
        
        Parameters
        ----------
        parent : ~pod_lca.building.Building
            The building to which the structure belong.
        """
        self.building = parent

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
    
    def get_assemblies(self):
        """ Get a list of all structural elements (i.e., structural assemblies) of the building.
        
        Returns
        -------
        list of ~pod_lca.building_structure.StructuralElement
            All the structural elements in the structure.
        """
        return  self.foundations + self.beams + self.columns + self.slabs
    
    # ================================
    # Add
    # ================================
    def add_assemblies(self, assemblies):
        """Add assemblies to the building structure.
        
        Parameters
        ----------
        assemblies : list of ~pod_lca.buildings.Assembly
            Assemblies to be added to the building structure.
        """
        for assembly in assemblies:
            self.add_assembly(assembly)

    def add_assembly(self, assembly):
        """Add assembly to the building structure.
        
        Parameters
        ----------
        assembly : ~pod_lca.buildings.Assembly
            Assembly to be added to the building structure.        
        """
        building = self.get_building()
        if building is not None:
            building.add_assembly(assembly)

        getattr(self, assembly.get_element_type()).append(assembly)
        assembly.set_service_life(assembly.get_service_life_category())

        for material in assembly.get_materials():
            material.set_service_life()
            material.set_properties_from_database()

        return self


if __name__ == '__main__':
    pass    
            