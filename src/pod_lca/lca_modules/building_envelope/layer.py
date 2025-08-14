__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from ..building import BuildingMaterial
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
        if data['__type__'] == 'Material':
            name                = data['name']
            roughness           = data['roughness']
            thickness           = data['thickness']
            conductivity        = data['conductivity']
            density             = data['density']
            specific_heat       = data['specific_heat']
            thermal_absorptance = data['thermal_absorptance']
            solar_absorptance   = data['solar_absorptance']
            visible_absorptance = data['visible_absorptance']

        elif data['__type__'] == 'MaterialNoMass':
            name                = data['name']
            roughness           = data['roughness']
            thermal_resistance  = data['thermal_resistance'] 
            solar_absorptance   = data['solar_absorptance']
            visible_absorptance = data['visible_absorptance']
            thickness           = None
            conductivity        = None
            density             = None
            specific_heat       = None
            thermal_absorptance = None

        material = BuildingMaterial.new_enclosure_material(name,
                                                           roughness,
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
        return layer


if __name__ == '__main__':
    pass