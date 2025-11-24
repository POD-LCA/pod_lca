__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from . import EnvelopeMaterial
from ..building_envelope import Layer
from pod_lca.lca_modules.building.assembly import Assembly
from ...units import CUBIC_METER
from ...utilities import DataImporter
from ...utilities import config


class Construction(Assembly):
    def __init__(self):
        super().__init__()
        self.layer_order = {}
        self.layers = {}
        self.surfaces = []

    @classmethod
    def from_idf(cls, name, building, surfaces, service_life):
        data = building.idf_constructions_data['constructions'][name]
        construction = cls.create(data['name'], building)
        construction.layer_order = data['layers']
        construction.get_layers(building)
        construction.surfaces = surfaces
        construction.set_service_life(35) # TODO: implement reading POD|LCA RSL Category from constructions
        construction.add_materials(building, service_life)
        for surface in surfaces:
            surface.add_construction(construction)
        return construction
    
    def add_materials(self, building, service_life):
        
        default_database_entry_map = DataImporter.csv_to_dict(config['file_paths']['building']['TEMPLATE_MATERIALS_DEFAULT_MAP'], 'template model material')

        area = self.area
        for lk in self.layers:
            mat_type = self.layers[lk].material_property.__type__
            if mat_type != 'EnvelopeMaterialAirGap' and mat_type != 'WindowMaterialGas':
                mat_name = self.layers[lk].material_property.name
                quantity = area * self.layers[lk].thickness #FIXME: not all impacts are declared per volume... 
                material = EnvelopeMaterial.new(parent=self,
                                                name=mat_name,
                                                qty=quantity,
                                                unit=CUBIC_METER,
                                                material_database_entry=default_database_entry_map[mat_name]['impact database entry'],
                                                product_year=building.get_built_year())
                                                            
                self.add_material(material)

    @property
    def area(self):
        area = 0
        for s in self.surfaces:
            area += s.area
        return area

    def get_layers(self, building):
        for mk in self.layer_order:
            name = self.layer_order[mk]
            layer = Layer.from_idf(name, building)
            self.layers[mk] = layer

if __name__ == '__main__':
    pass

    # from pod_lca.utilities import config


    # for i in range(50): print('')


    # name = 'Typical Insulated Steel Framed Exterior Wall-R16'
    # path = config['file_paths']['operational']['CONSTRUCTIONS']
    # c = Construction.from_idf(name, path)

    # print(c.layers['3'].material.name)