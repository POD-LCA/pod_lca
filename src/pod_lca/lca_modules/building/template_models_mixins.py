
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from math import sqrt

from . import BuildingFloor
from ..building_envelope import Envelope
from ..building_structure import Structure
from ..building_structure import TemplateStructure
from ..building_envelope import BuildingEnvelope
from ..building_envelope import Envelope
from ...units import MEGA
from ...units import Quantity as Q
from ...units import WATT_HOUR
from ...units import UNITS_MAP
from ...utilities import config
from ...utilities import DataImporter


class TemplateModels:

    @classmethod
    def from_template_model(cls, name, location, built_year, life_span, **kwargs):
        """ Build a building from a template model data given in a CSV file.
        
        Parameters
        ----------
        name : str
            Name of the building.
        location : ~pod_lca.location.Location
            Location of the building site.
        built_year: int
            Built year of the building.
        life_span: int
            Life span of the building in years.

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
        run_eplus: bool
            Whether to run EnergyPlus simulation for operational energy modeling. Default is False.
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
        run_eplus: bool
            Whether to run EnergyPlus simulation for operational energy modeling. Default is False.
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
        geometry_data = DataImporter.json_to_dict(config["file_paths"]["building"]["TEMPLATE_GEOMETRY"])[kwargs['building_type']]
        no_floors = geometry_data.get('no_floors', 1)
        if 'floor_plan' in geometry_data:
            floor_plan = geometry_data['floor_plan']
        else:
            if 'floor_area' in geometry_data:
                side_length = sqrt(geometry_data['floor_area'] / no_floors)
                floor_plan = [(0.0 , 0.0), (0.0, side_length), (side_length, side_length), (side_length, 0.0)]
            else:
                raise ValueError('Either floor plan or floor area must be provided to define the floor geometry.')
        geometry_units = geometry_data.get('geometry_units', 'm')

        # set floors
        f2f_height = kwargs.get('f2f_height', 3.0 if geometry_units == 'm' else 10.0)
        floor_plan_poly = [(Q(coords[0], UNITS_MAP[geometry_units]),
                            Q(coords[1], UNITS_MAP[geometry_units])) for coords in floor_plan]
        floor = BuildingFloor.from_floor_plan(floor_plan=floor_plan_poly,
                                              floor_height=Q(f2f_height, UNITS_MAP[geometry_units]),
                                              usage=kwargs['building_type'])

        # set building level products
        construction_energy_use = kwargs["construction_energy_use"] if "construction_energy_use" in kwargs else 0.0
        energy_units = UNITS_MAP[kwargs["construction_energy_use_unit"]] if "construction_energy_use" in kwargs else MEGA * WATT_HOUR
        self.set_building_level_products(logistic_type=kwargs.get('logistic_type', 'local'), 
                                         construction_electricity_consumption=construction_energy_use, 
                                         electricity_unit=energy_units)

        # make structure and envelope
        self.make_template_structure(floor, no_floors, kwargs['structure_type'])
        self.make_template_envelope(floor, no_floors, kwargs['enclosure-opaque'], kwargs['enclosure-translucent'], kwargs['roof']) 

        return self
    
    def make_template_structure(self, floor, no_floors, structure_type):
        """ Make structure in a template model.
        
        Parameters
        ----------
        floor : ~pod_lca.building.BuildingFloor
            Floor representation of the template building.
        no_floors : int
            No of floors.
        structure_type : {'Concrete', 'Steel', 'CLT'}
            Major vertical gravity system of the structure.
        """
        structure = Structure.create(structure_type, floor)
        building_structure = TemplateStructure.create(structure, no_floors)
        
        building_structure.build()
        
        self.set_structure(building_structure)

    def make_template_envelope(self, floor, no_floors, envelope_opaque, envelope_translucent, roofing):
        """ Create the envelope of the building.
        
        Parameters
        ----------
        floor : ~pod_lca.building.BuildingFloor
            Floor representation of the template building.
        no_floors : int
            No of floors.
        envelope_opaque : {'Curtain wall: steel spandrel', 'Curtain wall: aluminum spandrel', 'MV - Brick', 'MV - Granite', 
                            'Insulated Metal Panel', 'EIFS (XPS)', 'Rainscreen, GFRC', 'Rainscreen, Thin Brick', 'Rainscreen, Wood', 'Rainscreen, Formed Steel Panel', 'Brick, wood framing'}
            Template used for building opaque enclosure.
        envelope_translucent : {'Glazing, double pane IGU', 'Glazing, triple pane IGU', 'Operable window', 'Glazing, operable window'}
            Template used for building translucent enclosure.
        roofing : {'EPDM roofing', 'Asphalt shingle roofing'}
            Template used for building roofing.        
        """
        e = Envelope.from_template(floor, envelope_opaque, envelope_translucent, roofing)
        buiilding_envelope = BuildingEnvelope.from_template_envelope(e, no_floors)

        self.set_building_envelope(buiilding_envelope)

        return self


if __name__ == '__main__':
    pass
