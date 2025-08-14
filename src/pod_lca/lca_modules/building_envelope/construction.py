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
        construction.get_layers()
        return construction
    
    def get_layers(self):
        
        layer = Layer.from_idf()



if __name__ == '__main__':
    from pod_lca.utilities import config

    from pod_lca.lca_modules.building import BuildingMaterial

    for i in range(50): print('')

    name = 'Typical Insulated Steel Framed Exterior Wall-R16'
    path = config['file_paths']['operational']['CONSTRUCTIONS']
    c = Construction.from_idf(name, path)

