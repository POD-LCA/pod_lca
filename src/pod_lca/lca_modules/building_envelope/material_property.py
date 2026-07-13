__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


from pod_lca.lca_modules.operational.read_write import find_material_by_name
from pod_lca.lca_modules.operational.read_write import find_materials
from pod_lca.lca_modules.operational.read_write import find_no_mass_materials
from pod_lca.lca_modules.operational.read_write import find_materials_air_gap


class EnvelopeMaterialProperty(object):
    """ The envelope material properties base class.
    
    Attributes
    ----------
    name : str
        The name of the material propperty instance. 
    """
    def __init__(self):
        self.name               = None
        # Operational Energy attributes
        pass
    
    @classmethod
    def from_data(cls, data):
        """Creates an instance of the material properties class from a data
        dictionary. The dictionary should be made using the to_data method. 

        Parameters
        ----------
        data : dict
            The data dictionary with all required properties. 
        """
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


    @classmethod
    def from_idf(cls, name, filepath):
        """Creates an instance of the material properties class from an
        IDF file. 

        Parameters
        ----------
        name : str
            Name of the material property to be read in the IDF file. 

        filepath : str
            Path to the IDF file. 
        """
        data = find_material_by_name(filepath, name)
        return cls.from_data(data)


class EnvelopeMaterialPropertyMass(EnvelopeMaterialProperty):
    """ Defines an envelope MASS material properties class. To be used
    with materials with thermal mass properties, such as interior facing 
    surfaces. 
    
    Attributes
    ----------
    __type__ : str
        Contains the specific material property type. 

    roughness :  str
        Energy plus material roughness setting 

    conductivity :  ~pod_lca.units.Quantity
        Thermal conductivity
    
    speficic_heat :  ~pod_lca.units.Quantity
        Material specific_heat

    thermal_absorptance :  ~pod_lca.units.Quantity
        Material thermal absorptance

    solar_absorptance :  ~pod_lca.units.Quantity
        Material solar absorptance
    
    visible_absorptance :  ~pod_lca.units.Quantity
        Material visible absorptance
    """
    def __init__(self):
        super().__init__()  
        # Operational Energy attributes
        self.__type__ = 'EnvelopeMaterialPropertyMass'
        self.roughness = None
        self.conductivity = None
        self.specific_heat = None
        self.thermal_absorptance = None
        self.solar_absorptance = None
        self.visible_absorptance = None

    @classmethod
    def from_data(cls, data):
        """Creates an instance of the MASS material properties class from a data
        dictionary. The dictionary should be made using the to_data method. 

        Parameters
        ----------
        data : dict
            The data dictionary with all required properties. 
        """
        material = cls()
        material.__type__            = 'MaterialPropertyMass'
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


class EnvelopeMaterialPropertyAirGap(EnvelopeMaterialProperty):
    """ Defines an envelope Air Gap material properties class. 
    
    Attributes
    ----------
    __type__ : str
        Contains the specific material property type. 

    conductivity :  ~pod_lca.units.Quantity
        Thermal resistance of air
    """
    def __init__(self):
        super().__init__()  
        # Operational Energy attributes
        self.__type__ = 'EnvelopeMaterialPropertyAirGap'
        self.thermal_resistance = None

    @classmethod
    def from_data(cls, data):
        """Creates an instance of the Air Gap material properties class from a data
        dictionary. The dictionary should be made using the to_data method. 

        Parameters
        ----------
        data : dict
            The data dictionary with all required properties. 
        """
        material = cls()
        material.__type__            = 'EnvelopeMaterialPropertyAirGap'
        material.name                = data['name']
        material.thermal_resistance  = data['thermal_resistance']
        return material


