
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import CarbonStorage
from ..impacts import Emissions
from ..impacts import Impacts
from ..materials_screening import Product
from ..operational import find_materials
from ..operational import find_no_mass_materials
from ..operational import find_gas_materials
from ..operational import find_glazing_materials
from ...units import UNITS_MAP


class BuildingMaterial(Product):
    """ Subordinate level of construction for building components.
    
    Attributes
    ----------
    name : str
        Name of the building material.
    material_database_entry : str
        Identifier of LCA database entry corresponding to the material.
    sctg_code : int
        SCTG code mapped to the material.
    eol_product : str
        End-of-life product name corresponding to the material.
    density : float
        Density of the material.
    """
    
    def __init__(self):
        super().__init__()
        self.name = None

        # LCA attributes
        self.material_database_entry = None
        self.sctg_code = None
        self.eol_product = None
        self.bio_based = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new_structural_material(cls, parent, name, qty, unit, material_database_entry):
        """ Create new structural material.
        
        Parameters
        ----------
        parent : ~pod_lca.building.BuildingComponent
            Building component to whcih the material belong.
        name : str
            Name of the product.
        qty : float
            Product quantity.
        unit : ~pod_lca.units.Unit
            Unit of measurement.            
        material_database_entry : str
            Name of the impact database entry from which to use impacts.
        """
        material = cls()
        
        material.set_parent(parent)
        material.set_name(name)
        material.set_qty(qty)
        material.set_unit(unit)
        material.impacts = Impacts.from_parent(material)
        material.emissions = Emissions.from_parent(material)
        material.carbon_storage = CarbonStorage.from_parent(material)
        material.unit_impacts = Impacts.from_parent(material)
        material.unit_emissions = Emissions.from_parent(material)
        material.unit_carbon_storage = CarbonStorage.from_parent(material)
        material.set_impact_database_entry(material_database_entry)
        material.set_sctg_code(material_database_entry)
        material.set_eol_material(material_database_entry)
        material.set_density(material_database_entry)

        return material

    # ================================
    # Setters
    # ================================
    def set_parent(self, parent):
        """ Set the parent building component of the material.
        
        Parameters
        ----------
        parent : ~pod_lca.building.BuildingComponent
            Building componet to which the material belong.
        """
        self.parent = parent

        return self
    
    def set_density(self, material_database_entry):
        """ Set the density of the material.
        
        Parameters
        ----------
        material_database_entry : str
            Name of the impact database entry from which to use impacts.        
        """
        database = self.get_impact_database()
        data_entry = database.get_data_entry(material_database_entry)

        super().set_density(data_entry['Density'], UNITS_MAP[data_entry['Density unit']])

        return self
    
    def set_sctg_code(self, material_database_entry):
        """ Set the Standard Classification of Transported Goods (SCTG) code of the material.

        Parameters
        ----------
        material_database_entry : str
            Name of the impact database entry from which to use impacts.        
        """
        database = self.get_impact_database()
        data_entry = database.get_data_entry(material_database_entry)
        self.sctg_code = data_entry['sctg code']

    def set_eol_material(self, material_database_entry):
        """ Set the end-of-life product corresponding to the material.

        Parameters
        ----------
        material_database_entry : str
            Name of the impact database entry from which to use impacts.        
        """
        database = self.get_impact_database()
        data_entry = database.get_data_entry(material_database_entry)
        self.eol_product = data_entry['eol material']
        if 'bio-based' in data_entry:
            self.bio_based = data_entry['bio-based']

    # ================================
    # Getters
    # ================================
    def get_parent(self):
        """ Get the parent building component of the material.
        
        Returns
        -------
        ~pod_lca.building.BuildingComponent
            Building componet to which the material belong.
        """
        return self.parent  

    def get_project(self):
        """ Get the project (building) of the component.
        
        Returns
        -------
        ~pod_lca.building.Building
            Building project to which the component belong.
        """
        return self.get_parent().get_parent()
    
    def get_eol_material(self):
        """ Get the end-of-life product corresponding to the material.

        Returns
        -------
        str
            End-of-life product name corresponding to the material.      
        """
        return self.eol_product  
    
    def get_bio_based(self):
        """ Get the bio-based nature of the material.
        
        Returns
        -------
        bool
            True if the material is bio-based.   
        """
        return self.bio_based

    def get_building(self):
        """ Get the building to which this building material belong.

        Returns
        -------
        ~pod_lca.building.Building
            Building to which this building material belong.       
        """
        return self.get_parent().get_parent()
    
    def get_impact_database(self):
        """ Get the impact database giving the A1-A3 impacts of the building materials.

        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            Impact database object.
        """
        return self.get_building().get_material_impact_database()

    def get_transportation_manager(self):
        """ Get the transportation manager corresponding to the product.
        
        Returns
        -------
        ~pod_lca.transportation.TransportationManager
            Transportation manager
        """
        return self.get_building().get_transportation_manager()
    
    # @classmethod
    # def new_enclosure_material(cls,
    #                            name,
    #                            roughness,
    #                            conductivity,
    #                            density,
    #                            specific_heat,
    #                            thermal_absorptance,
    #                            solar_absorptance,
    #                            visible_absorptance):
    #     material = cls()
    #     material.name                = name               
    #     material.roughness           = roughness          
    #     material.conductivity        = conductivity       
    #     material.density             = density            
    #     material.specific_heat       = specific_heat      
    #     material.thermal_absorptance = thermal_absorptance
    #     material.solar_absorptance   = solar_absorptance  
    #     material.visible_absorptance = visible_absorptance
    #     return material

    # @classmethod
    # def new_enclosure_material_from_idf(cls, name, path):
    #     data = {}
    #     find_materials(path, data)
    #     if name not in data:
    #         find_no_mass_materials(path, data)
    #     if name not in data:
    #         find_gas_materials(path, data)
    #     if name not in data:
    #         find_glazing_materials(path, data)

    #     data = data['materials'][name]
    #     material = cls()
    #     material.name                = data['name']
    #     material.roughness           = data['roughness']
    #     material.conductivity        = data['conductivity']
    #     material.density             = data['density']
    #     material.specific_heat       = data['specific_heat']
    #     material.thermal_absorptance = data['thermal_absorptance']
    #     material.solar_absorptance   = data['solar_absorptance']
    #     material.visible_absorptance = data['visible_absorptance']
    #     return material


