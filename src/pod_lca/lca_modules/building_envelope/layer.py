__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from .material_property import EnvelopeMaterialPropertyMass
from .material_property import EnvelopeMaterialPropertyAirGap
from .material_property import EnvelopeMaterialPropertyNoMass
from .material_property import WindowMaterialPropertyGlazing
from .material_property import WindowMaterialPropertyGas

from pod_lca.units import Quantity as Q
from pod_lca.units import METER, KELVIN, WATT

mKW = (METER * KELVIN) / WATT


class Layer(object):
    def __init__(self):
        self.name = None
        self.material_property = None
        self.thickness = None
        self.unit = None
        self.classification = None

    @classmethod
    def from_data(cls, data, thickness, classification=None):
        layer = cls()
        layer.name = data['name']
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
        layer.name = name
        layer.thickness = thickness
        layer.material_property = layer.add_envelope_material_property(data)
        return layer

    @classmethod
    def from_property_and_thickness(cls, name, material_property, thickness, classification=None):
        layer = cls()
        layer.name = name
        layer.thickness = thickness
        layer.material_property = material_property
        layer.classification = classification
        return layer

    def add_envelope_material_property(self, data):
        mtype = data['__type__']
        if mtype == 'MaterialPropertyMass':
            material_prop = EnvelopeMaterialPropertyMass.from_data(data)
        elif mtype == 'MaterialPropertyAirGap':
            material_prop = EnvelopeMaterialPropertyAirGap.from_data(data)
        elif mtype == 'MaterialPropertyNoMass':
            material_prop = EnvelopeMaterialPropertyNoMass.from_data(data)
        elif mtype == 'WindowMaterialPropertyGlazing':
            material_prop = WindowMaterialPropertyGlazing.from_data(data)
        elif mtype == 'WindowMaterialPropertyGas':
            material_prop = WindowMaterialPropertyGas.from_data(data)
        else:
            raise ValueError('Material Property type {} has not been implemented yet'.format(mtype))

        return material_prop
    
    def get_r(self, thickness=None):
        mtype = self.material_property.__type__
        if mtype == 'MaterialPropertyMass':
            resistivity =  self.material_property.conductivity.invert()
            return resistivity * thickness
        elif mtype == 'EnvelopeMaterialPropertyAirGap':
            return self.material_property.thermal_resistance
        elif mtype == 'MaterialPropertyNoMass':
            return self.material_property.thermal_resistance
        else:
            raise ValueError('Material Property type {} has not been implemented yet'.format(mtype))

    def get_resistivity(self, thickness=None):
        mat = self.material_property
        mtype = mat.__type__
        if mtype == 'MaterialPropertyMass':
            return mat.conductivity.invert()
        elif mtype == 'MaterialPropertyNoMass':
            resistivity = mat.thermal_resistance / thickness
            # return Q(resistivity.value, mKW)
            return resistivity
        else:
            raise ValueError('Material Property type {} has not been implemented yet'.format(mtype))

if __name__ == '__main__':
    pass