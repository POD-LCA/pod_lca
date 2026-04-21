
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import ConstructionMixins
from . import DataMixins
from . import EndOfLifeMixins
from . import EnvelopeMixins
from . import OperationalMixins
from . import ProductScopeMixins
from . import Scenario
from . import TemplateModels
from . import TransportationMixins
from . import UseMixins
from ..dynamic_radiative_forcing import DynamicRadiativeForcingRecord
from ...units import MEGA
from ...units import WATT_HOUR


class Building (TemplateModels, DataMixins, EndOfLifeMixins, OperationalMixins, UseMixins, ConstructionMixins, TransportationMixins, ProductScopeMixins, EnvelopeMixins):
    """ Building object to keep track of the building materials flow (i.e., embodied energy assembly).

    Attributes
    ----------
    name : str
        Name of the building.
    structure_type : {'Concrete', 'Steel', 'CLT'}
        Major vertical gravity system of the structure.
    built_year: int
        Built year of the building.
    life_span : int
        Useful life of the building.
    location : ~pod_lca.location.Location
        Location of the building site.
    structure : ~pod_lca.building_structure.BuildingStructure
        Structural assemblies of the building.
    building_envelope : ~pod_lca.building_envelope.BuildingEnvelope
        Envelope assemblies of the building
    operational_object : ~pod_lca.operational.OperationalEnergyObject
        Operational energy object to handle operational energy simulations
    assemblies : list of ~pod_lca.building.Assembly 
        Structural and Fascade elements that make up the building.
    material_impact_database: ~pod_lca.impacts.ImpactsDatabase
        Buildin material impact database.
    transport_impact_database : ~pod_lca.impacts.TranportationModeImpactsDatabase
        Impact database of transportation modes.
    eol_impact_database : ImpactsDatabase Obj.
        Impacts related to end of life processes.
    eol_transport_dataset: ~pod_lca.transportation.TransportDataset
        End-of-life transportation dataset.
    transportation_manager: ~pod_lca.transportation.TransportationManager
        Manager of inward transportation of material for the construction of the building.
    building_data_standard: {'RICS', 'ASHRAE'}
        building strnadard used for 
    construction_energy_product : ~pod_lca.electricity.Electricity
        Electricity consumption during the building construction.
    operational_electricity_product : ~pod_lca.building.OperationalElectricityProduct
        Electricity consumption during the building operations.
    operational_energy_method : {'eplus', 'EUIs'}
        method fro computing operational energy.
    weather_file_path : str
        File path to the weather file to be used in operational energy simulations.
    idf_file_path : str
        File path to save the intemediary idf file from Python library to Eplus.
    eplus_folder_path: str
        Folder path to Eplus executable file.
    eplus_out_folder : str
        Folder path to save the raw Eplus results.
    energy_plus_results : dict
        Energy plus results output from the operational energy simulations.
    energy_plus_units : dict
        Units of the energy plus results.
    """     

    def __init__(self):
        self.name = None
        self.structure_type = None
        self.built_year = None
        self.life_span = None
        self.location = None

        self.floors = {} # FIXME: used in operational and plotters...

        self.structure = None
        self.building_envelope = None
        self.operational_object = None
        self.assemblies = []

        self.material_impact_database = None
        self.transport_impact_database = None
        self.eol_impact_database = None
        self.eol_transport_dataset = None
        self.transportation_manager = None
        self.building_data_standard = None

        self.construction_energy_product = None
        self.operational_electricity_product = None

        self.operational_energy_method = 'eplus'
        self.weather_file_path = None
        self.idf_file_path = None
        self.eplus_folder_path = None
        self.eplus_out_folder = None
        self.energy_plus_results = None
        self.energy_plus_units = None

        self.scenarios = {}

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, name, location, built_year, life_span):
        """ Build a building.
        
        Parameters
        ----------
        name : str
            Name of the building.
        type : {'Commercial', 'Residential'}
            Type of building.
        location : ~pod_lca.location.Location
            Location of the building site.
        built_year: int
            Built year of the building.
        life_span: int
            Life span of the building in years.

        Returns
        -------
        ~pod_lca.buildings.Building
            Building built.
        """    
        building = cls()

        building.set_name(name)
        building.set_location(location)
        building.set_built_year(built_year)
        building.set_life_span(life_span)

        return building
    
    @classmethod
    def from_assemblies(cls, name, location, built_year, life_span, structure, building_envelope, **kwargs):
        """ Build a building.
        
        Parameters
        ----------
        name : str
            Name of the building.
        location : ~pod_lca.location.Location
            Location of the building site.
        built_year: int
            Built year of the building.
        life_span: int
            Life span of the building in years.
        structure : ~pod_lca.building_structure.BuildingStructure
            Structure of the building.
        building_envelope : ~pod_lca.building_envelope.BuildingEnvelope
            Envelope of the building.

        Other Parameters
        ----------------
        logistic_type : {'local', 'global'}
            Transportation scope of the building material in construction.
        construction_energy_use: float
            Construction energy use for the building.
        construction_energy_use_unit: str
            Unit for construction energy use. E.g., 'MWh', 'kWh', etc


        Returns
        -------
        ~pod_lca.buildings.Building
            Building built.
        """    
        building = cls.new(name, location, built_year, life_span)
        building.set_databases(kwargs.get('building_standard', 'ASHRAE'))
        building.set_building_level_products(logistic_type=kwargs.get('logistic_type', 'local'),
                                             construction_electricity_consumption=kwargs.get('construction_energy_use', 0.0),
                                             electricity_unit=kwargs.get('construction_energy_use_unit', MEGA * WATT_HOUR))
        
        building.set_structure(structure)
        building.set_building_envelope(building_envelope)

        return building
     
    # ================================
    # Setters
    # ================================     
    def set_name(self, name):
        """ Set name of the building.
        
        Parameters
        ----------
        name : str
            Name of the building.
        """
        self.name =  name

        return self

    def set_structure_type(self, structure_type):
        """ Set the major vertical gravity system of the structure
        
        Parameters
        ----------
        structure_type : {'Concrete', 'Steel', 'CLT'}
            Major vertical gravity system of the structure.
        """
        self.structure_type = structure_type

        return self
        
    def set_built_year(self, year):
        """ Set built year of the building.
        
        Parameters
        ----------
        year: int
            Built year of the building.
        """
        self.built_year = year

        return self
    
    def set_life_span(self, life_span):
        """ Set life span of the building.
        
        Parameters
        ----------
        life_span: int
            Life span of the building in years.
        """
        self.life_span = life_span

        return self

    def set_location(self, location):
        """ Set location of the building site.
        
        Parameters
        ----------
        location : Location Obj.
            Location of the building site.
        """
        self.location = location

        return self
    
    def set_building_data_standard(self, standard):
        """ Set standard used for service lives and waste rates.
        
        Parameters
        ----------
        standard: {'RICS', 'ASHRAE'}
            building strnadard used for 
        """
        self.building_data_standard = standard
    
    def set_scenario(self, name):
        """ Create new scenario for the building.
        
        Parameters
        ----------
        name : str
            Name of the building scenario.
        """
        scenario = Scenario.new(self)

        self.scenarios[name] = scenario

        return scenario

    def set_databases(self, building_standard):
        """ Set databases and datasets to be used in the LCA computations.

        Parameters
        ----------
        building_standard: {'RICS', 'ASHRAE'}
            Standard used for service lives and waste rates.
        """
        self.set_material_database()
        self.set_transportation_mode_impact_database()
        self.set_eol_process_impact_database()
        self.set_eol_demolition_impact_database()
        self.set_eol_transport_dataset()
        self.set_building_data_standard(building_standard)

        return self
    
    def set_building_level_products(self, logistic_type, construction_electricity_consumption, electricity_unit):
        """ Set building level products used for LCA calculations.
        
        Parameters
        ----------
        logistic_type : {'domestic', 'global'}
            Type of logistic management used for A4 transportation.
        construction_electricity_consumption : float
            Amount of electricity consumed in construction activities.
        electricity_unit : ~pod_lca.units.Unit
            Unit of measurement used for electricity consumption.
        """
        self.set_transportation_manager(logistic_type)
        self.set_operational_electricity_product(electricity_unit)
        self.set_construction_energy_product(construction_electricity_consumption, electricity_unit)

        return self
    
    def set_structure(self, structure):
        """ Set the building structure object.
        
        Parameters
        ----------
        structure : ~pod_lca.building_structure.BuildingStructure
            Structural assemblies of the building.
        """
        self.structure = structure
        structure.set_building(self)

    def set_building_envelope(self, building_envelope):
        """ Set the building envelope object.
        
        Parameters
        ----------
        building_envelope : ~pod_lca.building_envelope.BuildingEnvelope
            Envelope assemblies of the building
        """
        self.building_envelope = building_envelope
        building_envelope.set_building(self)

    def set_operational_energy_object(self, operational_energy_object):
        """ Set the operational energy object used in energy plus simulations.
        
        Parameters
        ----------
        operational_object : ~pod_lca.operational.OperationalEnergyObject
            Operational energy object to handle operational energy simulations
        """
        self.operational_object = operational_energy_object
        operational_energy_object.set_building(self)

    # ================================
    # Getters
    # ================================
    def get_name(self):
        """ Get name of the building.
        
        Returns
        -------
        str
            Name of the building.
        """
        return self.name

    def get_structure_type(self):
        """ Get the major vertical gravity system of the structure
        
        Returns
        -------
        str
            Major vertical gravity system of the structure.
        """
        return self.structure_type
    
    def get_location(self):
        """ Get location of the building site.
        
        Returns
        -------
        ~pod_lca.location.Location
            Location of the building site.
        """
        return self.location
    
    def get_built_year(self):
        """ Get built year of the building.
        
        Returns
        -------
        int
            Built year of the building.

        """
        return self.built_year

    def get_life_span(self):
        """ Get life span of the building.
        
        Returns
        -------
        int
            Life span of the building in years.
        """
        return self.life_span

    def get_building_data_standard(self):
        """ Get standard used for service lives and waste rates.
        
        Returns
        -------
        str
            building strnadard used for 
        """
        return self.building_data_standard

    def get_structure(self):
        """ Get the building structure object.
        
        Returns
        -------
        ~pod_lca.building_structure.BuildingStructure
            Structural assemblies of the building.
        """
        return self.structure
    
    def get_envelope(self):
        """ Get the building envelope object.
        
        Returns
        -------
        ~pod_lca.building_envelope.BuildingEnvelope
            Envelope assemblies of the building
        """
        return self.envelope

    def get_operational_energy_object(self):
        """ Get the operational energy object used in energy plus simulations.
        
        Returns
        -------
        ~pod_lca.operational.OperationalEnergyObject
            Operational energy object to handle operational energy simulations
        """
        return self.operational_object
    
    def get_assemblies(self):
        """ Get a list of building assemblies.

        Returns
        -------
        list of ~pod_lca.building.Assembly
            Structural and Fascade elements that make up the building.
        """
        return self.assemblies

    def get_scenario(self, name):
        """ Retrieve a building scenario.
        
        Parameters
        ----------
        name : str
            Name of the building scenario.
        """
        return self.scenarios[name]
    
    # ================================
    # Assembly Methods
    # ================================ 
    def add_assembly(self, assembly):
        """ Add a assembly to the building.
        
        Parameters
        ----------
        assembly : ~pod_lca.building.Assembly
            Structural or envelope element to be added to the building.
        """
        self.get_assemblies().append(assembly)

        return self
    
    def remove_assembly(self, assembly):
        """ Remove assembly from a building.

        Parameters
        ----------
        assembly : ~pod_lca.building.Assembly
            Structural or envelope element to be removed from the building."""
        self.get_assemblies().remove(assembly)

    # ================================
    # LCA Methods
    # ================================ 
    def get_impacts(self, scope='all', lc_stage=None):
        """ Get impacts.
         
        Parameters
        ----------
        scope : {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}
            Scope of impacts
            - 'all': from A-C
            - 'product': from A1-A3
            - 'transportation': A4
            - 'construction': A5
            - 'use': from B1-B7
            - 'end of life': C1-C4
        lc_stage: {'C1', 'C2', 'C3', 'C4', None}
            Life cycle stage for which the impacts to be calculated. 
            If None, gives impacts for all the relevant life cycle stages. 
            Default is None.

        Returns
        -------
        ~pod_lca.impacts.Impact
            LCA Impacts.
        """
        # TODO: use cache with each part to avoid redoing calculations ---  same for emissions
        if scope == 'all':
            return (self.get_product_impacts() + self.get_transportation_impacts()
                    + self.get_construction_impacts() + self.get_replacement_impacts()
                    + self.get_operational_impacts() + self.get_eol_impacts(lc_stage))
        elif scope == 'product':
            return self.get_product_impacts()
        elif scope == 'transportation':
            return self.get_transportation_impacts()
        elif scope == 'construction':
            return self.get_construction_impacts()
        elif scope == 'replacement':
            return self.get_replacement_impacts()
        elif scope == 'operational energy':
            return self.get_operational_impacts()
        elif scope in ['end of life', 'end-of-life']:
            return self.get_eol_impacts(lc_stage)
        else:
            raise ValueError('LCA scope not recognized')

    def get_emissions(self, scope='all', lc_stage=None):
        """ Get emissions.
         
        Parameters
        ----------
        scope : {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}
            Scope of impacts
            - 'all': from A-C
            - 'product': from A1-A3
            - 'transportation: A4
            - 'construction': A5
            - 'use': from B1-B7
            - 'end of life': C1-C4
        lc_stage: {'C1', 'C2', 'C3', 'C4', None}
            Life cycle stage for which the impacts to be calculated. 
            If None, gives impacts for all the relevant life cycle stages. 
            Default is None.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            LCA emissions.
        """
        if scope == 'all':
            return (self.get_product_emissions() + self.get_transportation_emissions()
                    + self.get_construction_emissions() + self.get_replacement_emissions()
                    + self.get_operational_emissions() + self.get_eol_emissions(lc_stage))
        elif scope == 'product':
            return self.get_product_emissions()
        elif scope == 'transportation':
            return self.get_transportation_emissions()
        elif scope == 'construction':
            return self.get_construction_emissions()
        elif scope == 'replacement':
            return self.get_replacement_emissions()
        elif scope == 'operational energy':
            return self.get_operational_emissions()
        elif scope == 'end of life':
            return self.get_eol_emissions(lc_stage)
        else:
            raise ValueError('LCA scope not recognized')

    def get_drf_record(self, time_horizon=100, time_step=1/12):
        """ Get the dynamic radiative forcing record for all the products and procesess in the model.
        
        Parameters
        ----------
        time_horizon : int
            Time horizon in years.
        time_step : int or float
            Time step of the record. The same time step is used for both for integration and for reporting.

        Returns
        -------
        ~pod_lca.drf.DynamicRadiativeForcingRecord
            Dynamic Radiative Forcing Record
        """
        all_emissions = self.get_product_emissions(objs=True) + \
                        self.get_transportation_emissions(objs=True) + \
                        [self.get_construction_emissions()] + \
                        self.get_eol_emissions(lc_stage=None, objs=True) + \
                        self.get_replacement_emissions(objs=True) + \
                        self.get_operational_emissions(objs=True) 
                        
        return DynamicRadiativeForcingRecord.from_emissions(all_emissions, 
                                                           self.get_built_year(), 
                                                           time_horizon, 
                                                           time_step)


if __name__ == '__main__':
    pass
