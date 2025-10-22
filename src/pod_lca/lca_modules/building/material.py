
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

import gc

from ..eol.waste import Waste
from ..impacts import CarbonStorage
from ..impacts import Emissions
from ..impacts import Impacts
from ..impacts import UniformEmissionProfile
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
    def new_structural_material(cls, parent, name, qty, unit, material_database_entry, product_year):
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

        material.set_service_life()

        material.impacts = Impacts.from_parent(material)
        material.emissions = Emissions.from_parent(material)
        material.carbon_storage = CarbonStorage.from_parent(material)
        material.unit_impacts = Impacts.from_parent(material)
        material.unit_emissions = Emissions.from_parent(material)
        material.unit_carbon_storage = CarbonStorage.from_parent(material)

        # set properties from database
        material.set_impact_database_entry(material_database_entry)

        database = material.get_impact_database()
        data_entry = database.get_data_entry(material_database_entry)

        material.set_sctg_code(data_entry['sctg code'])
        if not unit.get_qty_measured() == 'mass':
            material.set_density(data_entry['Density'], UNITS_MAP[data_entry['Density unit']])  
        material.set_eol_material(data_entry['eol material'], 
                                  data_entry['bio-based'] if 'bio-based' in data_entry else None)
        material.set_waste_rate(waste_rate_category=data_entry['waste_rate_category'])

        material.set_production_year(product_year)

        # set allied processes
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

    def set_name(self, name):
        """ Set name of the product/process.
        
        Parameters
        ----------
        name : str
            Name of the product/process.
        """
        self.name = name + ' in ' + self.get_parent().get_name()

        return self
    
    def set_eol_material(self, eol_material, is_bio_based=None, is_composite=None):
        """ Set the end-of-life product corresponding to the material.

        Parameters
        ----------
        eol_material : str
            EOL product name.
        is_bio_based : bool
            Flag to identify if the material is bio-based.
        is_composite : bool
            Flag to identify if the material is a composite.    
        """
        self.eol_product = eol_material
        self.bio_based = is_bio_based if is_bio_based is not None else True
        self.composite = is_composite if is_composite is not None else True

        return self

    def set_waste_rate(self, waste_rate=None, waste_rate_category=None):
        """ Set the waste rate of the material.
        
        Parameters
        ----------
        waste_rate : float 
            Waste rate of material during construction. Value between 0 and 100.
        waste_rate_category : str
            Category from which to extract waste rate.   
        """
        if waste_rate is not None:
            self.waste_rate = waste_rate
        elif waste_rate_category is not None:
            building = self.get_building()
            building_standard = building.get_building_data_standard()

            match building_standard:
                case 'RICS':
                    data = DataImporter.csv_to_dict(config['file_paths']['building']['RICS_WASTE_RATE'], 'POD|LCA Key')
                case 'ASHRAE':
                    data = DataImporter.csv_to_dict(config['file_paths']['building']['ASHRAE_WASTE_RATE'], 'POD|LCA Key')

            if waste_rate_category in data:
                self.waste_rate = float(data[waste_rate_category]['waste_rate'])
            else:
                self.waste_rate = float(data['DEFAULT']['waste_rate'])
        else:
            raise ValueError('Waste rate input not recognized.')

        if self.waste_rate > 100 or self.waste_rate < 0:
            raise ValueError('Waste rate to be given as a value between 0 and 100.')

        return self

    def set_service_life(self, service_life=None):
        """ Set the service life of the material.
        
        Parameters
        ----------
        service_life : float
            Service life of the material in years.
        """
        if service_life is None:
            self.service_life = self.get_parent().get_service_life()
        else:
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
            Value between 0 and 100.
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

    def get_transportation_impacts(self, objs=False):
        """ Get A4 impacts of the material.

        Parameters
        ----------
        objs : bool
            If True, returns a list of Impacts objects for each transport leg. 
            If False, returns a single Impacts object summing all transport legs. Default is False.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts or list of ~pod_lca.impacts.Impacts
            A4-A5 impacts of the material. List of impacts if objs is True.
        """
        impacts = [] if objs else Impacts.from_parent(self)
        for leg in self.get_transportation():
            if objs:
                impacts.append(leg.get_impacts())
            else:
                impacts += leg.get_impacts()

        return impacts

    def get_transportation_emissions(self, objs=False):
        """ Get A4-A5 impacts of the building.

        Parameters
        ----------
        objs : bool
            If True, returns a list of Emissions objects for each transport leg. 
            If False, returns a single Emissions object summing all transport legs. Default is False.

        Returns
        -------
        ~pod_lca.impacts.Emissions or list of ~pod_lca.impacts.Emissions
            A4-A5 emissions of the building. List of emissions if objs is True.
        """
        emissions = [] if objs else Emissions.from_parent(self)
        for leg in self.get_transportation():
            if objs:
                emissions.append(leg.get_emissions())
            else:
                emissions += leg.get_emissions()    
        
        return emissions

    def get_eol_impacts(self, lc_stage=None, objs=False):
        """ Get C2-C4 impacts of the material.

        Parameters
        ----------
        lc_stage: {'C1', 'C2', 'C3', 'C4', None}
            Life cycle stage for which the impacts to be calculated. 
            If None, gives impacts for all the relevant life cycle stages. 
            Default is None.
        objs : bool
            If True, returns a list of Impacts objects for eol pathway, transportation, and demolition. 
            If False, returns a single Impacts object summing all eol pathways, transportations, and demolition. Default is False.

        Returns
        -------
        ~pod_lca.impacts.Impacts or list of ~pod_lca.impacts.Impacts
            C2-C4 impacts of the building. List of impacts if objs is True.
        """
        impacts = [] if objs else Impacts.from_parent(self)

        if lc_stage is None:
            for impact_lst in self.get_waste_product().get_impacts().values():
                if isinstance(impact_lst, Impacts):
                    if objs:
                        impacts.append(impact_lst)
                    else:
                        impacts += impact_lst
                else:
                    for impact in impact_lst:
                        if objs:
                            impacts.append(impact)
                        else:
                            impacts += impact
        else:
            impact_lst = self.get_waste_product().get_impacts()[lc_stage]
            if isinstance(impact_lst, Impacts):
                if objs:
                    impacts.append(impact_lst)
                else:
                    impacts += impact_lst
            else:
                for impact in impact_lst:
                    if objs:
                        impacts.append(impact)
                    else:
                        impacts += impact

        return impacts

    def get_eol_emissions(self, lc_stage=None, objs=False):
        """ Get C2-C4 emissions of the building.
        
        Parameters
        ----------
        lc_stage: {'C1', 'C2', 'C3', 'C4', None}
            Life cycle stage for which the emissions to be calculated. 
            If None, gives emissions for all the relevant life cycle stages. 
            Default is None.
        objs : bool
            If True, returns a list of Emissions objects for eol pathway, transportation, and demolition. 
            If False, returns a single Emissions object summing all eol pathways, transportations, and demolition. Default is False.

        Returns
        -------
        ~pod_lca.impacts.Emissions or list of ~pod_lca.impacts.Emissions
            C2-C4 emissions of the building. List of emissions if objs is True.
        """        
        emissions = [] if objs else Emissions.from_parent(self)

        if lc_stage is None:
            for emission_lst in self.get_waste_product().get_emissions().values():
                if isinstance(emission_lst, Emissions):
                    if objs:
                        emissions.append(emission_lst)
                    else:
                        emissions += emission_lst
                else:
                    for emission in emission_lst:
                        if objs:
                            emissions.append(emission)
                        else:
                            emissions += emission
        else:
            emission_lst = self.get_waste_product().get_emissions()[lc_stage]
            if isinstance(emission_lst, Emissions):
                if objs:
                    emissions.append(emission_lst)
                else:
                    emissions += emission_lst
            else:
                for emission in emission_lst:
                    if objs:
                        emissions.append(emission)
                    else:
                        emissions += emission  

        return emissions

    def get_construction_impacts(self):
        """ Get A5 impacts of the building.

        Returns
        -------
        ~pod_lca.impacts.Impacts
            A5 impacts of the building.
        """
        return (self.get_product_impacts() + self.get_transportation_impacts() + self.get_eol_impacts()) * (self.get_waste_rate()/100)

    def get_construction_emissions(self):
        """ Get A5 impacts of the building.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            A4-A5 emissions of the building.
        """
        emission = (self.get_product_emissions() + self.get_transportation_emissions() + self.get_eol_emissions()) * (self.get_waste_rate() / 100)

        pulse = UniformEmissionProfile.unit_pulse(at=self.get_building().get_built_year())
        emission.set_temporal_emission_profile(pulse)

        return emission
    
    def get_replacement_impacts(self, objs=False):
        """ Get B6 impacts of the building.

        Parameters
        ----------
        objs : bool
            If True, returns a list of Impacts objects for product, transportation, and eol. 
            If False, returns a single Impacts object summing product, transportation, and eol. Default is False.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts or list of ~pod_lca.impacts.Impacts
            B6 impacts of the building. List of impacts if objs is True.
        """
        replacement_materals = self.get_replacement_materials()
        if replacement_materals is None:
            return Impacts.from_parent(self)
        else:
            impacts = [] if objs else Impacts.from_parent(self)
            for replacement in replacement_materals:
                if objs:
                    replacement_impact = [replacement.get_product_impacts(),
                                            *replacement.get_transportation_impacts(objs=True),
                                            *replacement.get_eol_impacts(objs=True),
                                            replacement.get_construction_impacts()]
                    impacts.extend(replacement_impact)
                else:
                            replacement_impact = (replacement.get_product_impacts() + 
                                                  replacement.get_transportation_impacts() + 
                                                  replacement.get_eol_impacts() + 
                                                  replacement.get_construction_impacts())
                            impacts += replacement_impact

            return impacts

    def get_replacement_emissions(self, objs=False):
        """ Get B6 impacts of the building.

        Parameters
        ----------
        objs : bool
            If True, returns a list of Emissions objects for product, transportation, and eol. 
            If False, returns a single Emissions object summing product, transportation, and eol. Default is False.

        Returns
        -------
        ~pod_lca.impacts.Emissions or list of ~pod_lca.impacts.Emissions
            B6 impacts of the building. List of impacts if objs is True.
        """
        replacement_materals = self.get_replacement_materials()
        if replacement_materals is None:
            return Emissions.from_parent(self)
        else:
            emissions = [] if objs else Emissions.from_parent(self)
            for replacement in replacement_materals:
                if objs:
                    replacement_emission = [replacement.get_product_emissions(),
                                            *replacement.get_transportation_emissions(objs=True),
                                            *replacement.get_eol_emissions(objs=True),
                                            replacement.get_construction_emissions()]
                    emissions.extend(replacement_emission)
                else:
                            replacement_emission = (replacement.get_product_emissions() + 
                                                    replacement.get_transportation_emissions() + 
                                                    replacement.get_eol_emissions() + 
                                                    replacement.get_construction_emissions())
                            emissions += replacement_emission
            return emissions

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


