
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from ..building_envelope import Surface
from pod_lca.utilities import area_polygon


class Envelope:

    def __init__(self):
        self.name = None
        self.floor = None
        self.surfaces = {}

        self.walls = {}
        self.windows = {}
        self.shadings = {}
        self.floors = {}
        self.cielings = {}
        self.construction_map = {'Floor': self.floors,
                                 'Cieling': self.cielings,
                                 'Wall': self.walls,
                                 'Window': self.windows,
                                 'Shadings': self.shadings}
        
        self.wall_surface_keys = []
        self.window_surface_keys = []
        self.origin = [0, 0, 0]

    @classmethod
    def from_floor(cls, floor):
        envelope = cls()
        envelope.floor = floor
        envelope.update_envelope_surfaces()
        return envelope
    
    @property
    def height(self):
        return self.floor.height
    
    @property
    def floor_plan(self):
        return self.floor.floor_plan
    
    @property
    def area(self):
        return area_polygon(self.floor_plan)

    @property
    def volume(self):
        return self.height * self.area
    
    def update_envelope_surfaces(self):
        fp = self.floor_plan
        h = self.height
        cp = [[p[0], p[1], p[2]+h] for p in fp]
        self.surfaces['floor'] = Surface.from_polygon('floor', fp)
        self.surfaces['cieling'] = Surface.from_polygon('cieling', cp)
        for i in range(len(fp)):
            a = fp[i]
            if i == len(fp)-1:
                b = fp[0]
            else:
                b = fp[i+1]
            wp = [a, b, [b[0], b[1], b[2]+h], [a[0], a[1], a[2]+h]]
            wk = 'wall_{}'.format(i)
            self.surfaces[wk] = Surface.from_polygon(wk, wp)
            self.wall_surface_keys.append(wk)

    def get_assemblies(self):
        # TODO implement method to return all envelop elements as a list
        return []

    def add_construction(self, construction):
        con_dict = self.construction_map[construction.__type__]
        key = '{}_{}'.format(construction.__type__, len(con_dict))
        con_dict[key] = construction

    # def add_window(self, window):
    #     self.windows[len(self.windows)] = window

    # def add_shading(self, shading):
    #     self.shadings[len(self.shadings)] = shading

if __name__ == '__main__':

    pass