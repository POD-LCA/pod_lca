__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from .material_property import EnvelopeMaterial
from .material_property import EnvelopeMaterialAirGap
from .material_property import EnvelopeMaterialNoMass
from .material_property import WindowMaterialGlazing
from .material_property import WindowMaterialGas


class Layer(object):
    def __init__(self):
        self.name = None
        self._material_property = None
        self.thickness = None
        self.unit = None
        self.classification = None

    @classmethod
    def from_data(cls, data, thickness, classification=None):
        layer = cls()
        layer.name = '{}_{}'.format(data['name'], thickness)
        layer.thickness = thickness
        layer.material_property = layer.add_envelope_material_property(data)
        layer.classification = classification
        return layer


        

    @classmethod
    def from_idf(cls, name, building):
        data = building.idf_material_properties['materials'][name]
        name = data['name']
        thickness = data.get('thickness')

        layer = cls()
        layer.name = '{}_{}'.format(name, thickness)
        layer.thickness = thickness
        layer.material_property = layer.add_envelope_material_property(data)
        return layer

    def add_envelope_material_property(self, data):
        mtype = data['__type__']
        if mtype == 'Material':
            material_prop = EnvelopeMaterial.from_data(data)
        elif mtype == 'MaterialAirGap':
            material_prop = EnvelopeMaterialAirGap.from_data(data)
        elif mtype == 'MaterialNoMass':
            material_prop = EnvelopeMaterialNoMass.from_data(data)
        elif mtype == 'WindowMaterialGlazing':
            material_prop = WindowMaterialGlazing.from_data(data)
        elif mtype == 'WindowMaterialGas':
            material_prop = WindowMaterialGas.from_data(data)
        else:
            raise ValueError('Material Property type {} has not been implemented yet'.format(mtype))

        return material_prop

if __name__ == '__main__':
    pass