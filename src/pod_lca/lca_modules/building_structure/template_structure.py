
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import BuildingStructure
from . import Beam
from . import Column
from . import Foundation
from . import RoofStructure
from . import Slab
from . import StructuralMaterial
from . import Wall
from ...units import UNITS_MAP
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class TemplateStructure(BuildingStructure):
    """ A structure based on POD|LCA template models."""

    def __init__(self):
        super().__init__()


    def build(self):
        """ Build the structure material quantities from a template model.

        Notes
        -----
        Templates have precalculated material quantities.
        """
        building_usage_type = self.structures[0]["structure"].get_floor_plan().get_usage()
        structure_type = self.structures[0]["structure"].get_structural_material()

        bill_of_materials = self.get_template_boq(building_usage_type, structure_type)

        default_database_entry_map = DataImporter.csv_to_dict(config['file_paths']['building']['TEMPLATE_MATERIALS_DEFAULT_MAP'], 'template model material')

        column_foundation = Foundation.from_materials('wall foundation', None)
        wall_foundation = Foundation.from_materials('column foundation', None)
        slab_on_grade = Slab.from_materials('slab on grade', None)
        elevated_slab = Slab.from_materials('elevated slab', None)
        structural_beam = Beam.from_materials('structural framing: beams', None)
        structural_girders = Beam.from_materials('structural framing: girders', None)
        structural_columns = Column.from_materials('structural walls', None)
        structural_walls = Wall.from_materials('structural columns', None)
        roof_structure = RoofStructure.from_materials('roof structure', None)

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
                self.add_structural_element(structural_element)

        return self
    
    def get_template_boq(self, building_usage_type, structure_type):
        """ Get the Bill of Quantities from POD|LCA template model.

        Notes
        -----
        The corresonding CSV file in data folder, named as 'TEMPLATE_BOM_PREFIX_{building-type}_{structure-type}.csv', will be used.

        Parameters
        ----------
        building_usage_type: {'residential', 'commercial'}
            Usage type of building.
        structure_type: str
            for building type;
            - 'commercial' : {'BP_Steel'. 'LS_steel', 'SS_Steel', "BP_Concrete', 'LS_Concrete', 'SS_Concrete', 'BP_Wood', 'LS_Wood', 'SS_Wood'}
            - 'residential' : {"doe_prototype"}
        """
        bill_of_materials_all = DataImporter.csv_to_pandas(config['file_paths']['building']['TEMPLATE_BOM_STRUCTURE'])
        bill_of_materials = bill_of_materials_all[(bill_of_materials_all['building_type'].str.lower() == building_usage_type.lower()) & 
                                                  (bill_of_materials_all['structure_type'].str.lower() == structure_type.lower())].drop(['building_type', 'structure_type'], axis=1).to_dict('index')
        if not bill_of_materials:
            log("The structure is empty.", 'warn')
        
        return bill_of_materials


if __name__ == '__main__':
    pass    
            