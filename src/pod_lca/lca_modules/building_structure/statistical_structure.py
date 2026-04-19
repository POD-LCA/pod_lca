
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import BuildingStructure
from . import GenericElement
from . import StructuralMaterial
from ...units import KILOGRAM
from ...units import Quantity as Q
from ...units import SQUARE_METER
from ...utilities import area_polygon
from ...utilities import config
from ...utilities import DataImporter


class StatisticalStructure(BuildingStructure):
    """ A structure based on statistical data of existing building stock in the USA."""

    def __init__(self):
        super().__init__()


    def build(self, mui_type):
        """ Build the structural material quantities from the data set.
        
        Parameters
        ----------
        mui_type : {'low', 'mid', 'high'}
            Material usage intensity of the structural components.
        """
        for data in self.get_structures().values() :
            structure = data["structure"]
            num = data["no_floors"]
    
            structure_type = structure.structural_material
            building_type = structure.floor_plan.usage
            floor_plan = structure.floor_plan.floor_plan

            sample_building = self.get_sample_building_data(building_type, structure_type, mui_type)
            
            structural_element_obj = GenericElement.from_materials('generic structural element', None)

            floor_area = area_polygon(floor_plan) * num

            for _, row in sample_building.iterrows():
                omniclass_element = row['omniclass_element']
                mat_type_podlca = row['mat_type_podlca']
                mat_type = row['mat_type']
                mui_gfa = Q(row['mui_gfa'], KILOGRAM/SQUARE_METER)

                quantity = floor_area * mui_gfa
                building_material = StructuralMaterial.new(
                    name='{} {}'.format(omniclass_element, mat_type), 
                    qty=quantity.value,
                    unit=quantity.unit,
                    material_database_entry=mat_type_podlca,
                )

                structural_element_obj.add_material(building_material)

            self.add_structural_element(structural_element_obj)

        return self
    
    def get_sample_building_data(self, building_type, structure_type, mui_type):
        """ Get sample building from the data set.
        
        Parameters
        ----------
        building_type : {'Residential', 'Commercial'}
            Usage type of building.
        structure_type : {'Concrete', 'Steel', 'Light-Frame'}
            Primary structural material of the structure.
        mui_type : {'low', 'mid', 'high'}
            Material usage intensity of the structural components.
        """
        if building_type == 'Residential':
            if structure_type == 'Concrete':
                low, mid, high = 139, 170, 81
            elif structure_type == 'Light-Frame':
                low, mid, high = 142, 263, 84
            elif structure_type == 'CLT':
                low, mid, high = 131, 38, 79
            else:
                raise ValueError('{} in {} has not been yet implemented in this model'.format(building_type, structure_type))

        elif building_type == 'Commercial':
            if structure_type == 'Conrete':
                low, mid, high = 5, 93, 132
            elif structure_type == 'Steel':
                low, mid, high = 183, 179, 223
            elif structure_type == 'CLT':
                low, mid, high = 131, 38, 79
            else:
                raise ValueError('{} in {} has not been yet implemented in this model'.format(building_type, structure_type))
        else:
            raise ValueError('{} building type has not been yet implemented in this model'.format(building_type))

        mui_map = {'low': low, 'high': high, 'mid': mid}

        path = config['file_paths']['building']['SAMPLE_BUILDING_STRUCTURES']
        sample_buildings = DataImporter.csv_to_pandas(path)
        sample_building = sample_buildings[sample_buildings['project_index'] == mui_map[mui_type]]

        return sample_building


if __name__ == '__main__':
    pass    
            