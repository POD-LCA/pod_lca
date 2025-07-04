
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

import pickle

from ..impacts import Emissions
from ..impacts import Impacts
from ..impacts import TranportationModeImpactsDatabase
from ..location import Location
from ..transportation import LogisticLink, ForeignLink, DomesticLink
from ...units import KILOMETER


class ProjectLogisticManager:
    """ ProjectLogisticManager class which maintains the links of transportation.

    Attributes
    ----------
    name : str
        name of the project.
    goods_links_map : dict
        Dictionary mapping products to their corresponding transportation links.
    mode_impact_database : TranportationModeImpactsDatabase Obj
        Database containing unit impacts for transportation modes.
    """

    def __init__(self):
        self.name = None
        self.goods_links_map = {}
        self.mode_impact_database = None

    def __str__(self):
        str = "="*75 + "\n" + f"Project: {self.get_name()}\n" + "="*75 + "\n"

        for link in self.get_links():
            str += f"{link} \n"

        return str

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, name=None):
        """ Create a new project.

        Parameters
        ----------
        name : str
            Name of the project.

        Returns
        -------
        Project Obj.
            Project created.
        """
        new_project = cls()
        new_project.set_name(name)

        return new_project  

    # ================================
    # Setters
    # ================================
    def set_name(self, name:(str)):
        """ Set the name of the project.

        Parameters
        ----------
        name : str
            Name of the project.
        """
        self.name = name

        return self
    
    def set_database(self, database):
        """ Set mode impact database used in the project.
        
        Parameters
        ----------
        database : TranportationModeImpactsDatabase Obj or str
            Impact database created or filepath to the corresponding csv file containing impact data.
        """
        if isinstance(database, TranportationModeImpactsDatabase):
            self.mode_impact_database = database
        elif isinstance(database, str):
            transport_impact_database = TranportationModeImpactsDatabase.new("mode impact database")
            transport_impact_database.set_data(database)
            self.set_database(transport_impact_database)
        else:
            raise TypeError("Database input not recognized")
        
        return self

    def set_project_origin(self, origin:(str)):
        """ Set the origin location of the project.

        Parameters
        ----------
        origin : str
            Origin location of the project.
        """
        for link in self.get_links():
            link.set_shipping_org(origin)
        # TODO consider having a project level variable for origin

    def set_project_destination(self, destination:(str)):
        """ Set the destination location of the project.

        Parameters
        ----------
        destination : str
            Destination location of the project.
        """
        for link in self.get_links():
            link.set_shipping_dest(destination)
        # TODO consider having a project level variable for origin

    def set_scenario(self, transportation_scenario):
        pass # TODO: set project level scenario

    # ================================
    # Setters
    # ================================
    def get_name(self):
        """ Retrieve the name of the project.

        Returns
        -------
        str
            Name of the project.
        """
        return self.name

    def get_links(self):
        """ Retrieve the links of the project.

        Returns
        -------
        list
            List of links.
        """
        return list(*self.goods_links_map.values())
    
    def get_link(self, product):
        """ Retrieve the links corresponding to a product.
        
        Parameters
        ----------
        product : Master Obj.
            Object for which the transportation links correspond to.
        """
        if product in self.goods_links_map:
            return self.goods_links_map[product]

    def get_goods(self):
        """ Retrieve the goods of the project.

        Returns
        -------
        list
            List of goods.
        """
        return list(self.goods_links_map.keys())

    def get_database(self):
        """ Retrieve the transportation mode impact database.
        
        Returns
        -------
        TranportationModeImpactsDatabase Obj.
            Transportation mode impact database.
        """
        return self.mode_impact_database
    
    def get_impacts(self, product=None):
        """ Retrieve the impacts of the project.

        Parameters
        ----------
        product : Master Obj.
            Product for which the transportation impacts rquested

        Returns
        -------
        Impacts Obj.
            Impacts of the project.
        """
        if product is None:
            impact = Impacts.from_parent(self)
            for link in self.get_links():
                impact += link.get_impact()

            return impact
        
        else:
            if product not in self.goods_links_map:
                raise ValueError(f"Product '{product}' not found in the project.")
            
            impact = Impacts.from_parent(self)
            for link in self.goods_links_map[product]:
                impact += link.get_impacts()

            return impact

    def get_emissions(self, product=None):
        """ Retrieve the emissions of the product.

        Parameters
        ----------
        product : Master Obj or list of Master Obj.
            Product for which the transportation impacts rquested

        Returns
        -------
        Emissions Obj.
            Emissions of the product/process.
        """
        if product is None:
            impact = Emissions.from_parent(self)
            for link in self.get_links():
                impact += link.get_emissions()

            return impact
        
        else:
            if product not in self.goods_links_map:
                raise ValueError(f"Product '{product}' not found in the project.")
            
            impact = Emissions.from_parent(self)
            for link in self.goods_links_map[product]:
                impact += link.get_emissions()

            return impact
    
    # ================================
    # Model Methods
    # ================================
    def add_good(self, 
                  good, 
                  travel_dist=None,
                  shipping_dest=None, 
                  shipping_org=None,
                  transport_scenario=None,
                  distance_unit= KILOMETER, 
                  return_trip_factor=None, 
                  mode_name=None,
                  mode_fuel_type="Regular", 
                  mode_efficiency="Median"):
        """ Add goods to the project. This method creates the appropriate logistick links based on the data provided

        Parameters
        ----------
        goods : list of Product Obj.
            Goods to be transported.
        travel_dist : float
            Transportation distance for goods
        shipping_dest : Location Obj
            Shipping destination.
        shipping_org : Location Obj
            Shipping origin
        transportation_scenario : str
            Transportation scenario considered.
        distance_unit : Unit Obj
            Unit of measurement of distances.
        return_trip_factor : float
            Return trip factor.
        mode_name : str
            Name of the transportation mode.
        mode_fuel_type : str
            Fuel type used by the transportation mode.
        mode_efficiency : str
            Efficiency of the transportation mode.
        """
        self.goods_links_map[good] = []

        # select type of link
        if isinstance(travel_dist, (int, float)):
            LinkClass = LogisticLink

        elif (shipping_dest is not None) and (shipping_org is not None):
            if (shipping_dest.get_country_code() == 'US') and not (shipping_org.get_country_code() == 'US'):
                LinkClass = ForeignLink
            elif (shipping_dest.get_country_code() == 'US') and (shipping_org.get_country_code() == 'US'):
                LinkClass = DomesticLink
            else:
                raise NotImplementedError

        elif isinstance(transport_scenario, str):
            if transport_scenario in ["North_america", "Global"]:
                LinkClass = ForeignLink
            elif transport_scenario in ["National", "Regional_c", "Regional", "Local"]:
                LinkClass = DomesticLink
            else:
                raise ValueError("Transport scenario not recognized.")
            
        else:
            LinkClass = DomesticLink

        # create link
        link = LinkClass.in_project(good, self, 'transport_' + good.get_name())
        
        link.set_mode(mode_name, mode_fuel_type, mode_efficiency)

        link.set_travel_dist(travel_dist, distance_unit, return_trip_factor)
        link.set_shipping_destination(shipping_dest)
        link.set_shipping_origin(shipping_org)
        if isinstance(link, (DomesticLink, ForeignLink)):
            link.set_transport_scenario(transport_scenario)

        return self

    # ================================
    # Project Methods
    # ================================
    def clear_project(self, links=True, impacts=True):  
        """ Clear the project by removing all links and impacts.
        """
        self.goods_links_map = {}

        return self

    def save(self, file_path:(str)):
        """ Save as a *.pkl file.

        Parameters
        ----------
        file_path : str
            Location (including the name) where the data be saved.
        """
        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(file_path:(str)):
        """ Load a project from a pickled file.

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
            with open(file_path, 'rb') as file:
                project = pickle.load(file)
            return project
        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("Permission denied.")
        except Exception as e:
            print("An error occurred:", e)


if __name__ == '__main__':
    pass
