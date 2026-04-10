
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..electricity import ElectricitySupply
from ..impacts import UniformEmissionProfile
from ..impacts import Impacts
from ..impacts import Emissions
from ...units import KILO
from ...units import WATT


class OperationalElectricityProduct:
    """ Operational electricity product to manage resulting impacts/emissions from operational energy usage.

    Attributes
    ----------
    name: str
        Name of the object
    building: ~pod_lca.building.Building
        Building in which operational electricity consumed.
    unit: ~pod_lca.units.Unit
        Unit of measurement of electricity consumption.
    electricity_supplier : ~pod_lca.electricity.ElectricitySupply
        Electricity supply.
    impacts: dict
        Dictionary of lists of :class:`~pod_lca.imppacts.Impacts` categorized.
    emissions: dict
        Dictionary of lists of :class:`~pod_lca.imppacts.Emissions` categorized.
    """


    def __init__(self):
        self.name = None
        self.building = None
        self.unit = None
        self.electricity_supplier = None
        self.impacts = None
        self.emissions = None

        self._inventories_uptodate = False
        
    # ================================
    # Constructors
    # ================================ 
    @classmethod
    def create(cls, building, unit=None):
        """ Create an operation electricity product
        
        Parameters
        ----------
        building: ~pod_lca.building.Building
            Building in which operational electricity consumed.
        unit: ~pod_lca.units.Unit
            Unit of measurement of electricity consumption.
        """
        item = cls()

        item.set_name('operational energy')
        item.set_building(building)
        item.set_unit(unit=KILO * WATT if unit is None else unit)
        item.impacts = {'heating': [], 'lighting': [], 'cooling': [], 'total': []}
        item.emissions = {'heating': [], 'lighting': [], 'cooling': [], 'total': []}

        electricity_supplier = ElectricitySupply.from_location(building.get_location(), building.get_built_year())
        item.set_supplier(electricity_supplier)

        return item

    # ================================
    # Setters
    # ================================    
    def set_name(self, name):
        """ Set name of the product/process.
        
        Parameters
        ----------
        name : str
            Name of the product/process.
        """
        self.name = name

        return self

    def set_building(self, building):
        """ Set the building of the assembly.
        
        Parameters
        ----------
        building : ~pod_lca.building.Building
            Building to which the assembly belong.
        """
        self.building = building

        return self
    
    def set_unit(self, unit):
        """ Set unit of measurement for the product/process.
        
        Parameters
        ----------
        unit : ~pod_lca.units.Unit
            Unit of measurement.

        Raises
        ------
        ValueError
            Incompatible units.
        """
        self.unit = unit

        return self

    def set_supplier(self, supplier):
        """ Set electricity supplier.
        
        Parameters
        ----------
        supplier : ~pod_lca.electricity.ElectricitySupply
            Electricity supply
        """
        self.electricity_supplier = supplier

        return self
    
    def set_decarbonization_scenario(self, scenario):
        """ Set scenario name. This will be used with cambium data.
    
        Parameters
        ----------
        scenario : {'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'}
            Electricity consmuption scenario considered.
        """
        self.electricity_supplier.set_decarbonization_scenario(scenario)

        self._inventories_uptodate = False

        return self
    
    # ================================
    # Getters
    # ================================ 
    def get_name(self):
        """ Retrieve the name of the product/process.

        Returns
        -------
        str
            Name of the product/process.
        """
        return self.name
        
    def get_unit(self):
        """ Retrieve the unit of measurement of the product/process.

        Returns
        -------
        ~pod_lca.units.Units
            Unit of measurement of the product/process.
        """
        return self.unit
    
    def get_building(self):
        """ Get the building of the assembly.
        
        Returns
        -------
        ~pod_lca.building.Building
            Building to which the assembly belong.
        """
        return self.building

    def get_decarbonization_scenario(self):
        """ Set scenario name. This will be used with cambium data.
    
        Returns
        -------
        str 
            Electricity consmuption scenario considered. {'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'}
        """
        return self.electricity_supplier.get_decarbonization_scenario()
    
    def get_impacts(self, category='total'):
        """ Get impacts by functional category.

        Parameters
        ----------
        category : {'heating', 'lighting', 'cooling', 'total'}
            Category of operational energy.

        Returns
        -------
        list of ~pod_lca.impacts.Impacts
            List of impact objects.
        """
        return self.impacts[category]

    def get_emissions(self, category='total'):
        """ Get emissions by functional category.

        Parameters
        ----------
        category : {'heating', 'lighting', 'cooling', 'total'}
            Category of operational energy.

        Returns
        -------
        list of ~pod_lca.impacts.Emissions
            List of impact objects.
        """
        return self.emissions[category]
        
    # ================================
    # Methods
    # ================================
    def update_inventory_records(self):
        """ Set the impacts and emissions of the operational energy consmuption.
        """
        building = self.get_building()

        method = building.operational_energy_method
        if method == 'eplus':
            building.write_idf()
            building.run_operational_energy_model(delete=True)
            building.get_operational_energy_object().set_dirty(False)

        annual_electricity_usage = building.get_operational_electricity_usasge(method,
                                                                               summed_at='year', 
                                                                               group_by_category=True,
                                                                               group_by_zone=False,
                                                                               unit=self.get_unit())

        elec_supp = self.electricity_supplier
        electricity_declared_unit = elec_supp.get_declared_unit()
        conversion_factor = electricity_declared_unit.convert_to(self.get_unit())

        imp_h, imp_l, imp_c, imp_t = self.impacts['heating'], self.impacts['lighting'], self.impacts['cooling'], self.impacts['total']
        em_h, em_l, em_c, em_t = self.emissions['heating'], self.emissions['lighting'], self.emissions['cooling'], self.emissions['total']

        usage = annual_electricity_usage['year']
        h_usage = usage['heating'] * conversion_factor
        l_usage = usage['lighting'] * conversion_factor
        c_usage = usage['cooling'] * conversion_factor

        start_year = building.get_built_year()
        end_year = start_year + building.get_life_span() + 1
        electricity_impacts, electricity_emissions = elec_supp.get_inventories_in_bulk_for_years(list(range(start_year, end_year)))
        for year in range(start_year, end_year):

            unit_impacts = Impacts.from_dict(electricity_impacts.loc[year].to_dict())
            unit_emissions = Emissions.from_dict(electricity_emissions.loc[year].to_dict())

            # set impacts
            heating_impacts = unit_impacts * h_usage
            lighting_impacts = unit_impacts * l_usage
            cooling_impacts = unit_impacts * c_usage

            total_impacts = heating_impacts + lighting_impacts + cooling_impacts

            imp_h.append(heating_impacts)
            imp_l.append(lighting_impacts)
            imp_c.append(cooling_impacts)
            imp_t.append(total_impacts)    

            # set emissions
            heating_emissions = unit_emissions * h_usage
            lighting_emissions = unit_emissions * l_usage
            cooling_emissions = unit_emissions * c_usage

            total_emissions = heating_emissions + lighting_emissions + cooling_emissions

            em_h.append(heating_emissions)
            em_l.append(lighting_emissions)
            em_c.append(cooling_emissions)
            em_t.append(total_emissions)

            pulse = UniformEmissionProfile.unit_pulse(at=year)
            heating_emissions.set_temporal_emission_profile(pulse)
            lighting_emissions.set_temporal_emission_profile(pulse)
            cooling_emissions.set_temporal_emission_profile(pulse)
            total_emissions.set_temporal_emission_profile(pulse)

        self._inventories_uptodate = True

        return self

if __name__ == '__main__':
    pass