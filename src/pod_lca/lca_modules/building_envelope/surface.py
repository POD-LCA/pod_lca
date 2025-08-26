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
        # self.outside_boundary_condition_object  = ''

    @property
    def area(self):
        return area_polygon(self.polygon)


    @classmethod
    def from_polygon(cls, name, polygon):
        srf = cls()
        srf.name = name
        srf.polygon = polygon
        return srf