
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import GenericElement
from . import Foundation
from . import Beam
from . import Column
from . import Slab
from . import Wall
from . import RoofStructure
from . import StructuralMaterial
from ...units import UNITS_MAP, KILOGRAM, SQUARE_METER
from ...units import Quantity as Q
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
        self.unclassified = [] 
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
    def from_template(cls, building_type, structure_type):
        """ Create a structure from a template model.
        
        Parameters
        ----------
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
                    structural_element_obj = column_foundation
                case 'wall_foundation':
                    structural_element_obj = wall_foundation
                case 'slab_on_grade':
                    structural_element_obj = slab_on_grade
                case 'elevated_slabs' | 'floor_framing':
                    structural_element_obj = elevated_slab
                case 'structural_framing:_beams':
                    structural_element_obj = structural_beam
                case 'structural_framing:_girders':
                    structural_element_obj = structural_girders
                case 'structural_columns':
                    structural_element_obj = structural_columns
                case 'structural_walls':
                    structural_element_obj = structural_walls
                case 'roof_framing' | 'roof_decking':
                    structural_element_obj = roof_structure
                case _:
                    ValueError("Building assmebly not recognized.")

            building_material = StructuralMaterial.new(
                name=item['material'] + '_in_' + building_assembly, 
                qty=float(item['qty']),
                unit=UNITS_MAP[item['unit']],
                material_database_entry=default_database_entry_map[item['material']]['impact database entry'],
            )
            
            structural_element_obj.add_material(building_material)

        # add assemblies
        for structural_element in [column_foundation,
                         wall_foundation,
                         slab_on_grade,
                         elevated_slab,
                         structural_beam,
                         structural_girders,
                         structural_columns,
                         structural_walls,
                         roof_structure]:
            if structural_element.get_materials():
                structure.add_structural_element(structural_element)

        return structure

    @classmethod
    def from_geometry(cls, building):
        pass

    @classmethod
    def from_sample_buildings(cls, building_type, structure_type, mui_type):

        if structure_type == 'CLT':
            low, mid, high = 131, 38, 79

        elif building_type == 'Residential':
            if structure_type == 'Concrete':
                low, mid, high = 139, 170, 81
            elif structure_type == 'Light-Frame':
                low, mid, high = 142, 263, 84
            else:
                raise ValueError('{} in {} has not been yet implemented in this model'.format(building_type, structure_type))

        elif building_type == 'Commercial':
            if structure_type == 'Conrete':
                low, mid, high = 5, 93, 132
            elif structure_type == 'Steel':
                low, mid, high = 183, 179, 223
            else:
                raise ValueError('{} in {} has not been yet implemented in this model'.format(building_type, structure_type))
        else:
            raise ValueError('{} building type has not been yet implemented in this model'.format(building_type))

        path = config['file_paths']['building']['SAMPLE_BUILDING_STRUCTURES']
        sample_buildings = DataImporter.csv_to_pandas(path)
        low_building = sample_buildings[sample_buildings['project_index'] == low]
        

        structural_element_obj = GenericElement.create('generic structural element', None)
        # default_database_entry_map = DataImporter.csv_to_dict(config['file_paths']['building']['TEMPLATE_MATERIALS_DEFAULT_MAP'], 'template model material')

        floor_area = 100

        for _, row in low_building.iterrows():
            omniclass_element = row['omniclass_element']
            mat_type_podlca = row['mat_type_podlca']
            print(mat_type_podlca)
            mat_type = row['mat_type']
            mui_gfa = Q(row['mui_gfa'], KILOGRAM/SQUARE_METER)


            building_material = StructuralMaterial.new(
                name='{} {}'.format(omniclass_element, mat_type), 
                qty=floor_area * mui_gfa,
                unit=KILOGRAM,
                material_database_entry=mat_type_podlca,
            )

            structural_element_obj.add_material(building_material)

        structure = cls()
        structure.add_structural_element(structural_element_obj)

        return structure

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
    
    def get_structural_elements(self):
        """ Get a list of all structural elements (i.e., assemblies) of the building.
        
        Returns
        -------
        list of ~pod_lca.building_structure.StructuralElement
            All the structural elements in the structure.
        """
        return  self.foundations + self.beams + self.columns + self.slabs + self.structural_walls + self.roof_structure

    # ================================
    # Add
    # ================================
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
            