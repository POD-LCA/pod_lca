__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

import pickle

from ..impacts import Emissions
from ..impacts import Impacts
from ..impacts import TranportationModeImpactsDatabase
from . import TransportationLeg, ForeignLeg, DomesticLeg
from ...units import KILOMETER


class TransportationManager:
    """This class maintains the legs of transportation for products transported.

    Attributes
    ----------
    name : str
        name of the project.
    transport_legs : dict
        Dictionary mapping products to their corresponding transportation legs: {**product** (:class:`~pod_lca.materials_screening.Product`) : **transport leg** (:class:`~pod_lca.transportation.TransportationLeg`)}.
    mode_impact_database : ~pod_lca.impacts.TranportationModeImpactsDatabase
        Database containing unit impacts for transportation modes.
    """

    def __init__(self):
        self.name = None
        self.transport_legs = {}
        self.mode_impact_database = None

    def __str__(self):
        str = "=" * 75 + "\n" + f"Project: {self.get_name()}\n" + "=" * 75 + "\n"

        for leg in self.get_transportation_legs():
            str += f"{leg} \n"

        return str

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, name=None):
        """Create a new project.

        Parameters
        ----------
        name : str
            Name of the project.

        Returns
        -------
        ~pod_lca.transportation.TransportationManager
            Project created.
        """
        new_project = cls()
        new_project.set_name(name)

        return new_project

    # ================================
    # Setters
    # ================================
    def set_name(self, name: str):
        """Set the name of the project.

        Parameters
        ----------
        name : str
            Name of the project.
        """
        self.name = name

        return self

    def set_impact_database(self, database):
        """Set mode impact database used in the project.

        Parameters
        ----------
        database : ~pod_lca.impacts.TranportationModeImpactsDatabase or str
            Impact database object or if a string, filepath to the corresponding csv file containing impact data.

        Raises
        ------
        TypeError
            Database input not recognized
        """
        if isinstance(database, TranportationModeImpactsDatabase):
            self.mode_impact_database = database
        elif isinstance(database, str):
            transport_impact_database = TranportationModeImpactsDatabase.new("mode impact database")
            transport_impact_database.set_data(database)
            self.set_impact_database(transport_impact_database)
        else:
            raise TypeError("Database input not recognized")

        return self

    def set_project_origin(self, origin: str):
        """Set the origin location of the project.

        Parameters
        ----------
        origin : str
            Origin location of the project.
        """
        for leg in self.get_transportation_legs():
            leg.set_shipping_org(origin)
        # TODO consider having a project level variable for origin

    def set_project_destination(self, destination: str):
        """Set the destination location of the project.

        Parameters
        ----------
        destination : str
            Destination location of the project.
        """
        for leg in self.get_transportation_legs():
            leg.set_shipping_dest(destination)
        # TODO consider having a project level variable for origin

    def set_scenario(self, transportation_scenario):
        pass  # TODO: set project level scenario

    # ================================
    # Setters
    # ================================
    def get_name(self):
        """Retrieve the name of the project.

        Returns
        -------
        str
            Name of the project.
        """
        return self.name

    def get_transportation_legs(self):
        """Retrieve the transportation legs of the project.

        Returns
        -------
        list of ~pod_lca.transportation.TransportationLeg
            List of transportation legs.
        """
        return sum(self.transport_legs.values(), [])

    def get_transportation_leg(self, product):
        """Retrieve the transportation legs corresponding to a product.

        Parameters
        ----------
        product : ~pod_lca.materials_screening.Product
            Object for which the transportation leg correspond to.

        Returns
        -------
        ~pod_lca.transportation.TransportationLeg
            Transportation leg.
        """
        if product in self.transport_legs:
            return self.transport_legs[product]

    def get_goods(self):
        """Retrieve the goods of the project.

        Returns
        -------
        list of ~pod_lca.materials_screening.Product
            List of goods.
        """
        return list(self.transport_legs.keys())

    def get_impact_database(self):
        """Retrieve the transportation mode impact database.

        Returns
        -------
        ~pod_lca.impacts.TranportationModeImpactsDatabase
            Transportation mode impact database.
        """
        return self.mode_impact_database

    def get_impacts(self, product=None):
        """Retrieve the impacts of the project.

        Parameters
        ----------
        product : ~pod_lca.materials_screening.Product
            Product for which the transportation impacts rquested

        Returns
        -------
        ~pod_lca.impacts.Impacts
            Impacts of the project.

        Raises
        ------
        ValueError
            Product not found in the project.
        """
        if product is None:
            impact = Impacts.from_parent(self)
            for leg in self.get_transportation_legs():
                impact += leg.get_impacts()

            return impact

        else:
            if product not in self.transport_legs:
                raise ValueError(f"Product '{product}' not found in the project.")

            impact = Impacts.from_parent(self)
            for leg in self.transport_legs[product]:
                impact += leg.get_impacts()

            return impact

    def get_emissions(self, product=None):
        """Retrieve the emissions of the product.

        Parameters
        ----------
        product : ~pod_lca.materials_screening.Product
            Product for which the transportation impacts rquested

        Returns
        -------
        ~pod_lca.impacts.Emissions
            Emissions of the product/process.

        Raises
        ------
        ValueError
            Product not found in the project.
        """
        if product is None:
            impact = Emissions.from_parent(self)
            for leg in self.get_transportation_legs():
                impact += leg.get_emissions()

            return impact

        else:
            if product not in self.transport_legs:
                raise ValueError(f"Product '{product}' not found in the project.")

            impact = Emissions.from_parent(self)
            for leg in self.transport_legs[product]:
                impact += leg.get_emissions()

            return impact

    # ================================
    # Model Methods
    # ================================
    def add_good(
        self,
        good,
        travel_dist=None,
        shipping_dest=None,
        shipping_org=None,
        transport_scenario=None,
        distance_unit=KILOMETER,
        return_trip_factor=None,
        mode_name=None,
        mode_fuel_type="Regular",
        mode_efficiency="Median",
    ):
        """Add goods to the project. This method creates the appropriate transportation legs based on the data provided

        Parameters
        ----------
        good : ~pod_lca.materials_screening.Product
            Goods to be transported.
        travel_dist : float
            Transportation distance for goods
        shipping_dest : ~pod_lca.location.Location
            Shipping destination.
        shipping_org : ~pod_lca.location.Location
            Shipping origin
        transportation_scenario : {'Local', 'Regional', 'Regional_c', 'National', 'Global'}
            Transportation scenario considered.
        distance_unit : ~pod_lca.units.Unit
            Unit of measurement of distances.
        return_trip_factor : float
            Return trip factor.
        mode_name : {'Truck', 'E_Truck', 'Rail', 'Barge', 'Ocean', 'Air'}
            Name of the transportation mode.
        mode_efficiency : {'High', 'Median', 'Low'}
            Efficiency of the transportation mode.

        Raises
        ------
        ValueError
            Transport scenario not recognized.
        """
        self.transport_legs[good] = []

        # select type of leg
        if isinstance(travel_dist, (int, float)):
            LinkClass = TransportationLeg

        elif (shipping_dest is not None) and (shipping_org is not None):
            if (shipping_dest.get_country_code() == "US") and not (shipping_org.get_country_code() == "US"):
                LinkClass = ForeignLeg
            elif (shipping_dest.get_country_code() == "US") and (shipping_org.get_country_code() == "US"):
                LinkClass = DomesticLeg
            else:
                raise NotImplementedError

        elif isinstance(transport_scenario, str):
            if transport_scenario in ["Global"]:
                LinkClass = ForeignLeg
            elif transport_scenario in ["National", "Regional_c", "Regional", "Local"]:
                LinkClass = DomesticLeg
            else:
                raise ValueError("Transport scenario not recognized.")

        else:
            LinkClass = DomesticLeg

        # create transportation leg
        leg = LinkClass.in_project(good, self, "transport_" + good.get_name())

        leg.set_mode(mode_name, mode_efficiency)

        leg.set_travel_dist(travel_dist, distance_unit, return_trip_factor)
        leg.set_shipping_destination(shipping_dest)
        leg.set_shipping_origin(shipping_org)
        if isinstance(leg, (DomesticLeg, ForeignLeg)):
            leg.set_transport_scenario(transport_scenario)

        return self
    
    def remove_good(self, good):
        """Remove a good and its corresponding transportation legs from the project.

        Parameters
        ----------
        good : ~pod_lca.materials_screening.Product
            Good to be removed.

        Raises
        ------
        ValueError
            Good not found in the project.
        """
        if good not in self.transport_legs:
            raise ValueError(f"Good '{good}' not found in the project.")

        del self.transport_legs[good]

        return self

    # ================================
    # Project Methods
    # ================================
    def clear_project(self):
        """Clear the project by removing all transportation legs."""
        self.transport_legs = {}

        return self

    def save(self, file_path: str):
        """Save as a *.pkl file.

        Parameters
        ----------
        file_path : str
            Location (including the name) where the data be saved.
        """
        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(file_path: str):
        """Load a project from a pickled file.

        Parameters
        ----------
        file_path : str
            Location (including the name) where the data be loaded from.

        Raises
        ------
        FileNotFoundError
            File not found.
        PermissionError
            Permission denied to access file.
        """
        try:
            with open(file_path, "rb") as file:
                project = pickle.load(file)
            return project
        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("Permission denied.")
        except Exception as e:
            print("An error occurred:", e)


if __name__ == "__main__":
    pass
