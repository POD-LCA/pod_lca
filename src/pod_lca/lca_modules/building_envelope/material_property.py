__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


class EnvelopeMaterialProperty(object):
    def __init__(self):
        self.name               = None
        # Operational Energy attributes
        pass


class EnvelopeMaterial(EnvelopeMaterialProperty):
    def __init__(self):
        super().__init__()  
        # Operational Energy attributes
        self.__type__ = 'EnvelopeMaterial'
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

class EnvelopeMaterialAirGap(EnvelopeMaterialProperty):
    def __init__(self):
        super().__init__()  
        # Operational Energy attributes
        self.__type__ = 'EnvelopeMaterialAirGap'
        self.resistace = None

    @classmethod
    def from_idf_data(cls, data):
        material = cls()
        material.__type__            = 'EnvelopeMaterialAirGap'
        material.name                = data['name']
        material.resistance          = data['resistance']
        return material


class EnvelopeMaterialNoMass(EnvelopeMaterialProperty):
    def __init__(self):
        super().__init__()  
        self.name                = None
        self.__type__            = 'MaterialNoMass'
        self.roughness           = None
        self.thermal_resistance  = None
        self.thermal_absorptance = None
        self.solar_absorptance   = None
        self.visible_absorptance = None

    @classmethod
    def from_idf_data(cls, data):
        material = cls()
        material.__type__            = 'MaterialNoMass'
        material.name                = data['name']
        material.roughness           = data['roughness']
        material.thermal_resistance  = data['thermal_resistance'] 
        material.thermal_absorptance = data['thermal_absorptance'] 
        material.solar_absorptance   = data['solar_absorptance']
        material.visible_absorptance = data['visible_absorptance']
        return material
    

class WindowMaterialGlazing(EnvelopeMaterialProperty):

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
    

class WindowMaterialGas(EnvelopeMaterialProperty):
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

if __name__ == '__main__':
    pass