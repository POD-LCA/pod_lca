
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

import gc

from ..dynamic_radiative_forcing import UniformEmissionProfile
from ..eol.waste import Waste
from ..impacts import CarbonStorage
from ..impacts import Emissions
from ..impacts import Impacts
from ..materials_screening import Product
from ...units import UNITS_MAP
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class Material(Product):
    """ Material (contextual) that makes up assemblies in the building.
    
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
    waste_rate : float
        Waste rate of the material during construction of the assembly/building.
    service_life : float
        Service life of the material in years.
    
    """
    
    def __init__(self):
        super().__init__()
        self.name = None

        # LCA attributes
        self.material_database_entry = None
        self.sctg_code = None
        self.eol_product = None
        self.bio_based = None
        self.waste_rate = None
        self.service_life = None

        # impact objects
        self.waste_obj = None
        self.replacement_product = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new_structural_material(cls, parent, name, qty, unit, material_database_entry, product_year, service_life, waste_rate=0.0):
        """ Create new structural material.
        
        Parameters
        ----------
        parent : ~pod_lca.building.Assembly
            Assembly to whcih the material belong.
        name : str
            Name of the product.
        qty : float
            Product quantity.
        unit : ~pod_lca.units.Unit
            Unit of measurement.            
        material_database_entry : str
            Name of the impact database entry from which to use impacts.
        service_life : float
            Service life of the material in years.
        waste_rate : float
            Waste rate of the material during construction of the assembly/building. Default is 0.
        product_year : int, optional
            Year of the emissions from the material. If None, uses the year of the parent assembly. Default is None.     
        """
        material = cls()

        material.set_parent(parent)
        material.set_name(name)
        material.set_qty(qty)
        material.set_unit(unit)
        material.set_waste_rate(waste_rate)
        material.set_service_life(service_life) 

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
        material.set_production_year(product_year)

        material.set_transportation()
        material.set_waste_product()
        material.set_replacement_material()

        return material
    
    @classmethod
    def copy(cls, other, production_year):
        """ Create a copy of the material.
        
        Parameters
        ----------
        other : ~pod_lca.building.Material
            Material to be copied.
        production_year : int
            Year of the emissions from the material.

        Returns
        -------
        ~pod_lca.building.Material
            Material copied.
        """
        material = cls()

        material.set_parent(other.get_parent())
        material.set_name(other.get_name())
        material.set_qty(other.get_qty())
        material.set_unit(other.get_unit())
        material.set_waste_rate(other.get_waste_rate())
        material.set_service_life(other.get_service_life()) 

        material.impacts = Impacts.from_parent(material)
        material.emissions = Emissions.from_parent(material)
        material.carbon_storage = CarbonStorage.from_parent(material)
        material.unit_impacts = Impacts.from_parent(material)
        material.unit_emissions = Emissions.from_parent(material)
        material.unit_carbon_storage = CarbonStorage.from_parent(material)

        material_database_entry = other.get_impact_database_entry()
        material.set_impact_database_entry(material_database_entry)
        material.set_sctg_code(material_database_entry)
        material.set_eol_material(material_database_entry)
        material.set_density(material_database_entry)
        material.set_production_year(production_year)

        material.set_transportation()
        material.set_waste_product()
        material.set_replacement_material()

        return material

    # ================================
    # Setters
    # ================================
    def set_parent(self, parent):
        """ Set the parent building assembly of the material.
        
        Parameters
        ----------
        parent : ~pod_lca.building.Assembly
            Building componet to which the material belong.
        """
        self.parent = parent
        # TODO: this is created for integration with tranportation/or electricity modules
        # ideally, this should be linked to the assembly, not the building structure

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

    def set_waste_rate(self, waste_rate):
        """ Set the waste rate of the material.
        
        Parameters
        ----------
        waste_rate : float
            Waste rate of the material during construction of the assembly/building.
        """
        self.waste_rate = waste_rate

        return self

    def set_service_life(self, service_life):
        """ Set the service life of the material.
        
        Parameters
        ----------
        service_life : float
            Service life of the material in years.
        """
        self.service_life = service_life

        return self

    def set_waste_product(self):
        """ Set the end-of-life waste product of the material.
        """
        eol_mix_data = DataImporter.csv_to_pandas(config['file_paths']['eol']['EOL_DEFAULT_MIXES'])
            
        eol_material = self.get_eol_material()
        waste_qty = self.get_weight()
        waste_unit = self.get_weight_unit()
        
        if eol_mix_data['Material'].isin([eol_material]).any():
            eol_mix = eol_mix_data[eol_mix_data['Material']== eol_material].drop(labels='Material', axis=1).to_dict(orient='records')[0] 
        elif  eol_mix_data['Material'].isin([config['setup']['eol']['EOL_DEFAULT_KEY']]).any():
            eol_mix = eol_mix_data[eol_mix_data['Material']== config['setup']['eol']['EOL_DEFAULT_KEY']].drop(labels='Material', axis=1).to_dict(orient='records')[0]
        else:
            log("A mix doesnt exist", 0)

        if self.get_bio_based() is not None:
            waste_obj = Waste.new(self, 
                                database_item=eol_material, 
                                qty=waste_qty, 
                                unit=waste_unit, 
                                process_mix=eol_mix, 
                                bio_based=self.get_bio_based())
        else:
            waste_obj = Waste.new(self, 
                                    database_item=eol_material, 
                                    qty=waste_qty, 
                                    unit=waste_unit, 
                                    process_mix=eol_mix)
            
        self.waste_obj = waste_obj

        waste_produced_year = min(self.get_production_year() + self.get_service_life(), # end of material service life
                            self.get_building().get_built_year() + self.get_building().get_life_span()) # end of building life span
        self.waste_obj.set_production_year(waste_produced_year)

        del eol_mix_data
        gc.collect()

        return self

    def set_replacement_material(self):
        """ Set replacement materials for the building based on the service life of its materials.
        """
        material_end_year = self.get_production_year() + self.get_service_life()
        building_end_year = self.get_building().get_built_year() + self.get_building().get_life_span()

        if material_end_year < building_end_year:
            self.replacement_product = Material.copy(self, material_end_year)

    # ================================
    # Getters
    # ================================
    def get_parent(self):
        """ Get the parent building assembly of the material.
        
        Returns
        -------
        ~pod_lca.building.Assembly
            Building assembly to which the material belong.
        """
        return self.parent  

    def get_project(self):
        """ Get the project (building) of the assembly.
        
        Returns
        -------
        ~pod_lca.building.Building
            Building project to which the assembly belong.
        """
        return self.get_building()
    
    def get_eol_material(self):
        """ Get the end-of-life product corresponding to the material.

        Returns
        -------
        str
            End-of-life product name corresponding to the material.      
        """
        return self.eol_product  

    def get_waste_rate(self):
        """ Get the waste rate of the material.
        
        Returns
        -------
        float
            Waste rate of the material during construction of the assembly/building.
        """
        return self.waste_rate
    
    def get_service_life(self):
        """ Set the service life of the material.
        
        Returns
        -------
        float
            Service life of the material in years.
        """
        return self.service_life
        
    def get_waste_product(self):
        """ Set the end-of-life waste product of the material.

        Returns
        -------
        ~pod_lca.eol.Waste
            End-of-life waste object corresponding to the material.
        """
        return self.waste_obj
    
    def get_replacement_materials(self):
        """ Get replacement materials for the building based on the service life of its materials.

        Returns
        -------
        list of ~pod_lca.building.Material
            Replacement material object if the service life of the material is less than the building life span. 
            None if no replacement is needed.
        """
        replacements = []
        if self.replacement_product is None:
             return None
        else:
            replacements.append(self.replacement_product)
            if self.replacement_product.get_replacement_materials() is not None:
                replacements.extend(self.replacement_product.get_replacement_materials())

        return replacements

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
        return self.get_parent().get_building()
    
    def get_impact_database(self):
        """ Get the impact database giving the A1-A3 impacts of the building materials.

        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            Impact database object.
        """
        return self.get_building().get_material_impact_database()

    def get_eol_process_impact_database(self):
        """ Get the end-of-life process impact database giving the C2-C4 impacts of the building materials.

        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            End-of-life process impact database object.
        """
        return self.get_building().get_eol_process_impact_database()
    
    def get_eol_demolition_database(self):
        """ Get the end-of-life demolition impact database giving the C1 impacts of the building materials.

        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            End-of-life demolition impact database object.
        """
        return self.get_building().get_eol_demolition_database()

    def get_transportation_manager(self):
        """ Get the transportation manager corresponding to the product.
        
        Returns
        -------
        ~pod_lca.transportation.TransportationManager
            Transportation manager
        """
        return self.get_building().get_transportation_manager()
    
    # ================================
    # Inventory Records Methods
    # ================================
    def get_product_impacts(self):
        """ Get A1-A3 impacts of the material.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            A1-A3 impacts of the material.
        """
        return self.get_impacts()

    def get_product_emissions(self):
        """ Get A1-A3 emissions of the material.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions
            A1-A3 emissions of the material.
        """        
        return self.get_emissions()

    def get_transportation_impacts(self):
        """ Get A4 impacts of the material.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            A4-A5 impacts of the material.
        """
        impacts = Impacts.from_parent(self)
        for leg in self.transport_legs:
            impacts += leg.get_impacts()

        return impacts

    def get_transportation_emissions(self):
        """ Get A4-A5 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions
            A4-A5 emissions of the building.
        """
        emissions = Emissions.from_parent(self)
        for leg in self.transport_legs:
            emissions += leg.get_emissions()    
        
        return emissions

    def get_eol_impacts(self, lc_stage=None):
        """ Get C2-C4 impacts of the material.

        Parameters
        ----------
        lc_stage: {'C1', 'C2', 'C3', 'C4', None}
            Life cycle stage for which the impacts to be calculated. 
            If None, gives impacts for all the relevant life cycle stages. 
            Default is None.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            C2-C4 impacts of the building.
        """
        impacts = Impacts.from_parent(self)

        if lc_stage is None:
            for impact_lst in self.get_waste_product().get_impacts().values():
                if isinstance(impact_lst, Impacts):
                    impacts += impact_lst
                    continue
                for impact in impact_lst:
                    impacts += impact
        else:
            for impact in self.get_waste_product().get_impacts()[lc_stage]:
                impacts += impact      

        return impacts

    def get_eol_emissions(self, lc_stage=None):
        """ Get C2-C4 emissions of the building.
        
        Parameters
        ----------
        lc_stage: {'C1', 'C2', 'C3', 'C4', None}
            Life cycle stage for which the emissions to be calculated. 
            If None, gives emissions for all the relevant life cycle stages. 
            Default is None.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            C2-C4 emissions of the building.
        """        
        emissions = Emissions.from_parent(self)

        if lc_stage is None:
            for emission_lst in self.get_waste_product().get_emissions().values():
                if isinstance(emission_lst, Emissions):
                    emissions += emission_lst
                    continue
                for emission in emission_lst:
                    emissions += emission
        else:
            for emission in self.get_waste_product().get_emissions()[lc_stage]:
                emissions += emission  

        return emissions

    def get_construction_impacts(self):
        """ Get A5 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            A5 impacts of the building.
        """
        return (self.get_product_impacts() + self.get_transportation_impacts() + self.get_eol_impacts()) * self.get_waste_rate()

    def get_construction_emissions(self):
        """ Get A5 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions
            A4-A5 emissions of the building.
        """
        return (self.get_product_emissions() + self.get_transportation_emissions() + self.get_eol_emissions()) * self.get_waste_rate()
    
    def get_replacement_impacts(self):
        """ Get B6 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            B6 impacts of the building.
        """
        if self.get_replacement_materials() is None:
            return Impacts.from_parent(self)
        else:
            return self.get_replacement_materials().get_product_impacts()
            + self.get_replacement_materials().get_transportation_impacts() 
            + self.get_replacement_materials().get_eol_impacts()

    def get_replacement_emissions(self):
        """ Get B6 impacts of the building.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            B6 impacts of the building.
        """
        if self.get_replacement_materials() is None:
            return Impacts.from_parent(self)
        else:
            return self.get_replacement_materials().get_product_emissions()
            + self.get_replacement_materials().get_transportation_emissions() 
            + self.get_replacement_materials().get_eol_emissions()
                
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


class BuildingEnvelopeMaterial(Material):
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


class BuildingEnvelopeMaterialNoMass(Material):
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
    

class WindowMaterialGlazing(Material):

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