class BuildingEnvelopeMaterial(BuildingMaterial):
    def __init__(self):
        super().__init__()  
        # Operational Energy attributes
        self.__type__ = 'Material'
        self.roughness = None
        self.conductivity = None
        self.specific_heat = None
        self.thermal_absorptance = None
        self.solar_absorptance = None
        self.visible_absorptance = None

    @classmethod
    def from_idf_data(cls, data):
        material = cls()
        material.__type__            = 'Material'
        material.name                = data['name']
        material.roughness           = data['roughness']
        material.thickness           = data['thickness']
        material.conductivity        = data['conductivity']
        material.density             = data['density']
        material.specific_heat       = data['specific_heat']
        material.thermal_absorptance = data['thermal_absorptance']
        material.solar_absorptance   = data['solar_absorptance']
        material.visible_absorptance = data['visible_absorptance']
        return material


class BuildingEnvelopeMaterialNoMass(BuildingMaterial):
    def __init__(self):
        super().__init__()  
        self.name                = None
        self.__type__            = 'MaterialNoMass'
        self.roughness           = None
        self.thermal_resistance  = None
        self.solar_absorptance   = None
        self.visible_absorptance = None

    @classmethod
    def from_idf_data(cls, data):
        material = cls()
        material.__type__            = 'MaterialNoMass'
        material.name                = data['name']
        material.roughness           = data['roughness']
        material.thermal_resistance  = data['thermal_resistance'] 
        material.solar_absorptance   = data['solar_absorptance']
        material.visible_absorptance = data['visible_absorptance']
        return material
    

class WindowMaterialGlazing(BuildingMaterial):

    def __init__(self):
        super().__init__()  
        self.__type__                                   = 'WindowMaterialGlazing'
        self.name                                       = 'WindowMaterialGlazing'
        self.optical_data_type                          = None
        self.win_glass_spectral_data_name               = None
        self.solar_transmittance                        = None
        self.front_solar_reflectance                    = None
        self.back_solar_reflectance                     = None
        self.visible_transmittance                      = None
        self.front_visible_reflectance                  = None
        self.back_visible_reflectance                   = None
        self.infrared_transmittance                     = None
        self.front_infrared_hemispherical_emissivity    = None
        self.back_infrared_hemispherical_emissivity     = None
        self.conductivity                               = None
        self.dirt_correction_factor                     = None
        self.solar_diffusing                            = None

    @classmethod
    def from_idf_data(cls, data):
        material = cls()
        material.name                                    = data.get('name') or {}
        material.optical_data_type                       = data.get('optical_data_type') or {}
        material.win_glass_spectral_data_name            = data.get('win_glass_spectral_data_name') or ''
        material.solar_transmittance                     = data.get('solar_transmittance') or {}
        material.front_solar_reflectance                 = data.get('front_solar_reflectance') or {}
        material.back_solar_reflectance                  = data.get('back_solar_reflectance') or {}
        material.visible_transmittance                   = data.get('visible_transmittance') or {}
        material.front_visible_reflectance               = data.get('front_visible_reflectance') or {}
        material.back_visible_reflectance                = data.get('back_visible_reflectance') or {}
        material.infrared_transmittance                  = data.get('infrared_transmittance') or ''
        material.front_infrared_hemispherical_emissivity = data.get('front_infrared_hemispherical_emissivity') or {}
        material.back_infrared_hemispherical_emissivity  = data.get('back_infrared_hemispherical_emissivity') or {}
        material.conductivity                            = data.get('conductivity') or {}
        material.dirt_correction_factor                  = data.get('dirt_correction_factor') or {}
        material.solar_diffusing                         = data.get('solar_diffusing') or {}

        return material
    

class WindowMaterialGas(object):
    """
    Datastructure containing a WindowMaterialGass for Energy+ analysis

    Parameters
    ----------
    __type__ : str
        Material __type__ 
    name     : str
        Material name     
    gas_type : str
        Material gas_type 

    """
    def __init__(self):
        self.__type__          = 'WindowMaterialGas'
        self.name              = 'WindowMaterialGas'                   
        self.gas_type          = None
    
    @classmethod
    def from_idf_data(cls, data):
        material = cls()
        material.__type__           = data.get('__type__') or {}
        material.name               = data.get('name') or {}
        material.gas_type           = data.get('gas_type') or {}

        return material

