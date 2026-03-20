__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from . import EnvelopeMaterial
from ..building_envelope import Layer
from pod_lca.lca_modules.building.assembly import Assembly
from ...units import CUBIC_METER, METER
from ...units import Quantity as Q

from ...utilities import DataImporter
from ...utilities import config
from pod_lca.lca_modules.operational.read_write import find_constructions
from pod_lca.lca_modules.operational.read_write import find_materials
from pod_lca.lca_modules.operational.read_write import find_no_mass_materials
from pod_lca.lca_modules.operational.read_write import find_materials_air_gap
from pod_lca.lca_modules.operational.read_write import find_glazing_materials
from pod_lca.lca_modules.operational.read_write import find_gas_materials


class Construction(Assembly):
    def __init__(self):
        super().__init__()
        self.layer_order = {}
        self.layers = {}
        self.surfaces = {}

    @classmethod
    def from_idf(cls, name, idf_path):
        cdata = find_constructions(idf_path, {})['constructions'][name]
        layers = cdata['layers']
        ldata = find_materials(idf_path, {})
        ldata = find_no_mass_materials(idf_path, ldata)
        ldata = find_materials_air_gap(idf_path, ldata)
        ldata = find_glazing_materials(idf_path, ldata)
        ldata = find_gas_materials(idf_path, ldata)
        ldata = ldata['materials']

        layers_ = {}
        for lk in layers:
            mdata = ldata[layers[lk]]
            if 'thickness' in ldata[layers[lk]]:
                thickness = ldata[layers[lk]]['thickness']
            else:
                thickness = Q(0, METER)
            l = Layer.from_data(mdata, thickness, None)
            layers_[lk] = l

        construction = cls.create(name)
        construction.from_layers(name, layers_)
        return construction
    
    @classmethod
    def from_layers(cls, name, layers):
        construction = cls.create(name)
        construction = cls.create(name)
        construction.layer_order = {lk: layers[lk].name for lk in layers}
        construction.layers = layers
        return construction


    def set_building(self):
        """Set data from building level."""
        building = self.get_building()
        if building is not None:
            building.add_assembly(self)

            for material in self.get_materials():
                material.set_building()


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