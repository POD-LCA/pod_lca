__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


from pod_lca.utilities.geometry import area_polygon
from pod_lca.utilities.geometry import normal_polygon
from pod_lca.utilities.geometry import centroid

class Surface(object):
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
        area = area_polygon(self.polygon)
        if self.window:
            area -= self.window.area
        return area


    @classmethod
    def from_polygon(cls, name, polygon, **kwargs):
        srf = cls()
        srf.name = name
        srf.polygon = polygon
        srf.surface_type = kwargs.get('surface_type', None)
        srf.construction = kwargs.get('construction', None)
        return srf
    
    def add_construction(self, construction):
        self.construction = construction
        construction.surfaces[self.name] = self

    @classmethod
    def from_data(cls, data):
        srf = cls()
        srf.polygon                           = data['polygon']
        srf.name                              = data['name']
        srf.surface_type                      = data['surface_type']
        srf.outside_boundary_condition        = data['outside_boundary_condition']
        srf.outside_boundary_condition_object = data['outside_boundary_condition_object']
        srf.construction                      = data['construction']
        return srf

    def to_data(self):
        data = {}
        data['polygon']                           = self.polygon                          
        data['name']                              = self.name                             
        data['surface_type']                      = self.surface_type                     
        data['outside_boundary_condition']        = self.outside_boundary_condition       
        data['outside_boundary_condition_object'] = self.outside_boundary_condition_object
        data['construction']                      = self.construction                     
        return data

    def convert_polygon_to_unit(self, unit):
        for xyz in self.polygon:
            xyz[0].convert_to(unit)
            xyz[1].convert_to(unit)
            xyz[2].convert_to(unit)
    
    @property
    def normal(self):
        return normal_polygon(self.polygon)
    
    @property
    def centroid(self):
        return centroid(self.polygon)
    
    def reverse_normal(self):
        self.polygon = list(reversed(self.polygon))



