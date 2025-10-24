
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import ConstructionMixins
from . import DataMixins
from . import EndOfLifeMixins
from . import EnvelopeMixins
from . import Floor
from . import OperationalMixins
from . import ProductScopeMixins
from . import Scenario
from . import TemplateModels
from . import TransportationMixins
from . import UseMixins
from ..building_envelope import Envelope
from ..building_structure import BuildingStructure
from ..building_structure import ConcreteStructure
from ..dynamic_radiative_forcing import DynamicRadiativeForcingRecord
from ...units import MEGA
from ...units import METER
from ...units import WATT_HOUR
from ...utilities import centroid
from ...utilities import geometric_key
from ...utilities import config


class Building (TemplateModels, DataMixins, EndOfLifeMixins, OperationalMixins, UseMixins, ConstructionMixins, TransportationMixins, ProductScopeMixins, EnvelopeMixins):
    """ Building object to keep track of the building materials flow (i.e., embodied energy assembly).

    Attributes
    ----------
    name : str
        Name of the building.
    building_type : {'Commercial', 'Residential'}
        Type of building.
    structure_type : {'Concrete', 'Steel', 'CLT'}
        Major vertical gravity system of the structure.
    built_year: int
        Built year of the building.
    location : ~pod_lca.location.Location
        Location of the building site.
    assemblies : list of ~pod_lca.building.Assembly 
        Structural and Fascade elements that make up the building.
    material_impact_database: ~pod_lca.impacts.ImpactsDatabase
        Buildin material impact database.
    transport_impact_database : ~pod_lca.impacts.TranportationModeImpactsDatabase
        Impact database of transportation modes.
    eol_impact_database : ImpactsDatabase Obj.
        Impacts related to end of life processes.
    eol_transport_dataset: ~pod_lca.transportation.TransportDataset
        End-of-life transportation dataset.
    transportation_manager: ~pod_lca.transportation.TransportationManager
        Manager of inward transportation of material for the construction of the building.
    construction_energy_product : 

    building_data_standard: {'RICS', 'ASHRAE'}
        building strnadard used for 

    """

    def __init__(self):
        self.name = None
        self.building_type = None
        self.structure_type = None
        self.built_year = None
        self.life_span = None
        self.location = None

        self.floors = {}
        self.structure = None
        self.envelope = None
        self.operational_object = None
        self.assemblies = []
        self.surface_cpt_dict = {}
        self.constructions = {}

        self.material_impact_database = None
        self.transport_impact_database = None
        self.eol_impact_database = None
        self.eol_transport_dataset = None
        self.transportation_manager = None
        self.building_data_standard = None

        self.construction_energy_product = None
        self.operational_energy_product = None

        self.run_eplus = False
        self.idf_constructions_data = {}
        self.idf_material_properties = {}
        self.energy_plus_results = None
        self.energy_plus_units = None

        self.scenarios = {}

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, name, type, location, built_year, life_span):
        """ Build a building.
        
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

        Returns
        -------
        ~pod_lca.buildings.Building
            Building built.
        """    
        building = cls()

        building.set_name(name)
        building.set_building_type(type)
        building.set_location(location)
        building.set_built_year(built_year)
        building.set_life_span(life_span)

        return building
     
    @classmethod
    def from_parameters(cls, name, type, location, built_year, life_span, no_floors, f2f_height, floor_plan, floors_below_grade=None, geometry_units=METER, logistic_type='local'):
        """ Build a building.
        
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
        no_floors : int
            Number of floors in the building.
        f2f_height : float
            Floor to floor height.
        floor_plan : list of tuples of float
            A polygon defining the floor plan geometry [(x1, y1), (x2, y2), ... , (xn, yn)].
        floors_below_grade : int
            Number of floors below grade.
        geometry_units : ~pod_lca.units.Unit
            Unit of measurement used in geometry definitions.
        logistic_type : {'local', 'global'}
            Transportation scope of the building material in construction.
        # TODO: move above to kwargs
        # TODO: add building data standard to kwargs
        
        Returns
        -------
        ~pod_lca.buildings.Building
            Building built.
        """
        building = cls.new(name, type, location, built_year, life_span)
        building.set_databases()
        building.set_building_level_products(logistic_type)

        if floors_below_grade is None:
            if no_floors > 2:
                floors_below_grade = 1
            else:
                floors_below_grade = 0

        building.add_floors(no_floors, f2f_height, floor_plan, floors_below_grade, geometry_units)

        building.make_structure('from geometry')
        building.make_envelope()

        return building

    @classmethod
    def from_geometry(cls, name, type, location, built_year, life_span, geometry, logistic_type='local'):
        """ Build a building.
        
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
        geometry : 
            Geometry details of the building
        logistic_type : {'local', 'global'}
            Transportation scope of the building material in construction.

        Returns
        -------
        ~pod_lca.building.Building
            Building built.
        """
        building = cls.new(name, type, location, built_year, life_span)
        building.set_databases()
        building.set_building_level_products(logistic_type)

        building.make_structure()
        building.make_envelope()

        return building
    
    # ================================
    # Setters
    # ================================     
    def set_name(self, name):
        """ Set name of the building.
        
        Parameters
        ----------
        name : str
            Name of the building.
        """
        self.name =  name

        return self
    
    def set_building_type(self, building_type):
        """ Set building type.
        
        Parameters
        ----------
        type : {'Commercial', 'Residential'}
            Type of building.
        """
        self.building_type = building_type

        return self

    def set_structure_type(self, structure_type):
        """ Set the major vertical gravity system of the structure
        
        Parameters
        ----------
        structure_type : {'Concrete', 'Steel', 'CLT'}
            Major vertical gravity system of the structure.
        """
        self.structure_type = structure_type

        return self
        
    def set_built_year(self, year):
        """ Set built year of the building.
        
        Parameters
        ----------
        year: int
            Built year of the building.
        """
        self.built_year = year

        return self
    
    def set_life_span(self, life_span):
        """ Set life span of the building.
        
        Parameters
        ----------
        life_span: int
            Life span of the building in years.
        """
        self.life_span = life_span

        return self

    def set_location(self, location):
        """ Set location of the building site.
        
        Parameters
        ----------
        location : Location Obj.
            Location of the building site.
        """
        self.location = location

        return self
    
    def set_building_data_standard(self, standard):
        """ Set standard used for service lives and waste rates.
        
        Parameters
        ----------
        standard: {'RICS', 'ASHRAE'}
            building strnadard used for 
        """
        self.building_data_standard = standard
    
    def set_scenario(self, name):
        """ Create new scenario for the building.
        
        Parameters
        ----------
        name : str
            Name of the building scenario.
        """
        scenario = Scenario.new(self)

        self.scenarios[name] = scenario

        return scenario

    def set_databases(self):
        """ Set databases and datasets to be used in the LCA computations.
        """
        self.set_material_database()
        self.set_transportation_mode_impact_database()
        self.set_eol_process_impact_database()
        self.set_eol_demolition_impact_database()
        self.set_eol_transport_dataset()
        self.set_building_data_standard(config['setup']['building']['DEFAULT_DATA_STANDARD'])

        return self
    
    def set_building_level_products(self, logistic_type='domestic', construction_electricity_consumption=0.0, electricity_unit=MEGA * WATT_HOUR):
        """ Set building level products used for LCA calculations.
        
        Parameters
        ----------
        logistic_type : {'domestic', 'global'}
            Type of logistic management used for A4 transportation.
        construction_electricity_consumption : float
            Amount of electricity consumed in construction activities.
        electricity_unit : ~pod_lca.units.Unit
            Unit of measurement used for electricity consumption.
        """
        self.set_transportation_manager()
        self.set_operational_electricity_product(electricity_unit)
        self.set_construction_energy_product(construction_electricity_consumption, electricity_unit)

        return self
    # ================================
    # Getters
    # ================================
    def get_name(self):
        """ Get name of the building.
        
        Returns
        -------
        str
            Name of the building.
        """
        return self.name

    def get_building_type(self):
        """ Get building type.
        
        Returns
        -------
        str
            Type of building.
        """
        return self.building_type

    def get_structure_type(self):
        """ Get the major vertical gravity system of the structure
        
        Returns
        -------
        str
            Major vertical gravity system of the structure.
        """
        return self.structure_type
    
    def get_location(self):
        """ Get location of the building site.
        
        Returns
        -------
        ~pod_lca.location.Location
            Location of the building site.
        """
        return self.location
    
    def get_built_year(self):
        """ Get built year of the building.
        
        Returns
        -------
        int
            Built year of the building.

        """
        return self.built_year

    def get_life_span(self):
        """ Get life span of the building.
        
        Returns
        -------
        int
            Life span of the building in years.
        """
        return self.life_span

    def get_building_data_standard(self):
        """ Get standard used for service lives and waste rates.
        
        Returns
        -------
        str
            building strnadard used for 
        """
        return self.building_data_standard

    def get_floor(self, floor_no):
        """ Get the floor specified.

        Parameters
        ----------
        floor_no : int
            Floor id
        """
        return self.floors[str(floor_no)]
    
    def get_no_floors(self):
        """ Get number of floors in the building.
        """
        return len(self.floors)

    def get_structure(self):

        return self.structure
    
    def get_envelope(self):

        return self.envelope

    def get_assemblies(self):
        """ Get a list of building assemblies.

        Returns
        -------
        list of ~pod_lca.building.Assembly
            Structural and Fascade elements that make up the building.
        """
        return self.assemblies

    def get_scenario(self, name):
        """ Retrieve a building scenario.
        
        Parameters
        ----------
        name : str
            Name of the building scenario.
        """
        return self.scenarios[name]
    
    # ================================
    # Assembly Methods
    # ================================ 
    def add_floors(self, no_floors, f2f_height, floor_plan, floors_below_grade, geometry_units):
        """ Add floors to the building.
        
        Parameters
        ----------
        no_floors : int
            Number of floors in the building.
        f2f_height : float
            Floor to floor height.
        floor_plan : list of tuples of float
            A polygon defining the floor plan geometry [(x1, y1), (x2, y2), ... , (xn, yn)].
        floors_below_grade : int
            Number of floors below grade.
        geometry_units : ~pod_lca.units.Unit
            Unit of measurement used in geometry definitions.        
        """
        for num in range(no_floors):
            z = (f2f_height * num) - (floors_below_grade * f2f_height)
            floor_plan_poly = [(coords[0], coords[1], z) for coords in floor_plan]

            floor_no = num +1
            below_grade = True if floor_no <= floors_below_grade else False
            on_ground = True if floor_no == floors_below_grade + 1 else False
            is_last = True if floor_no == no_floors else False
            self.add_floor(floor_no, floor_plan_poly, f2f_height, geometry_units, below_grade, on_ground, is_last)

        return self

    def add_floor(self, floor_no, floor_plan, floor_height, geometry_unit, below_grade, on_ground, is_last):
        """ Add a floor to the building.

        Parameters
        ----------      
        floor_no : int
            Floor number. 
        floor_plan : list of tuples of float
            A polygon defining the floor plan geometry [(x1, y1, z), (x2, y2, z), ... , (xn, yn, z)].  
        floor_height : float
            Floor height.   
        geometry_unit : ~pod_lca.units.Unit
            Unit of measurement     
        below_grade : bool
            True, if the floor is above grade.
        on_ground : bool
            True, if the floor is on the ground.
        is_last : bool

        """
        floor = Floor.from_floor_plan(floor_no, floor_plan, floor_height, geometry_unit)
        floor.is_last = is_last

        if below_grade:
            floor.set_floor_below_grade()
        if on_ground:
            floor.set_floor_on_ground()

        self.floors[str(floor_no)] = floor
        
        return self

    def make_structure(self, method, **kwargs):
        """ Create the structure of the building.
        
        Parameters
        ----------
        method : {'from geometry', 'from template'}
            Method of structure generation.

        Other Parameters
        ----------------
        template_bom : str
            File path to the bill-of-materials of the template model.            
        """
        structure_type = self.get_structure_type()

        if structure_type == 'Concrete':
            structure_obj = ConcreteStructure
        else:
            structure_obj = BuildingStructure

        if method == 'from geometry':
            structure = structure_obj.from_geometry(self)
        elif method == 'from template':
            structure = structure_obj.from_template(self, kwargs['template_bom'])
        else:
            raise ValueError('Method of creating structure is not recognized.')
        
        self.structure = structure

        return self

    def make_envelope(self,  method, **kwargs):
        """ Create the envelope of the building.
        
        Parameters
        ----------
        method : {'from geometry', 'from template'}
            Method of structure generation.

        Other Parameters
        ----------------
        template_bom_walls : str
            File path to the bill-of-materials of the template model for opaque enclosure.
        template_bom_windows : str
            File path to the bill-of-materials of the template model for transparent enclosure.
        operational_sys_path: str
            File path to operational systems IDF file.         
        """
        if method == 'from geometry':
            self.read_constructions_data()
            self.read_material_properties_data()
            # FIXME: consolidate the different thinkings in envelope by geometry and from template
            envelope = self.create_envelopes_from_template(kwargs['operational_sys_path'])
        elif method == 'from template':
            envelope = Envelope.from_template(self, kwargs['template_bom_walls'], kwargs['template_bom_windows'])
        else:
            raise ValueError('Method of creating envelope is not recognized.')
        
        
        
        self.envelope = envelope

        return self

    def add_assembly(self, assembly):
        """ Add a assembly to the building.
        
        Parameters
        ----------
        assembly : ~pod_lca.building.Assembly
            Structural or envelope element to be added to the building.
        """
        self.get_assemblies().append(assembly)
        assembly.set_building(self)

        return self
    
    def remove_assembly(self, assembly):
        """ Remove assembly from a building.

        Parameters
        ----------
        assembly : ~pod_lca.building.Assembly
            Structural or envelope element to be removed from the building."""
        self.get_assemblies().remove(assembly)

    def update_envelope_surfaces(self):
        for fk in self.floors:
            floor = self.floors[fk]
            for sk in floor.envelope.surfaces:
                srf = floor.envelope.surfaces[sk]
                if 'wall' in sk:
                    if floor.is_below_grade:
                        srf.outside_boundary_condition = 'Ground'
                    else:
                        srf.outside_boundary_condition = 'Outdoors'
                elif sk == 'floor':
                    if floor.is_on_ground:
                        srf.outside_boundary_condition = 'Ground'
                    else:
                        srf.outside_boundary_condition = 'Adiabatic'
                elif sk == 'ceiling':
                    if floor.is_last:
                        srf.outside_boundary_condition = 'Outdoors'
                    else:
                        srf.outside_boundary_condition = 'Adiabatic'
                cpt = centroid(self.floors[fk].envelope.surfaces[sk].polygon)
                self.surface_cpt_dict[geometric_key(cpt)] = {}

    # ================================
    # LCA Methods
    # ================================ 
    def get_impacts(self, scope='all', lc_stage=None):
        """ Get impacts.
         
        Parameters
        ----------
        scope : {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}
            Scope of impacts
            - 'all': from A-C
            - 'product': from A1-A3
            - 'transportation': A4
            - 'construction': A5
            - 'use': from B1-B7
            - 'end of life': C1-C4
        lc_stage: {'C1', 'C2', 'C3', 'C4', None}
            Life cycle stage for which the impacts to be calculated. 
            If None, gives impacts for all the relevant life cycle stages. 
            Default is None.

        Returns
        -------
        ~pod_lca.impacts.Impact
            LCA Impacts.
        """
        # TODO: use cache with each part to avoid redoing calculations ---  same for emissions
        if scope == 'all':
            return (self.get_product_impacts() + self.get_transportation_impacts()
                    + self.get_construction_impacts() + self.get_replacement_impacts()
                    + self.get_operational_impacts() + self.get_eol_impacts(lc_stage))
        elif scope == 'product':
            return self.get_product_impacts()
        elif scope == 'transportation':
            return self.get_transportation_impacts()
        elif scope == 'construction':
            return self.get_construction_impacts()
        elif scope == 'replacement':
            return self.get_replacement_impacts()
        elif scope == 'operational energy':
            return self.get_operational_impacts()
        elif scope in ['end of life', 'end-of-life']:
            return self.get_eol_impacts(lc_stage)
        else:
            raise ValueError('LCA scope not recognized')

    def get_emissions(self, scope='all', lc_stage=None):
        """ Get emissions.
         
        Parameters
        ----------
        scope : {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}
            Scope of impacts
            - 'all': from A-C
            - 'product': from A1-A3
            - 'transportation: A4
            - 'construction': A5
            - 'use': from B1-B7
            - 'end of life': C1-C4
        lc_stage: {'C1', 'C2', 'C3', 'C4', None}
            Life cycle stage for which the impacts to be calculated. 
            If None, gives impacts for all the relevant life cycle stages. 
            Default is None.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            LCA emissions.
        """
        if scope == 'all':
            return (self.get_product_emissions() + self.get_transportation_emissions()
                    + self.get_construction_emissions() + self.get_replacement_emissions()
                    + self.get_operational_emissions() + self.get_eol_emissions(lc_stage))
        elif scope == 'product':
            return self.get_product_emissions()
        elif scope == 'transportation':
            return self.get_transportation_emissions()
        elif scope == 'construction':
            return self.get_construction_emissions()
        elif scope == 'replacement':
            return self.get_replacement_emissions()
        elif scope == 'operational energy':
            return self.get_operational_emissions()
        elif scope == 'end of life':
            return self.get_eol_emissions(lc_stage)
        else:
            raise ValueError('LCA scope not recognized')

    def get_drf_record(self, time_horizon=100, time_step=1/12):
        """ Get the dynamic radiative forcing record for all the products and procesess in the model.
        
        Parameters
        ----------
        time_horizon : int
            Time horizon in years.
        time_step : int or float
            Time step of the record. The same time step is used for both for integration and for reporting.

        Returns
        -------
        ~pod_lca.drf.DynamicRadiativeForcingRecord
            Dynamic Radiative Forcing Record
        """
        all_emissions = self.get_product_emissions(objs=True) + \
                        self.get_transportation_emissions(objs=True) + \
                        [self.get_construction_emissions()] + \
                        self.get_eol_emissions(lc_stage=None, objs=True) + \
                        self.get_replacement_emissions(objs=True) + \
                        self.get_operational_emissions(objs=True) 
                        
        return DynamicRadiativeForcingRecord.from_emissions(all_emissions, 
                                                           self.get_built_year(), 
                                                           time_horizon, 
                                                           time_step)


if __name__ == '__main__':
    pass
