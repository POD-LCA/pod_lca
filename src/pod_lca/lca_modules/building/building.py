
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import ConstructionMixins
from . import DataMixins
from . import EndOfLifeMixins
from . import Floor
from . import OperationalMixins
from . import ProductScopeMixins
from . import TransportationMixins
from . import UseMixins
from ..building_structure import BuildingStructure
from ..building_structure import ConcreteStructure
from ..dynamic_radiative_forcing import DynamicRadiativeForcingRecord
from ...units import METER
from ...units import UNITS_MAP
from ...utilities import centroid
from ...utilities import geometric_key


class Building (DataMixins, EndOfLifeMixins, OperationalMixins, UseMixins, ConstructionMixins, TransportationMixins, ProductScopeMixins):
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

        self.construction_energy_product = None
        self.operational_energy_product = None

    # ================================
    # Constructors
    # ================================
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

        building.set_material_database()
        building.set_transportation_mode_impact_database()
        building.set_eol_process_impact_database()
        building.set_eol_demolition_impact_database()
        building.set_eol_transport_dataset()

        if floors_below_grade is None:
            if no_floors > 2:
                floors_below_grade = 1
            else:
                floors_below_grade = 0

        building.add_floors(no_floors, f2f_height, floor_plan, floors_below_grade, geometry_units)

        building.set_transportation_manager(logistic_type)
        building.set_operational_electricity_product()

        building.make_structure('from geometry')
        building.make_envelope()

        return building

    @classmethod
    def from_template_model(cls, name, type, location, built_year, life_span, file_path, building_data):
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

        building.set_material_database()
        building.set_transportation_mode_impact_database()
        building.set_eol_process_impact_database()
        building.set_eol_demolition_impact_database()
        building.set_eol_transport_dataset()

        building.set_template_model(file_path, building_data)

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
        building = cls()

        building.set_name(name)
        building.set_building_type(type)
        building.set_location(location)
        building.set_built_year(built_year)
        building.set_life_span(life_span)

        building.set_material_database()
        building.set_transportation_mode_impact_database()
        building.set_eol_process_impact_database()
        building.set_eol_demolition_impact_database()
        building.set_eol_transport_dataset()

        building.set_transportation_manager(logistic_type)
        building.set_operational_electricity_product()

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
    
    def set_template_model(self, file_path, building_data):
        """ Set attributes to an existing building.
        
        Parameters
        ----------
        file_path : int
            File path to template model bill of material list.
        building_data : dict
            Dictionary provding building data
        """
        self.add_floors(building_data['no_floors'], 
                        building_data['f2f_height'], 
                        building_data['floor_plan'], 
                        building_data['floors_below_grade'], 
                        UNITS_MAP[building_data['geometry_units']])
        
        self.set_transportation_manager(building_data['logistic_type'])
        self.set_operational_electricity_product(unit=UNITS_MAP[building_data["construction_energy_use_unit"]])

        if "construction_energy_use" in building_data:
            self.set_construction_energy_product(building_data["construction_energy_use"], 
                                         UNITS_MAP[building_data["construction_energy_use_unit"]])

        self.make_structure('from template', template_bom=file_path)
        self.make_envelope()    

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
        self.building_type = type

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
        
    def get_floor(self, floor_no):
        """ Get the floor """
        pass

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
        # return self.get_structure().get_assemblies() # + self.get_envelope().get_assemblies() # TODO add envelop assemblies

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

    def make_envelope(self):

        pass

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
                        srf.outside_boundary_condition = 'Zone'
                elif sk == 'cieling':
                    if floor.is_last:
                        srf.outside_boundary_condition = 'Outdoors'
                    else:
                        srf.outside_boundary_condition = 'Zone'
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
                        self.get_replacement_emissions(objs=True) 
                        # self.get_operational_emissions(objs=True) + \
                        
        return DynamicRadiativeForcingRecord.from_emissions(all_emissions, 
                                                           self.get_built_year(), 
                                                           time_horizon, 
                                                           time_step)


if __name__ == '__main__':
    pass
