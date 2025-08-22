
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from shapely import Polygon

from . import EndOfLifeMixins
from . import ProductScopeMixins
from . import Floor
from ..building_structure import BuildingStructure
from ..building_structure import ConcreteStructure
from ...units import METER
from ...units import UNITS_MAP


class Building (EndOfLifeMixins, ProductScopeMixins):
    """ Building object to keep track of the building materials flow (i.e., embodied energy component).

    Attributes
    ----------
    name : str
        Name of the building.
    building_type : {'Commercial', 'Residential'}
        Type of building.
    structure_type : {'Concrete', 'Steel', 'CLT'}
        Major vertical gravity system of the structure.
    location : ~pod_lca.location.Location
        Location of the building site.
    built_year: int
        Built year of the building.
    components : list of BuildingComponent Objs.
        Structural and Fascade elements that make up the building.
    impacts : dict
        Impact objects categorized by life cycle stage {life cycle stage (str): list of Impacts Obj.}
    eol_impact_database : ImpactsDatabase Obj.
        Impacts related to end of life processes.
    transportation_in: ProjectLogisticManager Obj.
        Inward trransportation of material for the construction of the building.   
    """

    def __init__(self):
        self.name = None
        self.building_type = None
        self.structure_type = None
        self.built_year = None
        self.location = None

        self.floors = {}
        self.structure = None
        self.envelope = None
        self.operational_object = None
        self.components = []

        self.impacts = {'A5':[], 'B1':[], 'B2':[], 'B3':[], 'B4':[], 'B5':[], 'C1':[]}
        self.emissions = {'A5':[], 'B1':[], 'B2':[], 'B3':[], 'B4':[], 'B5':[], 'C1':[]}

        self.material_impact_database = None
        self.transport_impact_database = None
        self.eol_impact_database = None
        self.eol_transport_dataset = None
        self.transportation_in = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_parameters(cls, name, type, location, built_year, no_floors, f2f_height, floor_plan, floors_below_grade=None, geometry_units=METER):
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
        no_floors : int
            Number of floors in the building.
        f2f_height : float
            Floor to floor height.
        floor_plan : shapely.Polygon or list of tuples of float
            A polygon defining the floor plan geometry.
        floors_below_grade : int
            Number of floors below grade.
        geometry_units : ~pod_lca.units.Unit
            Unit of measurement used in geometry definitions.
        
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

        if not isinstance(floor_plan, Polygon):
            floor_no = Polygon(floor_plan)
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
    def from_template_model(cls, name, type, location, built_year, file_path, building_data):
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

        building.set_template_model(name, type, location, built_year, file_path, building_data)

        return building

    @classmethod
    def from_geometry(cls, name, type, location, built_year, geometry):
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
        geometry : 
            Geometry details of the building

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

    def set_location(self, location):
        """ Set location of the building site.
        
        Parameters
        ----------
        location : Location Obj.
            Location of the building site.
        """
        self.location = location

        return self
    
    def set_template_model(self, name, type, location, built_year, file_path, building_data):
        """ Set attributes to an existing building.
        
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
        """
        self.set_name(name)
        self.set_building_type(type)
        self.set_location(location)
        self.set_built_year(built_year)

        self.add_floors(building_data['no_floors'], 
                        building_data['f2f_height'], 
                        building_data['floor_plan'], 
                        building_data['floors_below_grade'], 
                        UNITS_MAP[building_data['geometry_units']])

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
    
    def get_floor(self, floor_no):
        """ Get the floor """
        pass

    def get_structure(self):

        return self.structure
    
    def get_envelope(self):

        return self.envelope

    def get_components(self):
        """ Get a list of building components.

        Returns
        -------
        list of BuildingComponent Objs.
            Structural and Fascade elements that make up the building.
        """
        return self.get_structure().get_components() # + self.get_envelope().get_components() # TODO add envelop components

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
        floor_plan : shapely.Polygon or list of tuples of float
            A polygon defining the floor plan geometry.
        floors_below_grade : int
            Number of floors below grade.
        geometry_units : ~pod_lca.units.Unit
            Unit of measurement used in geometry definitions.        
        """
        for num in range(no_floors):
            floor_no = num +1
            below_grade = True if floor_no <= floors_below_grade else False
            on_ground = True if floor_no == floors_below_grade + 1 else False
            self.add_floor(floor_no, floor_plan, f2f_height, geometry_units, below_grade, on_ground)

        return self

    def add_floor(self, floor_no, floor_plan, floor_height, geometry_unit, below_grade, on_ground):
        """ Add a floor to the building.

        Parameters
        ----------      
        floor_no : int
            Floor number. 
        floor_plan : shapely.Polygon
            Floor plan.   
        floor_height : float
            Floor height.   
        geometry_unit : ~pod_lca.units.Unit
            Unit of measurement     
        below_grade : bool
            True, if the floor is above grade.
        on_ground : bool
            True, if the floor is on the ground.
        """
        floor = Floor.from_floor_plan(floor_no, floor_plan, floor_height, geometry_unit)

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

    def add_component(self, component):
        """ Add a component to the building.
        
        Returns
        -------
        component : BuildingComponent Objs.
            Structural or fascade element to be added to the building.
        """

        self.get_components().append(component)
        component.set_building(self)

        return self

    def update_envelope_surfaces(self):
        pass

    # ================================
    # LCA Methods
    # ================================ 
    def get_impacts(self, scope='all'):
        """ Get impacts.
         
        Parameters
        ----------
        scope : {'all', 'product', 'construction', 'use', 'end of life'}
            Scope of impacts
            - 'all': from A-C
            - 'product': from A1-A3
            - 'construction': from A4-A5
            - 'use': from B1-B7
            - 'end of life': C1-C4
        """
        if scope == 'all':
            pass
        elif scope == 'product':
            return self.get_product_impacts()

    def get_emissions(self, scope='all'):
        """ Get emissions.
         
        Parameters
        ----------
        scope : {'all', 'product', 'construction', 'use', 'end of life'}
            Scope of impacts
            - 'all': from A-C
            - 'product': from A1-A3
            - 'construction': from A4-A5
            - 'use': from B1-B7
            - 'end of life': C1-C4
        """
        if scope == 'all':
            pass
        elif scope == 'product':
            return self.get_product_emissions()


if __name__ == '__main__':
    pass
