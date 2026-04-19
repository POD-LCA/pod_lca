__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from . import EnvelopeMaterial
from ..building_envelope import Layer
from pod_lca.lca_modules.building.assembly import Assembly
from ...units import METER
from ...units import SQUARE_METER
from ...units import UNITS_MAP
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
        self.surface = None
        
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

        construction = cls.from_layers(name, layers_)
        return construction
    
    @classmethod
    def from_layers(cls, name, layers):
        construction = cls.from_materials(name)
        construction.layer_order = {lk: layers[lk].name for lk in layers}
        construction.layers = layers

        return construction

    def set_building(self):
        """Set data from building level."""
        building = self.get_building()
        if building is not None:
            building.add_assembly(self)

            materials = self.get_materials()
            for material in materials:
                material.set_building()

    def set_materials(self):
        default_database_entry_map = DataImporter.csv_to_dict(config['file_paths']['building']['IDF_IMPACT_DATA_PRODUCT_MAP'], 'IDF Material Name')

        for lk in self.layers:
            mat_type = self.layers[lk].material_property.__type__
            if mat_type != 'EnvelopeMaterialAirGap' and mat_type != 'WindowMaterialGas':
                mat_name = self.layers[lk].material_property.name

                database_declared_qty_in = UNITS_MAP[default_database_entry_map[mat_name]["LCI Database Declared Unit"]].get_qty_measured()
                quantity = self.get_quantity(lk, database_declared_qty_in)

                material = EnvelopeMaterial.new(name=mat_name,
                                                qty=quantity.value,
                                                unit=quantity.unit,
                                                material_database_entry=default_database_entry_map[mat_name]['LCI Database Product Name'],)
                material.set_service_life_category(default_database_entry_map[mat_name]["POD|LCA RSL Category"])


                self.add_material(material)

    @property
    def area(self):
        if self.surface:
            return self.surface.area
        else:
            return Q(0, SQUARE_METER)

    def get_layers(self, building):
        for mk in self.layer_order:
            name = self.layer_order[mk]
            layer = Layer.from_idf(name, building)
            self.layers[mk] = layer

    def get_quantity(self, layer, qty_in):
        """ Returns the quantity of the specified layer.
        
        Parameters
        ----------
        layer : int
            ID of the layer.
        qty_in : {'volume', 'area', 'mass'}
            Requested quantity measured in?
        """
        if qty_in in ['volume', 'mass']:
            return self.area * self.layers[layer].thickness
        elif qty_in in ["area"]:
            return self.area
        else:
            raise ValueError("Quantity request not recognized.")
    

if __name__ == '__main__':
    pass

    # from pod_lca.utilities import config


    # for i in range(50): print('')


    # name = 'Typical Insulated Steel Framed Exterior Wall-R16'
    # path = config['file_paths']['operational']['CONSTRUCTIONS']
    # c = Construction.from_idf(name, path)

    # print(c.layers['3'].material.name)