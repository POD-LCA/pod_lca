__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Master
from ..carbon_storage import CarbonStorage
from ..electricity import ElectricitySupply
from ..impacts import Emissions
from ..impacts import Impacts
from ..location import Location
from ..analysis import DataDistribution
from ...utilities import config


class Electricity(Master):
    """Electricity product object, inheriting from the Fuel object.

    Attributes
    ----------
    electricity_supplier: ~pod_lca.electricity.ElectricitySupply
        Electricity supplier
    year : int
        Year of electricity consumption
    geographical_scope: {'National'. 'Regional', 'Local'}
        Geographical scope considered for electricity data.
    scenario: str
        Cambium scenario for prediction of electricity technology futures.
    """

    def __init__(self):
        super().__init__()
        self.electricity_supplier = None
        self.year = None
        self.geographical_scope = None
        self.location = None
        self.scenario = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, id, name, model, stage, qty, unit, location=None, year=None):
        """Create a new electricity product in a model.

        Parameters
        ----------
        id : int
            An identification number.
        name : str
            Name of the item.
        model : ~pod_lca.materials_screening.Model
            Model in which the item is created.
        stage : {'A1', 'A3'}
            LCA stage.
            - 'A1': Raw materials supply.
            - 'A3': manufacturing.
        qty : float
            Quantity of the item
        unit : ~pod_lca.units.Unit
            Unit corresponding to the quantity.
        """
        item = cls()

        item.set_id(id)
        item.set_name(name)
        item.set_model(model)
        item.set_life_cycle_stage(stage)
        item.set_qty(qty)
        item.set_unit(unit)
        item.impacts = Impacts.from_parent(item)
        item.emissions = Emissions.from_parent(item)
        item.carbon_storage = CarbonStorage.from_parent(item)

        if location is None:
            location = model.get_location()
        electricity_supplier = ElectricitySupply.from_location(location, year)
        item.set_supplier(electricity_supplier)

        return item

    @classmethod
    def from_unit_inventories(cls, name, qty, unit, impacts, emissions, carbon_storage):
        """Create an electricity impact from given impacts. This is primarily for seperating electricity component of products.

        Parameters
        ----------
        name : str
            Name of the electricity.
        qty : float
            Quantity of elctricity consumption.
        unit : ~pod_lca.units.Unit
            Unit of electricity consumption.
        impacts : ~pod_lca.impacts.Impacts
            Impacts corresponding to electricity consumption.
        emissions : ~pod_lca.impacts.Emissions
            Emissions corresponding to electricity consumption.
        carbon_storage : ~pod_lca.impacts.CarbonStorage
            Carbon storage corresponding to electricity consumption.
        """
        item = cls()

        item.set_name(name)
        item.set_qty(qty)
        item.set_unit(unit)
        item.impacts = Impacts.from_parent(item)
        item.emissions = Emissions.from_parent(item)
        item.carbon_storage = CarbonStorage.from_parent(item)

        item.unit_impacts = impacts
        item.unit_emissions = emissions
        item.unit_carbon_storage = carbon_storage

        item.inventories_declared_unit = unit
        item.inventories_declared_qty = 1.0

        return item

    # ================================
    # Setters
    # ================================
    def set_impact_database_entry(self, database_item: str):
        """Electricity does not directly read from database."""
        pass

    def set_supplier(self, supplier):
        """Set electricity supplier.

        Parameters
        ----------
        supplier : ~pod_lca.electricity.ElectricitySupply
            Electricity supply
        """
        self.electricity_supplier = supplier

        self.unit_impacts = supplier.get_unit_impacts()
        self.unit_emissions = supplier.get_unit_emissions()
        self.unit_carbon_storage = CarbonStorage.from_parent(
            supplier
        )  # ElectricitySupply does not have CarbonStorage record

        self.inventories_declared_qty = 1.0  # ElectricitySupply computes impact per one unit
        self.inventories_declared_unit = supplier.get_declared_unit()

        return self

    def set_year(self, year):
        """Set the year of electricity consumption.

        Parameters
        ----------
        year : int
            Year of electricity consumption.
        """
        self.year = year

        if self.get_supplier() is not None:
            self.get_supplier().set_year(year)

        return self

    def set_geographical_scope(self, geographical_scope):
        """Set the spatial resolution of the electricity supply.

        Parameters
        ----------
        geographical_scope : {'National', 'Regional', 'Local'}
            Geographical scope of the electricity supply.
        """
        self.geographical_scope = geographical_scope

        if self.get_supplier() is not None:
            self.get_supplier().set_geographical_scope(geographical_scope)

        return self
    
    def set_location(self, **kwargs):
        """Set location object for electricity supply.

        Other Parameters
        ----------------
        location_obj : ~pod_lca.location.Location, optional
            Location object to set, by default None
        zip_code : str, optional
            Zip code to set, by default None
        state : str, optional
            US State to set, by default None
        """
        location_obj = None
        if "location_obj" in kwargs:
            location_obj = kwargs["location_obj"]
        if "zip_code" in kwargs:
            location_obj = Location.from_US_zip(kwargs["zip_code"])
        if "state" in kwargs:
            location_obj = Location.from_US_state(kwargs["state"])

        self.location = location_obj
        if self.get_supplier() is not None:
            self.get_supplier().set_location(location_obj)

        return self

    def set_scenario(self, scenario):
        """Set scenario name. This will be used with cambium data.

        Parameters
        ----------
        scenario : {'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'}
            Electricity consmuption scenario considered.

        Raises
        ------
        ValueError
            Scenario is not recognized.
        """
        self.scenario = scenario

        if self.get_supplier() is not None:
            if scenario in [
                "MidCase",
                "LowRECost",
                "HighRECost",
                "HighDemandGrowth",
                "LowNGPrice",
                "HighNGPrice",
                "Decarb95by2050",
                "Decarb100by2035",
            ]:
                self.get_supplier().set_scenario(scenario)
            else:
                raise ValueError(
                    f"Scenario {scenario} is not a valid scenario. Valid scenarios are: 'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'."
                )

        return self

    # ================================
    # Getters
    # ================================
    def get_impact_database_entry(self):
        """Electricity does not directly read from database."""
        pass

    def get_supplier(self):
        """Get the electricity supplier.

        Returns
        -------
        ~pod_lca.electricity.ElectricitySupply
            Electricity supplier.
        """
        return self.electricity_supplier

    def get_year(self):
        """Get the year of electricity consumption.

        Returns
        -------
        int
            Year of electricity consumption.
        """
        if self.year is None:
            self.year = self.get_supplier().get_year()
        return self.year

    def get_geographical_scope(self):
        """Get the spatial resolution of the electricity supply.

        Parameters
        ----------
        str
            Spatial resolution of the electricity supply: 'National', 'Regional', 'Local'.
        """
        if self.geographical_scope is None:
            self.geographical_scope = self.get_supplier().get_geographical_scope()
        return self.geographical_scope

    def get_location(self):
        """Get location object for electricity supply.

        Returns
        -------
        ~pod_lca.location.Location
            Location object.
        """
        if self.location is None:
            return self.get_supplier().get_location()
        else:
            return self.location
    
    def get_scenario(self):
        """Get scenario name. This will what used with cambium data.

        Parameters
        ----------
        str
            Electricity consmuption scenario considered: e.g., 'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'.
        """
        if self.scenario is None:
            self.scenario = self.get_supplier().get_scenario()
        return self.scenario

    def get_data_distribution(self, attr):
        """Get data_distribution object corresponding to the given attribute.

        Parameters
        ----------
        attr : str
            Attribute to which the distribution correspond.

        Returns
        -------
        ~pod_lca.uncertainty.DataDistribution
            Data distribution.
        """
        if (attr == "impacts") and (self.get_supplier() is not None):
            supplier = self.get_supplier()
            impact_distribution, weights = supplier.get_impact_distribution()  # this is a sampling of unit impacts

            declared_unit = supplier.get_declared_unit()
            conversion_factor = declared_unit.convert_to(self.get_unit())

            impact_distributions = []
            for category in config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"]:
                data = []
                for impact, weight in zip(impact_distribution, weights):
                    data.extend([impact.get_record(category) * conversion_factor * self.get_qty()] * int(weight))

                impact_distributions.append(
                    DataDistribution.from_data(data, is_cts=True, name=category, set_dist=False)
                )

            return impact_distributions
        else:
            return self.data_distributions[attr]

    # ================================
    # Methods
    # ================================
    def update_inventory_records(self):
        """Sets impacts quantities, based on database item asigned to the product/process and the product/process quantity. If no database entry is asigned, impacts are not updated."""
        if self.get_supplier() is not None:
            supplier = self.get_supplier()
            supplier.update_inventory_records()

        super().update_inventory_records()

        return self


if __name__ == "__main__":
    pass
