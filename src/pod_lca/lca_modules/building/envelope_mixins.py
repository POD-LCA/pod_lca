__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from ..operational import find_constructions
from ..operational import find_materials
from ..operational import find_materials_air_gap
from ..operational import find_no_mass_materials
from ..operational import find_gas_materials
from ..operational import find_glazing_materials





class EnvelopeMixins():
    def read_constructions_data(self, path):
        find_constructions(path, self.idf_constructions_data)

    def read_material_properties_data(self, path):
        find_materials(path, self.idf_material_properties)
        find_materials_air_gap(path, self.idf_material_properties)
        find_no_mass_materials(path, self.idf_material_properties)
        find_gas_materials(path, self.idf_material_properties)
        find_glazing_materials(path, self.idf_material_properties)