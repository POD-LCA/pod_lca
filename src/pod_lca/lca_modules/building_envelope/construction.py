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
    """ The structural assemblies of the building.
    
    Attributes
    ----------
    layer_order : list
        List of layer keys ordered from the outside to the inside.
    layers : (dict of) ~pod_lca.building_envelope.Layer
        Dictionary of all the layers in the construction. 
    surfaces : (dict of) ~pod_lca.building_envelope.Surface
        Surfaces objects for the consrtruction. 

    """
    def __init__(self):
        super().__init__()
        self.layer_order = []
        self.layers = {}
        self.surfaces = {}
        
    @classmethod
    def from_idf(cls, name, idf_path):
        """ Create an envelope construction from IDF data.
        
        Parameters
        ----------
        name : str
            Name of the construction to be imported from the IDF, as written in the file.
        idf_path : str
            Path to the IDF file.  

        Returns
        -------
        ~pod_lca.building_envelope.Construction
            The created construction. 
        """
        cdata = find_constructions(idf_path, {})['constructions'][name]
        layers = cdata['layers']
        ldata = find_materials(idf_path, {})
        ldata = find_no_mass_materials(idf_path, ldata)
        ldata = find_materials_air_gap(idf_path, ldata)
        ldata = find_glazing_materials(idf_path, ldata)
        ldata = find_gas_materials(idf_path, ldata)
        ldata = ldata['materials']

        layers_ = {}
        for i in range(len(layers)):
            mdata = ldata[layers[i]]
            if 'thickness' in ldata[layers[i]]:
                thickness = ldata[layers[i]]['thickness']
            else:
                thickness = Q(0, METER)
            l = Layer.from_data(mdata, thickness, None)
            layers_[i] = l

        construction = cls.from_layers(name, layers_)
        return construction
    
    @classmethod
    def from_layers(cls, name, layers):
        """ Create an envelope construction from a list of layers.
        
        Parameters
        ----------
        name : str
            Name of the construction to be created.
        layers : (list of) ~pod_lca.building_envelope.Layer
            The layers to be included in the construction.  

        Returns
        -------
        ~pod_lca.building_envelope.Construction
            The created construction. 
        """
        construction = cls.from_materials(name)
        construction.layer_order = [lk for lk in layers]
        construction.layers = layers

        for lk in construction.layers:
            construction.layers[lk].parent_construction = construction

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
        """Set the materials for the construction. 
        """
        default_database_entry_map = DataImporter.csv_to_dict(config['file_paths']['building']['IDF_IMPACT_DATA_PRODUCT_MAP'], 'IDF Material Name')
        
        area = self.area
        for layer in self.get_constituent_materials():
            mat_type = layer.material_property.__type__
            if (not layer.is_structural) and (mat_type != 'EnvelopeMaterialAirGap') and (mat_type != 'WindowMaterialGas'):
                mat_name = layer.material_property.name

                database_declared_qty_in = UNITS_MAP[default_database_entry_map[mat_name]["LCI Database Declared Unit"]].get_qty_measured()

                quantity = layer.get_quantity(area, database_declared_qty_in)

                material = EnvelopeMaterial.new(name=mat_name,
                                                qty=quantity.value,
                                                unit=quantity.unit,
                                                material_database_entry=default_database_entry_map[mat_name]['LCI Database Product Name'],)
                material.set_service_life_category(default_database_entry_map[mat_name]["POD|LCA RSL Category"])


                self.add_material(material)

    @property
    def area(self):
        """ Returns the surface area of the construction.
        
        Returns
        -------
        ~pod_lca.units.Quantity
            The surface area of the construction. 
        """
        if self.surfaces:
            area = 0
            for sk in self.surfaces:
                area += self.surfaces[sk].area
            return area
        else:
            return Q(0, SQUARE_METER)


    def get_constituent_materials(self):
        constituent_materials = []
        for layer in self.layers.values():
            constituent_materials.append(layer)
            if layer.anciallary_materials:
                constituent_materials.extend(layer.anciallary_materials)

        return constituent_materials

    # def get_layers(self, building):
    #     """ Returns the layers of the construction.
        
    #     Returns
    #     -------
    #     ~pod_lca.units.Quantity
    #         The area of the envelope
    #     """
    #     for mk in self.layer_order:
    #         name = self.layer_order[mk]
    #         layer = Layer.from_idf(name, building)
    #         self.layers[mk] = layer
    

if __name__ == '__main__':
    pass

    # from pod_lca.utilities import config


    # for i in range(50): print('')


    # name = 'Typical Insulated Steel Framed Exterior Wall-R16'
    # path = config['file_paths']['operational']['CONSTRUCTIONS']
    # c = Construction.from_idf(name, path)

    # print(c.layers['3'].material.name)