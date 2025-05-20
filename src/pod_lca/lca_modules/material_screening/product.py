
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Master
from ..electricity import ElectricitySupply
from ..impacts import CarbonStorage
from ..impacts import Emissions
from ..impacts import Impacts
from ..uncertainty import DataDistribution
from ...units import UNITS_MAP
from ...utilities import config


class Product(Master):
    """ Product object, inheriting from the Master object, represent a product.

    Attributes
    ----------
    production_year : int
        The year the product was produced.
    electricity : dict
        Dictionary containing A3 electricity impacts of the production of the material. 
        'from_database' contains electricity impacts from database, 'by_location' contains corresponding electricity impacts by location data. 
        '_current' indicates which of the above is in use for impacts.
    weight : float
        Mass of the product.
    weight_unit : str
        Unit of measurement of mass. Default is set as 'kg'.
    density : float
        The mass of product in weight units per unit of product's unit of measurement.
    trnasporter : TransportationProcess Obj.
        Transportation process, if the product is being transported, else None.
    is_material : bool
        True, if the product is a material.
    is_fuel : bool
        True, of the product is an energy source.
    """

    def __init__(self):
        super().__init__()
        self.production_year = None
        self.electricity = {'from_database': None, 'by_location': None, '_current': None, '_tag':None}
        self.weight = 0.0
        self.weight_unit = None
        self.density = 1.0 # the weight of 1 unit of prodcut
        self.transporter = None
        self.is_material = True

    def __str__(self):
        return f"Product(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"
    
    # ================================
    # Setters
    # ================================
    def set_qty(self, qty):
        """ Update the qty of the product.
            This will also re-calculate the corresponding impact quantities.
            
        Parameters
        ----------
        qty : float
            Product quantity.
        """
        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError("Quantity should be a numeric entry.")
            
        self.qty = qty
        self.weight = self.qty * self.density

        if self.get_transporter() is not None:
            transporter = self.get_transporter()
            transporter.set_transported_weight()

        self.update_inventory_records()

        return self

    def set_unit(self, unit):
        """ Set unit of measurement for the product.
            If the unit of measurement is of mass dimensions, same unit is set as weight unit of the product.
        
        Parameters
        ----------
        unit : Unit Obj.
            Unit of measurement.
        """
        self.unit = unit
        if unit.get_qty_measured() == 'mass':
            self.set_weight_unit(unit)
            self.density = 1.0

        return self

    def set_production_year(self, year):
        """ Set the year of production for the item.
        
        Parameters
        ----------
        year : int
            Year of production.
        """
        self.production_year = year

        if not self.electricity['by_location'] is None:
            self.electricity['by_location'].set_year(year)

        return self
    
    def set_weight_unit(self, unit):
        """ Set unit of measurement for the mass of the product.

        Parameters
        ----------
        str
            Unit of measurement of mass.
        """
        self.weight_unit = unit

        return self

    def set_density(self, density):
        """ Set density of the product.
            Density is defined here as mass per unit measurement of product (not necessarily volume)
    
        Parameters
        ----------
        density : float
            Denisty of product (mass per unit mesurement of product).

        Raises
        ------
        TypeError
            Density must be a numerical value.
        """
        if isinstance(density, str):
            try:
                density = float(density)
            except:
                raise TypeError(f"Density of {self.get_name()} should be a numerical value.")
    
        self.density = density

        return self

    def set_transporter(self, transporter):
        """ Set transport processes the product is subject to.
            If not already added, will add the product to the transportation process as a transported product.
            
        Note
        ----
        This method is equivalent to calling 'set_transported_product' from the TransportationProcess Obj.

        Parameters
        ----------
        TransportationProcess Obj.
            Transportation process the product is subject to.
        """
        self.transporter = transporter
        if self not in transporter.get_transported_products():
            transporter.set_transported_product(self)

        return self
       
    def set_electricity_source(self, source='from_database'):
        """ Set the source of electricity inventories.
        
        Parameters
        ----------
        source : str
            Source of electricity inventories data.
        """
        if source in [key for key in self.electricity if not key.startswith('_')]:
            current_source = self.get_electricity_source()
            self.electricity["_current"] = source

            if current_source is not None:
                product_impact = self.get_impacts()

                product_impact -= self.electricity[current_source].get_impacts()
                product_impact += self.electricity[source].get_impacts()

                return self
        else:
            raise KeyError(f"Source of electricty ({source} not recognized.)")

 
    def set_electricity_database_tag(self):
        """ Find the tag used to identify electricity data in the database.
        """
        if self.get_impact_database_entry() is not None:
            database = self.get_project().get_database()
            data_set = database.get_data_entry(self.get_impact_database_entry())
            
            electricity_tag = None
            for key in ['Electricity_', 'electricity_', 'elec_', 'Elec_']:
                if key + database.get_qty_key() in data_set:
                    electricity_tag = key
                    self.electricity['_tag'] = electricity_tag
                    break
        
        return self
    
    # ================================
    # Getters
    # ================================      
    def get_production_year(self):
        """ Get the year of production for the item.
        
        Returns
        -------
        year : int
            Year of production.
        """
        return self.production_yea

    def get_electricity(self):
        """ Get the electricity product of the item.
        
        Returns
        -------
        Electricity Obj.
            Electricity used in the production of the item.
        """
        return self.electricity[self.get_electricity_source()]
    
    def get_electricity_source(self):
        """ Get the source of electricity inventories.
        
        Returns
        -------
        str
            Source of electricity inventories data.
        """
        return self.electricity["_current"]

    def get_electricity_database_tag(self):
        """ Find the tag used to identify electricity data in the database.

        Returns
        -------
        str
            Tag used to identify electricity data in the database.
        """
        return self.electricity['_tag']
    
    def get_electricity_qty(self):
        """ Get electricity quantity used for the production of product quantity.
        
        Returns
        -------
        float
            Quantity of the electricity
        """
        
        database = self.get_project().get_database()
        data_set = database.get_data_entry(self.get_impact_database_entry())

        qty = data_set[self.get_electricity_database_tag() + database.get_qty_key()]

        declared_unit = database.get_data_entry(self.get_impact_database_entry())[database.get_unit_key()]
        declared_qty = database.get_data_entry(self.get_impact_database_entry())[database.get_qty_key()]
        conversion_factor = self.get_unit().get_conversion_factor(declared_unit)

        return qty * (self.get_qty()/ (declared_qty * conversion_factor))
    
    def get_weight(self):
        """ Retrieve the mass of the product.
        
        Returns
        -------
        str
            Mass of the product.
        """
        return self.weight

    def get_weight_unit(self):
        """ Retrieve the unit of measurement of mass of the product.
            This is used for the definition of density of the product.

        Returns
        -------
        str
            Unit of measurement of mass of the product.
        """
        return self.weight_unit
    
    def get_density(self):
        """ Retrieve density of the product.
            Density is defined here as mass per unit measurement of product (not necessarily volume)
        
        Returns
        -------
        float
            Denisty of product (mass per unit mesurement of product).
        """
        return self.density 
       
    def get_transporter(self):
        """ Retrieve transport processes the product is subject to, if any.

        Returns
        -------
        TransportationProcess Obj.
            Transportation process the product is subject to, if any.
            None, otherwise.
        """
        return self.transporter

    # ================================
    # Methods
    # ================================
    def update_inventory_records(self):
        """ Sets inventory quantities, based on database item asigned to the product/process 
            and the product/process quantity.
            If no database entry is asigned, impacts are not updated.

        Raises
        ------
        ImportError : Incompatible units of Master object and database entry.
        """
        super().update_inventory_records()
        self.update_electricity_records()

        return self

    def update_electricity_records(self):
        """ Set electricity objects from database and location. This is done only if the database seperates electricity data (i.e., quantity, unit, and inventories).
            The electricity data in the database should be prefixed with one of 'Electricity_', 'electricity_', 'elec_', or 'Elec_'.
        """
        if self.get_impact_database_entry() is not None:
            self.set_electricity_database_tag()
            
            database = self.get_project().get_database()
            data_set = database.get_data_entry(self.get_impact_database_entry())

            electricity_tag = self.get_electricity_database_tag()

            if electricity_tag is not None:
                # electricity quantity
                electricity_qty = self.get_electricity_qty()
                electricity_unit = UNITS_MAP[data_set[electricity_tag + database.get_unit_key()]]
                
                # electricity by location
                if self.electricity['by_location'] is None:
                    electricity_by_location = Electricity.new(id=None, 
                                                            name=self.get_name() + '_electricity', 
                                                            model=self.get_model(), 
                                                            stage=None, 
                                                            qty=electricity_qty, 
                                                            unit=electricity_unit)
                    self.electricity['by_location'] = electricity_by_location
                else:
                    self.electricity['by_location'].set_qty(electricity_qty)
                    self.electricity['by_location'].set_unit(electricity_unit)
                
                # electricity from database
                for data_type, DATA_HEADERS_DICT in database.__class__.DATA_IMPORTS.items():
                    record_dict = {}
                    for cat in DATA_HEADERS_DICT:
                        if electricity_tag + '_' + cat in data_set:
                            record_dict[cat] = data_set[electricity_tag + '_' + cat]

                    if data_type == 'impacts':
                        impacts = Impacts.from_dict(record_dict)
                    elif data_type == 'emissions':
                        emissons = Emissions.from_dict(record_dict)
                    elif data_type == 'carbon_storage':
                        carbon_storage = CarbonStorage.from_dict(record_dict)
                    else: 
                        raise KeyError(f"Record type {data_type} not recognized.")

                electiricity_from_data = Electricity.from_inventories(name=self.get_name() + '_electricity', 
                                                                    qty=electricity_qty, 
                                                                    unit=electricity_unit, 
                                                                    impacts=impacts,
                                                                    emissions=emissons,
                                                                    carbon_storage=carbon_storage)
                self.electricity['from_database'] = electiricity_from_data

            if self.get_electricity_source() is None:
                self.electricity["_current"] = 'from_database'
            elif self.get_electricity_source() == 'by_location':
                product_impact = self.get_impacts()
                product_impact -= self.electricity['from_database'].get_impacts()
                product_impact += self.electricity['by_location'].get_impacts()
        
        return self


