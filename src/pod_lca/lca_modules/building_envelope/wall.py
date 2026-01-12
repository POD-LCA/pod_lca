__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building_envelope.construction import Construction


class Wall(Construction):
    def __init__(self):
        super().__init__()
        self.__type__ = 'Wall'


class FramedWall(Construction):
    def __init__(self):
        super().__init__()
        self.__type__ = 'Wall'
        self.framing = None


    @classmethod
    def from_layers_framing(cls, name, layers, framing):

        construction = cls.create(name, building)
        construction.layer_order = data['layers']
        construction.get_layers(building)
        construction.surfaces = surfaces
        construction.set_service_life(35) # TODO: implement reading POD|LCA RSL Category from constructions
        construction.add_materials(building, service_life)
        for surface in surfaces:
            surface.add_construction(construction)
        return construction