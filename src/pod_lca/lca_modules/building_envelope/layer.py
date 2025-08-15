__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from ..building import BuildingMaterial
from ..building import BuildingEnvelopeMaterial
from ..building import BuildingEnvelopeMaterialNoMass
from ..operational import find_materials
from ..operational import find_no_mass_materials
from ..operational import find_gas_materials
from ..operational import find_glazing_materials


class Layer(object):
    def __init__(self):
        self.name = None
        self.material = None
        self.thickness = None

    @classmethod
    def from_idf(cls, name, path):

        #TODO: Fix the issue of different material types!!!!
        data = {}
        find_materials(path, data)
        if name not in data:
            find_no_mass_materials(path, data)
        if name not in data:
            find_gas_materials(path, data)
        if name not in data:
            find_glazing_materials(path, data)

        data                = data['materials'][name]
        name = data['name']
        thickness = data.get('thickness')

        layer = cls()
        layer.name = '{}_{}'.format(name, thickness)
        layer.thickness = thickness
        layer.material = layer.add_building_envelope_material(data)
        return layer

    def add_building_envelope_material(self, data):
        mtype = data['__type__']
        if mtype == 'Material':
            material = BuildingEnvelopeMaterial.from_idf_data(data)
        elif mtype == 'MaterialNoMass':
            material = BuildingEnvelopeMaterialNoMass.from_idf_data(data)

        return material

if __name__ == '__main__':
    pass