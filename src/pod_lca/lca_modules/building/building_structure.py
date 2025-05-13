
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class Building:
    """ Building object to keep track of the building materials flow (i.e., embodied energy component).

    Attributes
    ----------
    name : str
        Name of the building.
    type : str
        Type of building: e.g., 'Commercial', 'Residential'.
    location : Location Obj.
        Location of the building site.
    built_year: int
        Built year of the building.
    components : list of BuildingComponent Objs.
        Structural and Fascade elements that make up the building.
    impacts : dict.
        Impact objects categorized by life cycle stage {life cycle stage (str): list of Impacts Obj.}
    eol_impact_database : ImpactsDatabase Obj.
        Impacts related to end of life processes.
    transportation_in: ProjectLogisticManager Obj.
        Inward trransportation of material for the construction of the building.
    transportation_out: ProjectLogisticManager Obj.
        Outward trransportation of waste material after demolition and/or deconstruction.    
    """

    def __init__(self): # NOTE: Currently only includes EOL
        self.name = None
        self.type = None
        self.location = None
        self.built_year = None
        self.components = []
        self.impacts = {'A5':[], 'B1':[], 'B2':[], 'B3':[], 'B4':[], 'B5':[], 'C1':[]}
        self.eol_impact_database = None
        self.transportation_in = None
        self.transportation_out = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def build(cls, name, type, location, built_year, geometry):
        """ Build a building.
        
        Parameters
        ----------
        name : str
            Name of the building.
        type : str
            Type of building: e.g., 'Commercial', 'Residential'.
        location : Location Obj.
            Location of the building site.
        built_year: int
            Built year of the building.
        geometry : 
            Geometry details of the building

        Returns
        -------
        Building Obj.
            Building built.
        """
        building = cls()

        building.set_name(name)
        building.set_type(type)
        building.set_location(location)
        building.set_built_year(built_year)

        # TODO: build components from the geometry / assembly_map

        # TODO: set ProjectLogisticManager Obj.

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
    
    def set_type(self, type):
        """ Set building type.
        
        Parameters
        ----------
        type : str
            Type of building: e.g., 'Commercial', 'Residential'.
        """
        self.type = type

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
    
    def set_built_year(self, year):
        """ Set built year of the building.
        
        Parameters
        ----------
        year: int
            Built year of the building.
        """
        self.built_year = year

        return self
    
    def set_eol_database(self, database):
        """ Set the impact database for end-of-life impacts.
        
        Parameters
        ----------
        database : ImpactsDatabase Obj.
            End-of-Life impacts database.
        """
        self.eol_impact_database = database

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

    def get_type(self):
        """ Get building type.
        
        Returns
        -------
        str
            Type of building: e.g., 'Commercial', 'Residential'.
        """

        self.type = type

    def get_location(self):
        """ Get location of the building site.
        
        Returns
        -------
        Location Obj.
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
    
    def get_components(self):
        """ Get a list of building components.

        Returns
        -------
        list of BuildingComponent Objs.
            Structural and Fascade elements that make up the building.
        """
        return self.components

    def get_eol_database(self):
        """ Get the impact database for end-of-life impacts.
        
        Parameters
        ----------
        ImpactsDatabase Obj.
            End-of-Life impacts database.
        """
        return self.eol_impact_database
    
    # ================================
    # Assembly Methods
    # ================================ 
    def add_component(self, component):
        """ Add a component to the building.
        
        Parameters
        ----------
        component : BuildingComponent Objs.
            Structural or fascade element to be added to the building.
        """

        self.get_components().append(component)
        component.set_building(self)

        # TODO: set the transportation link

        return self

    # ================================
    # EOL Methods
    # ================================ 
    def deconstruct(self):

        pass # TODO: write method to deconstruct the building and add C1 impacts

    def demolish(self):

        pass # TODO: writte method to demolish the building and add C1 impacts


if __name__ == '__main__':
    pass
