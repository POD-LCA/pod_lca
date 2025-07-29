
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import EOLImpactsDatabase
from ..impacts import TranportationModeImpactsDatabase


class Building:
    """ Building object to keep track of the building materials flow (i.e., embodied energy component).

    Attributes
    ----------
    name : str
        Name of the building.
    type : {'Commercial', 'Residential'}
        Type of building.
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

    def __init__(self): # NOTE: Currently only includes EOL
        self.name = None
        self.building_type = None
        self.location = None
        self.built_year = None
        self.gloors = {}
        self.structure = None
        self.envelope = None
        self.operational_object = None
        self.components = []
        self.impacts = {'A5':[], 'B1':[], 'B2':[], 'B3':[], 'B4':[], 'B5':[], 'C1':[]}
        self.emissions = {'A5':[], 'B1':[], 'B2':[], 'B3':[], 'B4':[], 'B5':[], 'C1':[]}
        self.transport_impact_database = None
        self.eol_impact_database = None
        self.eol_transport_dataset = None
        self.transportation_in = None

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
        self.building_type = type

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

    def set_transportation_impact_database(self, database):
        """ Set the impact database for end-of-life impacts.
        
        Parameters
        ----------
        database : ~pod_lca.impacts.TranportationModeImpactsDatabase or str
            Impact database object or if a string, filepath to the corresponding csv file containing impact data.
        """
        if isinstance(database, TranportationModeImpactsDatabase):
            self.transport_impact_database = database
        elif isinstance(database, str):
            impact_database = TranportationModeImpactsDatabase.new("impact database")
            impact_database.set_data(database)
            self.set_transportation_impact_database(impact_database)
        else:
            raise TypeError("Database input not recognized")

        return self
      
    def set_eol_database(self, database):
        """ Set the impact database for end-of-life impacts.
        
        Parameters
        ----------
        database : ~pod_lca.impacts.EOLImpactsDatabase or str
            Impact database object or if a string, filepath to the corresponding csv file containing impact data.
        """
        if isinstance(database, EOLImpactsDatabase):
            self.eol_impact_database = database
        elif isinstance(database, str):
            impact_database = EOLImpactsDatabase.new("impact database")
            impact_database.set_data(database)
            self.set_eol_database(impact_database)
        else:
            raise TypeError("Database input not recognized")
    
    def set_eol_transport_dataset(self, dataset):
        """ Set transportation dataset for the end-of-life impacts.

        Parameters
        ----------
        dataset : ~pod_lca.transportation.TransportDataset
            End-of-life transportation dataset.
        """
        self.eol_transport_dataset = dataset

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

        self.building_type = type

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

    def get_transportation_impact_database(self):
        """ Set the impact database for end-of-life impacts.
        
        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            End-of-Life impacts database.
        """
        return self.transport_impact_database
    
    def get_eol_database(self):
        """ Get the impact database for end-of-life impacts.
        
        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            End-of-Life impacts database.
        """
        return self.eol_impact_database

    def get_eol_transport_dataset(self):
        """ Get transportation dataset for the end-of-life impacts.

        Returns
        -------
        ~pod_lca.transportation.TransportDataset
            End-of-life transportation dataset.
        """
        return self.eol_transport_dataset
    # ================================
    # Assembly Methods
    # ================================ 
    def add_component(self, component):
        """ Add a component to the building.
        
        Returns
        -------
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

        pass # TODO: write method to demolish the building and add C1 impacts


if __name__ == '__main__':
    pass