class EnvelopeMaterialPropertyNoMass(EnvelopeMaterialProperty):
    """ Defines an envelope No MASS material properties class. 
    
    Attributes
    ----------
    __type__ : str
        Contains the specific material property type. 

    roughness :  str
        Energy plus material roughness setting 

    thermal_resistance :  ~pod_lca.units.Quantity
        Material thermal resistance

    thermal_absorptance :  ~pod_lca.units.Quantity
        Material thermal absorptance

    solar_absorptance :  ~pod_lca.units.Quantity
        Material solar absorptance
    
    visible_absorptance :  ~pod_lca.units.Quantity
        Material visible absorptance

    thickness : ~pod_lca.units.Quantity
        Material thickness. Will be overwritten by layer thickness. 
    """
    def __init__(self):
        super().__init__()  
        self.__type__            = 'MaterialPropertyNoMass'
        self.roughness           = None
        self.conductivity        = None
        self.thermal_absorptance = None
        self.solar_absorptance   = None
        self.visible_absorptance = None
        self.thickness           = None

    @classmethod
    def from_data(cls, data):
        """Creates an instance of the No MASS material properties class from a data
        dictionary. The dictionary should be made using the to_data method. 

        Parameters
        ----------
        data : dict
            The data dictionary with all required properties. 
        """
        material = cls()
        material.__type__            = 'MaterialPropertyNoMass'
        material.name                = data['name']
        material.roughness           = data['roughness']
        material.conductivity        = data['conductivity'] 
        material.thermal_absorptance = data['thermal_absorptance'] 
        material.solar_absorptance   = data['solar_absorptance']
        material.visible_absorptance = data['visible_absorptance']
        material.thickness           = data['thickness']
        return material
    
    @property
    def thermal_resistance(self):
        return self.thickness / self.conductivity

class WindowMaterialPropertyGlazing(EnvelopeMaterialProperty):
    """ Defines an envelope Glazing material properties class. 
    
    Attributes
    ----------
    __type__ : str
        Contains the specific material property type. 

    optical_data_type : str
        Material optical data type

    win_glass_spectral_data_name : str
        Material Window Glass Spectral Data Set Name           

    solar_transmittance : ~pod_lca.units.Quantity
        Material Solar Transmittance at Normal Incidence                    

    front_solar_reflectance : ~pod_lca.units.Quantity
        Material Front Side Solar Reflectance at Normal Incidence                

    back_solar_reflectance : ~pod_lca.units.Quantity
        Material Back Side Solar Reflectance at Normal Incidence                 

    visible_transmittance : ~pod_lca.units.Quantity
        Material Visible Transmittance at Normal Incidence                  

    front_visible_reflectance : ~pod_lca.units.Quantity
        Material Front Side Visible Reflectance at Normal Incidence              

    back_visible_reflectance : ~pod_lca.units.Quantity
        Material Back Side Visible Reflectance at Normal Incidence               

    infrared_transmittance : ~pod_lca.units.Quantity
        Material Infrared Transmittance at Normal Incidence                 

    front_infrared_hemispherical_emissivity : ~pod_lca.units.Quantity
        Material Front Side Infrared Hemispherical Emissivity

    back_infrared_hemispherical_emissivity : ~pod_lca.units.Quantity
        Material Back Side Infrared Hemispherical Emissivity 

    conductivity : ~pod_lca.units.Quantity
        Material Conductivity                           

    dirt_correction_factor : ~pod_lca.units.Quantity
        Material Dirt Correction Factor for Solar and Visible Transmittance                 

    solar_diffusing  : str
        Does the material diffuse sun yes or no.                         
    """
    def __init__(self):
        super().__init__()  
        self.__type__                                   = 'WindowMaterialPropertyGlazing'
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
    def from_data(cls, data):
        """Creates an instance of the Glazing material properties class from a data
        dictionary. The dictionary should be made using the to_data method. 

        Parameters
        ----------
        data : dict
            The data dictionary with all required properties. 
        """
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
    

class WindowMaterialPropertyGas(EnvelopeMaterialProperty):
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
        self.__type__          = 'WindowMaterialPropertyGas'
        self.name              = 'WindowMaterialPropertyGas'                   
        self.gas_type          = None
    
    @classmethod
    def from_data(cls, data):
        """Creates an instance of the Gas material properties class from a data
        dictionary. The dictionary should be made using the to_data method. 

        Parameters
        ----------
        data : dict
            The data dictionary with all required properties. 
        """
        material = cls()
        material.__type__           = data.get('__type__') or {}
        material.name               = data.get('name') or {}
        material.gas_type           = data.get('gas_type') or {}

        return material


if __name__ == '__main__':
    pass