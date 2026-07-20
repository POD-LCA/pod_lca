__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from math import isnan

from pod_lca.lca_modules.operational.read_write import find_material_by_name
from pod_lca.units import Quantity as Q
from pod_lca.units import INCH 
from pod_lca.units import JOULE 
from pod_lca.units import KELVIN
from pod_lca.units import KILOGRAM
from pod_lca.units import METER
from pod_lca.units import SQUARE_METER
from pod_lca.units import WATT


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
    
    @classmethod
    def from_database(cls, name, database_entry_name):
        """Creates an instance of the material properties class from the
        default database. 

        Parameters
        ----------
        name : str
            Name of the material property to be read in the default database. 
        """
        material_prop = cls()
        material_prop.name = name
        material_prop.database_entry_name = database_entry_name

        return material_prop

    def get_thermal_resistance(self, thickness=None, building=None):
        if (self.thermal_resistance is None) or (isnan(self.thermal_resistance.value)):
            if building:
                RSI_per_inch = building.material_impact_database.get_data_entry(self.database_entry_name)['RSI /inch (m2C/W)']

                thickness = thickness.convert_to(INCH)
                thermal_resistance_val = RSI_per_inch * thickness.value 

                self.thermal_resistance = Q(thermal_resistance_val, (SQUARE_METER * KELVIN) / WATT)

        return self.thermal_resistance

    def get_roughness(self, building=None):
        if self.roughness is None:
            if building:
                self.roughness = building.material_impact_database.get_data_entry(self.database_entry_name)['Roughness']
            else:
                raise ValueError

        return self.roughness

    def get_conductivity(self, building=None):
        if (self.conductivity is None) or (isnan(self.conductivity.value)):
            if building:
                conductivity_val = building.material_impact_database.get_data_entry(self.database_entry_name)['Thermal conductivity']
                self.conductivity = Q(conductivity_val, WATT/(METER*KELVIN)) 
            else:
                raise ValueError
        
        return self.conductivity
    
    def get_resistivity(self, thickness=None, building=None):
        """Returns the thermal resistivity of the layer

        Parameters
        ----------
        thickness : ~pod_lca.units.Quantity
            (optional) The thickness of the layer if the resistivity should be computed 
            for a different thickness than currently assigned to the layer. 

        Returns
        -------
        ~pod_lca.units.Quantity
            The thermal resistivity of the layer. 
        """
        pass        
    
    def get_density(self, building=None, of_unit=None, thickness=None):
        if self.density is None:
            if building:
                database = building.material_impact_database
                density_val = database.get_data_entry(self.database_entry_name)[database.get_density_key()]
                density_unit = database.get_data_entry(self.database_entry_name)[database.get_density_unit_key()]

                self.density = Q(density_val, density_unit) 
            else:
                raise ValueError
            
        if of_unit:
            if (of_unit.qty_measured == self.density.unit.qty_measured):
                self.density = self.density.convert_to(of_unit) 
            elif thickness:   
                if (of_unit.qty_measured == (self.density / thickness).unit.qty_measured):
                    self.density = self.density / thickness
                elif (of_unit.qty_measured == (self.density * thickness).unit.qty_measured):
                    self.density = self.density * thickness
                else:
                    raise ValueError("Cannot compute the density in the desired units.")
                self.density = self.density.convert_to(of_unit)
            else:
                raise NotImplementedError

        return self.density
    
    def get_specific_heat(self, building=None):
        if self.specific_heat is None:
            if building:
                database = building.material_impact_database
                specific_heat_val = database.get_data_entry(self.database_entry_name)["Specific Heat J/kg-K"]

                self.specific_heat = Q(specific_heat_val, JOULE / (KILOGRAM * KELVIN)) 
            else:
                raise ValueError
        
        return self.specific_heat

    def get_thermal_absorptance(self, building=None):
        if self.thermal_absorptance is None:
            if building:
                self.thermal_absorptance = building.material_impact_database.get_data_entry(self.database_entry_name)["Thermal Absorptance"]
            else:
                raise ValueError
        
        return self.thermal_absorptance

    def get_solar_absorptance(self, building=None):
        if self.solar_absorptance is None:
            if building:
                self.solar_absorptance = building.material_impact_database.get_data_entry(self.database_entry_name)["Solar Absorptance"]
            else:
                raise ValueError
        
        return self.solar_absorptance

    def get_visible_absorptance(self, building=None):
        if self.visible_absorptance is None:
            if building:
                self.visible_absorptance = building.material_impact_database.get_data_entry(self.database_entry_name)["Visible Absorptance"]
            else:
                raise ValueError
        
        return self.visible_absorptance
    

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
        self.__type__ = 'MaterialPropertyMass'
        self.density = None
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

    def get_thermal_resistance(self, thickness=None, building=None):
        resistivity =  self.get_conductivity(building).invert()
        return resistivity * thickness

    def get_resistivity(self, thickness=None, building=None):
        """Returns the thermal resistivity of the layer

        Parameters
        ----------
        thickness : ~pod_lca.units.Quantity
            (optional) The thickness of the layer if the resistivity should be computed 
            for a different thickness than currently assigned to the layer. 

        Returns
        -------
        ~pod_lca.units.Quantity
            The thermal resistivity of the layer. 
        """
        return self.get_conductivity(building).invert()


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

    def get_thermal_resistance(self, thickness=None, building=None):
        if (self.thermal_resistance is None) or (isnan(self.thermal_resistance.value)):
            if building:
                thermal_resistance_val = building.material_impact_database.get_data_entry(self.database_entry_name)['RSI /inch (m2C/W)']
                self.thermal_resistance = Q(thermal_resistance_val, (SQUARE_METER * KELVIN) / WATT)

        return self.thermal_resistance
    

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
    
    def get_thermal_resistance(self, thickness, building=None):
        return thickness / self.get_conductivity(building)

    def get_resistivity(self, thickness=None, building=None):
        """Returns the thermal resistivity of the layer

        Parameters
        ----------
        thickness : ~pod_lca.units.Quantity
            (optional) The thickness of the layer if the resistivity should be computed 
            for a different thickness than currently assigned to the layer. 

        Returns
        -------
        ~pod_lca.units.Quantity
            The thermal resistivity of the layer. 
        """
        return self.get_thermal_resistance(thickness, building) / thickness
    

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
        self.optical_data_type                          = 'SpectralAverage'
        self.win_glass_spectral_data_name               = ''
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
        self.dirt_correction_factor                     = 1
        self.solar_diffusing                            = 'No'

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
    

    def get_solar_transmittance(self, building=None):
        if self.solar_transmittance is None:
            if building:
                database = building.material_impact_database
                self.solar_transmittance = database.get_data_entry(self.database_entry_name)["Solar Transmittance at Normal Incidence"]
            else:
                raise ValueError
        
        return self.solar_transmittance

    def get_front_solar_reflectance(self, building=None):
        if self.front_solar_reflectance is None:
            if building:
                database = building.material_impact_database
                self.front_solar_reflectance = database.get_data_entry(self.database_entry_name)["Front Side Visible Reflectance at Normal Incidence"]
            else:
                raise ValueError
        
        return self.front_solar_reflectance
    
    def get_back_solar_reflectance(self, building=None):
        if self.back_solar_reflectance is None:
            if building:
                database = building.material_impact_database
                self.back_solar_reflectance = database.get_data_entry(self.database_entry_name)["Back Side Solar Reflectance at Normal Incidence"]
            else:
                raise ValueError
        
        return self.back_solar_reflectance
    
    def get_front_visible_reflectance(self, building=None):
        if self.front_visible_reflectance is None:
            if building:
                database = building.material_impact_database
                self.front_visible_reflectance = database.get_data_entry(self.database_entry_name)["Front Side Visible Reflectance at Normal Incidence"]
            else:
                raise ValueError
        
        return self.front_visible_reflectance

    def get_back_visible_reflectance(self, building=None):
        if self.back_visible_reflectance is None:
            if building:
                database = building.material_impact_database
                self.back_visible_reflectance = database.get_data_entry(self.database_entry_name)["Back Side Visible Reflectance at Normal Incidence"]
            else:
                raise ValueError
        
        return self.back_visible_reflectance
    
    def get_visible_transmittance(self, building=None):
        if self.visible_transmittance is None:
            if building:
                database = building.material_impact_database
                self.visible_transmittance = database.get_data_entry(self.database_entry_name)["Visible Transmittance at Normal Incidence"]
            else:
                raise ValueError
        
        return self.visible_transmittance

    def get_infrared_transmittance(self, building=None):
        if self.infrared_transmittance is None:
            if building:
                database = building.material_impact_database
                self.infrared_transmittance = database.get_data_entry(self.database_entry_name)["Infrared Transmittance at Normal Incidence"]
            else:
                raise ValueError
        
        return self.infrared_transmittance

    def get_front_infrared_hemispherical_emissivity(self, building=None):
        if self.front_infrared_hemispherical_emissivity is None:
            if building:
                database = building.material_impact_database
                self.front_infrared_hemispherical_emissivity = database.get_data_entry(self.database_entry_name)["Front Side Infrared Hemispherical Emissivity"]
            else:
                raise ValueError
        
        return self.front_infrared_hemispherical_emissivity
    
    def get_back_infrared_hemispherical_emissivity(self, building=None):
        if self.back_infrared_hemispherical_emissivity is None:
            if building:
                database = building.material_impact_database
                self.back_infrared_hemispherical_emissivity = database.get_data_entry(self.database_entry_name)["Back Side Infrared Hemispherical Emissivity"]
            else:
                raise ValueError
        
        return self.back_infrared_hemispherical_emissivity


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