class Fuel(Product):
    """ Fuel product object, inheriting from the product object.

    Attributes
    ----------
    is_material : bool
        True
    is_energy : bool
        True
    """

    def __init__(self):
        super().__init__()
        self.is_material = True
        self.is_energy = True

    def __str__(self):
        return f"Fuel(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"

class Electricity(Fuel):
    """ Electricity product object, inheriting from the Fuel object.

    Attributes
    ----------
    electricity_supplier: ElectricitySupply Obj
        Electricity supplier
    year : int
        Year of electricity consumption
    spatial_resolution: str
        Spatial resolution considered for electricity data: 'National'. 'Regional', 'Local'
    scenario: str
        Cambium scenario for prediction of electricity technology futures.
    """

    def __init__(self):
        super().__init__()
        self.electricity_supplier = None
        self.year = None
        self.spatial_resolution = None
        self.scenario = None

    @classmethod
    def new(cls, id, name, model, stage, qty, unit):
        item = cls()

        item.set_id(id)
        item.set_name(name)
        item.set_model(model)
        item.set_life_cycle_stage(stage)
        item.set_qty(qty)
        item.set_unit(unit)
        item.set_weight_unit(unit)
        item.impacts = Impacts.from_parent(item)
        item.emissions = Emissions.from_parent(item)
        item.carbon_stroage = CarbonStorage.from_parent(item)

        electricity_supplier = ElectricitySupply.from_location(model.get_project().get_location())
        item.set_supplier(electricity_supplier)

        return item
    
    @classmethod
    def from_inventories(cls, name, qty, unit, impacts, emissions, carbon_storage):
        """ Create an electricity impact from given impacts. This is primarily for seperating electricity component of products.
        
        Parameters
        ----------
        name : str
            Name of the electricity.
        qty : float
            Quantity of elctricity consumption.
        unit : Unit Obj.
            Unit of electricity consumption.
        impacts : Impacts Obj.
            Impacts corresponding to electricity consumption.
        emissions : Emissions Obj.
            Emissions corresponding to electricity consumption.
        carbon_storage : CarbonStorage Obj.
            Carbon storage corresponding to electricity consumption.
        """
        item = cls()

        item.set_name(name)
        item.set_qty(qty)
        item.set_unit(unit)
        item.set_weight_unit(unit)
        item.impacts = impacts
        item.emissions = emissions
        item.carbon_stroage = carbon_storage

        return item
    
    def update_inventory_records(self):
        """ Sets impacts quantities, based on database item asigned to the product/process 
            and the product/process quantity.
            If no database entry is asigned, impacts are not updated.

        Raises
        ------
        ImportError : Incompatible units of Master object and database entry.
        """
        if not self.get_supplier() is None:
            supplier = self.get_supplier()
            
            declared_unit = supplier.get_unit()
            unit_impacts = supplier.get_impacts()
            unit_emissions = supplier.get_emissions()

            conversion_factor = declared_unit.get_conversion_factor(self.get_unit())

            impacts = {category: (unit_impacts.get_record(category) / conversion_factor) * self.qty for category in config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']}
            self.get_impacts().update_qty(impacts)

            emissions = {category: (unit_emissions.get_record(category) / conversion_factor) * self.qty for category in config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES']}
            self.get_emissions().update_qty(emissions)
                 
    def set_supplier(self, supplier):
        """ Set electricity supplier.
        
        Parameters
        ----------
        supplier : ElectricitySupply Obj.
            Electricity supply
        """
        self.electricity_supplier = supplier
        self.update_inventory_records()

        return self

    def set_year(self, year):
        """ Set the year of electricity consumption.
        
        Parameters
        ----------
        year : int
            Year of electricity consumption.
        """
        self.year = year

        if self.get_supplier() is not None:
            self.get_supplier().set_year(year)
            self.update_inventory_records()

        return self
    
    def set_spatial_resolution(self, spatial_resolution):
        """ Set the spatial resolution of the electricity supply.
        
        Parameters
        ----------
        spatial_resolution : str
            Spatial resolution of the electricity supply: 'National', 'Regional', 'Local'.
        """
        self.spatial_resolution = spatial_resolution

        if self.get_supplier() is not None:
            self.get_supplier().set_spatial_resolution(spatial_resolution)
            self.update_inventory_records()

        return self
    
    def set_scenario(self, scenario):
        """ Set scenario name. This will be used with cambium data.
        
        Parameters
        ----------
        scenario : str
            Electricity consmuption scenario considered: e.g., 'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'.
        """
        self.scenario = scenario

        if self.get_supplier() is not None:
            if scenario in ['MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035']:
                self.get_supplier().set_scenario(scenario)
                self.update_inventory_records()
                
            else:
                raise ValueError(f"Scenario {scenario} is not a valid scenario. Valid scenarios are: 'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'.")

        return self
    
    def get_supplier(self):
        """ Get the electricity supplier.
        
        Returns
        -------
        ElectricitySupply Obj.
            Electricity supplier.
        """
        return self.electricity_supplier
    
    def get_year(self):
        """ Get the year of electricity consumption.
        
        Returns
        -------
        int
            Year of electricity consumption.
        """
        return self.year
    
    def get_spatial_resolution(self):
        """ Get the spatial resolution of the electricity supply.
    
        Parameters
        ----------
        str
            Spatial resolution of the electricity supply: 'National', 'Regional', 'Local'.
        """
        return self.spatial_resolution

    def get_scenario(self):
        """ Get scenario name. This will what used with cambium data.
        
        Parameters
        ----------
        str
            Electricity consmuption scenario considered: e.g., 'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'.
        """
        return self.scenario

    def get_data_distribution(self, attr):
        """ Get data_distribution object corresponding to the given attribute.

        Parameters
        ----------
        attr : str.
            Attribute to which the distribution correspond.

        Returns
        -------
        DataDistribution Obj.
            Data distribution.        
        """ 
        if self.get_supplier() is not None:
            if attr == 'impacts':

                supplier = self.get_supplier()
                impact_distribution, weights = supplier.get_impact_distribution() # this is a sampling of unit impacts

                declared_unit = supplier.get_unit()
                conversion_factor = declared_unit.get_conversion_factor(self.get_unit())

                impact_distributions = []
                for category in config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']:
                    data = []
                    for impact, weight in zip(impact_distribution, weights):
                        data.extend([impact.get_record(category) * conversion_factor * self.get_qty()] * int(weight))

                    impact_distributions.append(DataDistribution.from_data(data, is_cts=True, name=category, set_dist=False))

                return impact_distributions

            else:
                return self.data_distributions[attr]
    
class Emission(Product):
    """ Emission product object, inheriting from the product object.

    Attributes
    ----------
    is_emission : bool
        True  
    """

    def __init__(self):
        super().__init__()
        self.is_emssion = True

    def __str__(self):
        return f"Emission(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"

class Waste(Product):
    """ Waste product object, inheriting from the product object.

    Attributes
    ----------
    is_waste : bool
        True 
    """

    def __init__(self):
        super().__init__()
        self.is_waste = True

    def __str__(self):
        return f"Waste(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"


if __name__ == '__main__':
    pass
