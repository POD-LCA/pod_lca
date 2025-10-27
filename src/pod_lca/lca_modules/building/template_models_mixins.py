
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from math import sqrt

from ...units import MEGA
from ...units import WATT_HOUR
from ...units import UNITS_MAP
from ...utilities import config


class TemplateModels:

    @classmethod
    def from_template_model(cls, name, location, built_year, life_span, building_data):
        """ Build a building from a template model data given in a CSV file.
        
        Parameters
        ----------
        name : str
            Name of the building.
        type : {'Commercial', 'Residential'}
            Type of building.
        location : ~pod_lca.location.Location
            Location of the building site.
        built_year: int
            Built year of the building.
        life_span: int
            Life span of the building in years.
        file_path : int
            File path to template model bill of material list.
        building_data : dict
            Dictionary provding building data
        env_constructions_path: str
            File path to envelope constructions IDF file
        operational_sys_path: str
            File path to operational systems IDF file
        
        Returns
        -------
        ~pod_lca.buildings.Building
            Building built.
        """
        building = cls.new(name,
                           type=building_data['building_type'],
                           location=location, 
                           built_year=built_year, 
                           life_span=life_span)
        building.set_databases()

        building.set_template_model(building_data)

        return building
    
    # ================================
    # Setters
    # ================================   
    def set_template_model(self, building_data):
        """ Set attributes to an existing building.

        Notes
        -----
        - If floor_plan is not provided, a square floor plan will be created based on the provided floor_area.

        Parameters
        ----------
        building_data : dict
            Dictionary provding building data
        """
        no_floors = building_data['no_floors'] if 'no_floors' in building_data else 1
        floors_below_grade = building_data['floors_below_grade'] if 'floors_below_grade' in building_data else 0
        geometry_units = building_data['geometry_units'] if 'geometry_units' in building_data else 'm'
        f2f_height = building_data['f2f_height'] if 'f2f_height' in building_data else 3.0 if geometry_units == 'm' else 10.0

        if 'floor_plan' in building_data:
            floor_plan = building_data['floor_plan']
        else:
            if 'floor_area' in building_data:
                side_length = sqrt(building_data['floor_area'])
                floor_plan = [(0.0 , 0.0), (0.0, side_length), (side_length, side_length), (side_length, 0.0)]
            else:
                raise ValueError('Either floor plan or floor area must be provided to define the floor geometry.')
            
        self.add_floors(no_floors=no_floors, 
                        floors_below_grade=floors_below_grade,
                        f2f_height=f2f_height, 
                        floor_plan=floor_plan,
                        geometry_units=UNITS_MAP[geometry_units])
        
        construction_energy_use = building_data["construction_energy_use"] if "construction_energy_use" in building_data else 0.0
        energy_units = UNITS_MAP[building_data["construction_energy_use_unit"]] if "construction_energy_use" in building_data else MEGA * WATT_HOUR
        self.set_building_level_products(logistic_type=building_data['logistic_type'], 
                                         construction_electricity_consumption=construction_energy_use, 
                                         electricity_unit=energy_units)

        template_bom_file_name_prefix = config['setup']['building']['TEMPLATE_BOM_PREFIX'] + building_data['building_type'] + '_'

        template_bom_path_structure = config['file_paths']['building']['TEMPLATE_BOM_FOLDER'] / (template_bom_file_name_prefix + building_data['structure_type'] + '.csv')
        self.make_structure('from template', template_bom=template_bom_path_structure)
        
        # FIXME: decide on check... optional parameter in method.. or drop this altogether
        if self.run_eplus:
            operational_sys_path = config['file_paths']['operational']['SYSTEMS']
            self.make_envelope('from geometry', operational_sys_path=operational_sys_path)  
        else:
            template_bom_path_walls = config['file_paths']['building']['TEMPLATE_BOM_FOLDER'] / (template_bom_file_name_prefix + building_data['enclosure-opaque'] + '.csv')   
            template_bom_path_windows = config['file_paths']['building']['TEMPLATE_BOM_FOLDER'] / (template_bom_file_name_prefix + building_data['enclosure-translucent'] + '.csv')       
            self.make_envelope('from template', 
                               template_bom_walls=template_bom_path_walls,
                               template_bom_windows=template_bom_path_windows)

        return self


if __name__ == '__main__':
    pass
