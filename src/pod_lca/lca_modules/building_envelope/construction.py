__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building_envelope.layer import Layer
from pod_lca.lca_modules.operational.read_write import find_constructions


class Construction(object):
    def __init__(self):
        self.name = None
        self.layers = {}

    @classmethod
    def from_idf(cls, name, path):
        data = {}
        find_constructions(path, data)
        data = data['constructions'][name]

        construction = cls()
        construction.name = data['name']
        construction.layers = data['layers']
        construction.get_layers_from_idf(path)
        return construction
    
    def get_layers_from_idf(self, path):
        for mk in self.layers:
            name = self.layers[mk]
            layer = Layer.from_idf(name, path)
            self.layers[mk] = layer

if __name__ == '__main__':
    from pod_lca.utilities import config

    from pod_lca.lca_modules.building import BuildingMaterial

    for i in range(50): print('')


    #TODO: Fix the issue of different material types, start at layer!!!!

    name = 'Typical Insulated Steel Framed Exterior Wall-R16'
    path = config['file_paths']['operational']['CONSTRUCTIONS']
    c = Construction.from_idf(name, path)

    print(c.layers['0'].material.roughness)