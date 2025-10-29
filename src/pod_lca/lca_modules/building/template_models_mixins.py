
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
    def from_template_model(cls, name, location, built_year, life_span, **kwargs):
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

        Other Parameters
        ----------------
        building_type: {'residential', 'commercial'}
            Type of building.
        structure_type: str
            Template used for building structure. 
            The corresonding CSV file in data folder, named as 'TEMPLATE_BOM_PREFIX_{building-type}_{structure-type}.csv', will be used.
        enclosure-opaque: str
            Template used for building opaque enclosure.
            The corresonding CSV file in data folder, named as 'TEMPLATE_BOM_PREFIX_{building-type}_{enclosure-opaque}.csv', will be used.                                                                                                         
        enclosure-translucent: str
            Template used for building translucent enclosure.
            The corresonding CSV file in data folder, named as 'TEMPLATE_BOM_PREFIX_{building-type}_{enclosure-translucent}.csv', will be used.
        roof: str
            Template used for building roof enclosure.
            The corresonding CSV file in data folder, named as 'TEMPLATE_BOM_PREFIX_{building-type}_{roof}.csv', will be used.
        no_floors: int
            Number of floors in the building.
        floors_below_grade: int
            Number of floors below grade in the building.
        floor_plan: list of tuple of float
            List of (x, y) coordinates defining the floor plan of the building
        floor_area: float
            Total floor area of the building. If floor_plan is not provided, a square floor plan will be created based on the provided floor_area.
        f2f_height: float
            Floor to floor height of each story in the building.
        geometry_units: {'m', 'ft'}
            Units used for building geometry.
        wwr: float
            Window to wall ratio for the building façades.
        construction_energy_use: float
            Construction energy use for the building.
        construction_energy_use_unit: str
            Unit for construction energy use. E.g., 'MWh', 'kWh', etc
        building_standard : {'RICS', 'ASHRAE'}
            Standard used for service lives and waste rates. Default is 'ASHRAE'.
        logistic_type: {'Local', 'Global'}
            Logistic type for building material transportation. 
        
        Returns
        -------
        ~pod_lca.buildings.Building
            Building built.
        """
        building = cls.new(name,
                           type=kwargs['building_type'],
                           location=location, 
                           built_year=built_year, 
                           life_span=life_span)
        building.set_databases(kwargs.get('building_standard', 'ASHRAE'))

        building.set_template_model(**kwargs)

        return building
    
    # ================================
    # Setters
    # ================================   
    def set_template_model(self, **kwargs):
        """ Set attributes to an existing building.

        Other Parameters
        ----------------
        building_type: {'residential', 'commercial'}
            Type of building.
        structure_type: str
            Template used for building structure. 
            The corresonding CSV file in data folder, named as 'TEMPLATE_BOM_PREFIX_{building-type}_{structure-type}.csv', will be used.
        enclosure-opaque: str
            Template used for building opaque enclosure.
            The corresonding CSV file in data folder, named as 'TEMPLATE_BOM_PREFIX_{building-type}_{enclosure-opaque}.csv', will be used.                                                                                                         
        enclosure-translucent: str
            Template used for building translucent enclosure.
            The corresonding CSV file in data folder, named as 'TEMPLATE_BOM_PREFIX_{building-type}_{enclosure-translucent}.csv', will be used.
        roof: str
            Template used for building roof enclosure.
            The corresonding CSV file in data folder, named as 'TEMPLATE_BOM_PREFIX_{building-type}_{roof}.csv', will be used.
        no_floors: int
            Number of floors in the building.
        floors_below_grade: int
            Number of floors below grade in the building.
        floor_plan: list of tuple of float
            List of (x, y) coordinates defining the floor plan of the building
        floor_area: float
            Total floor area of the building. If floor_plan is not provided, a square floor plan will be created based on the provided floor_area.
        f2f_height: float
            Floor to floor height of each story in the building.
        geometry_units: {'m', 'ft'}
            Units used for building geometry.
        wwr: float
            Window to wall ratio for the building façades.
        construction_energy_use: float
            Construction energy use for the building.
        construction_energy_use_unit: str
            Unit for construction energy use. E.g., 'MWh', 'kWh', etc
        logistic_type: {'Local', 'Global'}
            Logistic type for building material transportation. 
        """
        # set default geometry
        no_floors = kwargs.get('no_floors', 1)
        if 'floor_plan' in kwargs:
            floor_plan = kwargs['floor_plan']
        else:
            if 'floor_area' in kwargs:
                side_length = sqrt(kwargs['floor_area'] / no_floors)
                floor_plan = [(0.0 , 0.0), (0.0, side_length), (side_length, side_length), (side_length, 0.0)]
            else:
                raise ValueError('Either floor plan or floor area must be provided to define the floor geometry.')
        geometry_units = kwargs.get('geometry_units', 'm')

        # set floors
        self.add_floors(no_floors=no_floors, 
                        floors_below_grade=kwargs.get('floors_below_grade', 0),
                        f2f_height=kwargs.get('f2f_height', 3.0 if geometry_units == 'm' else 10.0), 
                        floor_plan=floor_plan,
                        geometry_units=UNITS_MAP[geometry_units])
        
        # set building level products
        construction_energy_use = kwargs["construction_energy_use"] if "construction_energy_use" in kwargs else 0.0
        energy_units = UNITS_MAP[kwargs["construction_energy_use_unit"]] if "construction_energy_use" in kwargs else MEGA * WATT_HOUR
        self.set_building_level_products(logistic_type=kwargs.get('logistic_type', 'local'), 
                                         construction_electricity_consumption=construction_energy_use, 
                                         electricity_unit=energy_units)

        # building structure and envelope
        template_bom_file_name_prefix = config['setup']['building']['TEMPLATE_BOM_PREFIX'] + kwargs['building_type'] + '_'

        template_bom_path_structure = config['file_paths']['building']['TEMPLATE_BOM_FOLDER'] / (template_bom_file_name_prefix + kwargs['structure_type'] + '.csv')
        self.make_structure('from template', template_bom=template_bom_path_structure)
        
        # FIXME: decide on check... optional parameter in method.. or drop this altogether
        if self.run_eplus:
            operational_sys_path = config['file_paths']['operational']['SYSTEMS']
            self.make_envelope('from geometry', operational_sys_path=operational_sys_path)  
        else:
            template_bom_path_walls = config['file_paths']['building']['TEMPLATE_BOM_FOLDER'] / (template_bom_file_name_prefix + kwargs['enclosure-opaque'] + '.csv') if 'enclosure-opaque' in kwargs else None 
            template_bom_path_windows = config['file_paths']['building']['TEMPLATE_BOM_FOLDER'] / (template_bom_file_name_prefix + kwargs['enclosure-translucent'] + '.csv') if 'enclosure-translucent' in kwargs else None
            template_bom_path_roof = config['file_paths']['building']['TEMPLATE_BOM_FOLDER'] / (template_bom_file_name_prefix + kwargs['roof'] + '.csv') if 'roof' in kwargs else None   
            self.make_envelope('from template', 
                               template_bom_walls=template_bom_path_walls,
                               template_bom_windows=template_bom_path_windows,
                               template_bom_roof=template_bom_path_roof)

        return self


if __name__ == '__main__':
    pass
