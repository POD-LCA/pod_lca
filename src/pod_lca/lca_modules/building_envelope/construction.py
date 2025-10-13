__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from ..building_envelope import Layer
from ..operational import find_constructions
from pod_lca.lca_modules.building.assembly import Assembly
from pod_lca.lca_modules.building.material import Material
from ...units import CUBIC_METER


class Construction(Assembly):
    def __init__(self):
        super().__init__()
        self.layers = {}
        self.surfaces = []

    @classmethod
    def from_idf(cls, name, path, building, envelope, surface_type, service_life):

    
        data = {}
        find_constructions(path, data)
        data = data['constructions'][name]

        construction = cls.create(data['name'], building)
        construction.layers = data['layers']
        construction.get_layers_from_idf(path)

        if surface_type == 'wall' or surface_type == 'walls':
            sks = envelope.wall_surface_keys
        elif surface_type == 'window' or surface_type == 'windows':
            sks = envelope.window_surface_keys
        else:
            sks = [surface_type]
        for sk in sks:
            construction.surfaces.append(envelope.surfaces[sk])
        area = construction.area
        for lk in construction.layers:
            mat_type = construction.layers[lk].material_property.__type__
            if mat_type != 'EnvelopeMaterialAirGap' and mat_type != 'WindowMaterialGas':
                mat_name = construction.layers[lk].material_property.name
                quantity = area * construction.layers[lk].thickness
                material = Material.new_structural_material(parent=construction,
                                                            name=mat_name,
                                                            qty=quantity,
                                                            unit=CUBIC_METER,
                                                            material_database_entry=mat_name,
                                                            product_year=building.get_built_year(),
                                                            service_life=service_life,
                                                            waste_rate=0.0)
                construction.add_material(material)

        return construction
    

    @property
    def area(self):
        area = 0
        for s in self.surfaces:
            area += s.area
        return area


    def get_layers_from_idf(self, path):
        for mk in self.layers:
            name = self.layers[mk]
            layer = Layer.from_idf(name, path)
            self.layers[mk] = layer

if __name__ == '__main__':
    pass

    # from pod_lca.utilities import config


    # for i in range(50): print('')


    # name = 'Typical Insulated Steel Framed Exterior Wall-R16'
    # path = config['file_paths']['operational']['CONSTRUCTIONS']
    # c = Construction.from_idf(name, path)

    # print(c.layers['3'].material.name)