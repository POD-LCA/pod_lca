__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from ..building import BuildingMaterial
from ..operational.read_write import find_materials

class Layer(object):
    def __init__(self):
        self.name = None
        self.material = None
        self.thickness = None

    @classmethod
    def from_idf(cls, name, path):
        data = {}
        find_materials(path, data)
        data = data['materials'][name]
        name                = data['name']
        roughness           = data['roughness']
        thickness           = data['thickness']
        conductivity        = data['conductivity']
        density             = data['density']
        specific_heat       = data['specific_heat']
        thermal_absorptance = data['thermal_absorptance']
        solar_absorptance   = data['solar_absorptance']
        visible_absorptance = data['visible_absorptance']

        material = BuildingMaterial.new_enclosure_material(name,
                                                           roughness,
                                                           thickness,
                                                           conductivity,
                                                           density,
                                                           specific_heat,
                                                           thermal_absorptance,
                                                           solar_absorptance,
                                                           visible_absorptance)

        layer = cls()
        layer.name = '{}_{}'.format(name, thickness)
        layer.thickness = thickness
        layer.material = material


if __name__ == '__main__':
    pass