__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


from pod_lca.utilities.geometry import area_polygon
from pod_lca.utilities.geometry import normal_polygon
from pod_lca.utilities.geometry import centroid

class Surface(object):
    """ Flat building surfaces base object.
    
    Attributes
    ----------
    polygon : (list of) of ~pod_lca.units.Quantity
        List of X,Y,Z coordinates for the surface boundary.
    name : str
        The name of the surface.
    surface_type : str 
        Type of the surface (Wall. Window, Floor, etc.)
    outside_boundary_condition :  str
        The type of condition on the outside of the surface 
        (Outdoors, Ground, Adiabatic. etc). 
    outside_boundary_condition_object : str
        Object or surface a surface is in contact with. 
    construction :  ~pod_lca.building_envelope.Construction
        The construction the surface is assigned to. 
    window :  ~pod_lca.building_envelope.Window
        The window object the surface is assigned to. 
    """
    def __init__(self):
        self.polygon                            = None
        self.name                               = None
        self.surface_type                       = None
        self.outside_boundary_condition         = None
        self.outside_boundary_condition_object  = None
        self.construction                       = None
        self.window                             = None

    @property
    def area(self):
        """Computes the surface area. 

        Returns
        -------
        area : ~pod_lca.units.Quantity
            The surface area. 
        """
        area = area_polygon(self.polygon)
        if self.window:
            area -= self.window.area
        return area


    @classmethod
    def from_polygon(cls, name, polygon, **kwargs):
        """Creates an instance of the surface object from a 
        polygon and kwargs. 

        Parameters
        ----------
        name : str
            The name of the surface. 
        polygon : (list of) ~pod_lca.units.Quantity
            List of X,Y,Z coordinates for the surface vertices. 
        kwargs : (optional) dict
            Additional surface properties like surface_type. 

        Returns
        -------
        srf : ~pod_lca.building_envelope.Surface
            The surface instance
        """
        srf = cls()
        srf.name = name
        srf.polygon = polygon
        srf.surface_type = kwargs.get('surface_type', None)
        srf.construction = kwargs.get('construction', None)
        return srf
    
    def add_construction(self, construction):
        """Adds a given construction to the surface. 

        Parameters
        ----------
        construction : ~pod_lca.building_envelope.Construction
            The construction object to be added.
        """
        self.construction = construction
        construction.surfaces[self.name] = self

    @classmethod
    def from_data(cls, data):
        """Creates a surface instance from a data dictionary

        Parameters
        ----------
        data :  dict
            The dictionary containing all required data to create
            the surface instance. 
        
        Returns
        -------
        srf : ~pod_lca.building_envelope.Surface
            The surface instance
        """
        srf = cls()
        srf.polygon                           = data['polygon']
        srf.name                              = data['name']
        srf.surface_type                      = data['surface_type']
        srf.outside_boundary_condition        = data['outside_boundary_condition']
        srf.outside_boundary_condition_object = data['outside_boundary_condition_object']
        srf.construction                      = data['construction']
        return srf

    def to_data(self):
        """Exports all surface data to a dictionary. 

        Returns
        -------
        data :  dict
            A dictionary containing all surface data. 
        """
        data = {}
        data['polygon']                           = self.polygon                          
        data['name']                              = self.name                             
        data['surface_type']                      = self.surface_type                     
        data['outside_boundary_condition']        = self.outside_boundary_condition       
        data['outside_boundary_condition_object'] = self.outside_boundary_condition_object
        data['construction']                      = self.construction                     
        return data

    def convert_polygon_to_unit(self, unit):
        """Converts the X,Y,Z coordinates of all polygon
        vertices to a given unit. 

        Parameters
        ----------
        unit :  ~pod_lca.units.Unit
            The desirted unit of distance to convert to. 
        """
        for xyz in self.polygon:
            xyz[0].convert_to(unit)
            xyz[1].convert_to(unit)
            xyz[2].convert_to(unit)
    
    @property
    def normal(self):
        """Returns the surface normal vector.

        Returns
        ------- 
        ~pod_lca.units.Quantity
            X, Y, Z components of the normal vector
        """
        return normal_polygon(self.polygon)
    
    @property
    def centroid(self):
        """Returns the centroid of the surface.

        Returns
        ------- 
        (list of) ~pod_lca.units.Quantity
            X, Y, Z coordinates of the centroid. 
        """
        return centroid(self.polygon)
    
    def reverse_normal(self):
        """Reverses the cycle direction of the surface
        polygon, and hence the surface normal. 
        """
        self.polygon = list(reversed(self.polygon))



