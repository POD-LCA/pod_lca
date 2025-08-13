
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import CarbonStorage
from ..impacts import Emissions
from ..impacts import Impacts
from ..materials_screening import Master


class BuildingMaterial(Master):

    def __init__(self):
        self.name = None

        # LCA attributes
        self.material_database_entry = None
        self.qty = None
        self.unit = None
        self.density = None
        self.sctg_code = None
        self.eol_product = None

        # Operational Energy attributes
        self.roughness = None
        self.conductivity = None
        self.specific_heat = None
        self.thermal_absorptance = None
        self.solar_absorptance = None
        self.visible_absorptance = None

        # impacts
        self.unit_impacts = None
        self.unit_emission_inventories = None


    @classmethod
    def new_structural_material(cls, name, qty, unit, material_database_entry):
        """ Create new structural material.
        
        Parameters
        ----------
        
        """
        material = cls()
        
        material.set_name(name)
        material.set_qty(qty)
        material.set_unit(unit)
        material.unit_impacts = Impacts.from_parent(material)
        material.unit_emissions = Emissions.from_parent(material)
        material.unit_carbon_storage = CarbonStorage.from_parent(material)
        # material.set_impact_database_entry(material_database_entry)
        # TODO: set impact database

        return material

    @classmethod
    def new_enclosure_material(cls, name, ):
        pass


    # TODO add getters and setters ---  Should this inherit from Master Object
    def set_qty(self, qty ):
        pass


