__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


from pod_lca.utilities.geometry import area_polygon


class Surface(object):
    def __init__(self):
        self.polygon                            = None
        self.name                               = None
        self.surface_type                       = None
        self.outside_boundary_condition         = None
        self.outside_boundary_condition_object  = None
        self.construction                       = None

    @property
    def area(self):
        return area_polygon(self.polygon)


    @classmethod
    def from_polygon(cls, name, polygon, surface_type):
        srf = cls()
        srf.name = name
        srf.polygon = polygon
        srf.surface_type = surface_type
        return srf
    
    def add_construction(self, construction):
        self.construction = construction

    @classmethod
    def from_data(cls, data):
        srf = cls()
        srf.polygon                           = data['polygon']
        srf.name                              = data['name']
        srf.surface_type                      = data['surface_type']
        srf.outside_boundary_condition        = data['outside_boundary_condition']
        srf.outside_boundary_condition_object = data['outside_boundary_condition_object']
        # srf.construction                      = data['construction']
        return srf

    def to_data(self):
        data = {}
        data['polygon']                           = self.polygon                          
        data['name']                              = self.name                             
        data['surface_type']                      = self.surface_type                     
        data['outside_boundary_condition']        = self.outside_boundary_condition       
        data['outside_boundary_condition_object'] = self.outside_boundary_condition_object
        # data['construction']                      = self.construction                     

        return data




